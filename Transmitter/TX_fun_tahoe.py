import threading
import time
from threading import Lock
from TX_fun_encode import *


BUFFER_SIZE = DEFAULT_SIZE + 8  # 4 segment_number, 1 tip, 2 lungime
TIME_TO_WAIT = 2  # Round Trip Time
cwnd = 2  # congestion window pleaca de la 2, pentru ca pentru cwnd 1 am functia recvfrom care e blocanta
sstresh = 30  # slow start threshhold
timers_queue = []
lock = Lock()
pack_ack_to_retransmit = 0
segments_in_pipe = 0
sending_done = False
last_ack_of_file = 0
last_segment_transmitted = 2
last_ack_received = 1
flag_retransmit = False
retransmit_thread = threading.Thread()
segment_pipe = []
number_ack_duplicate = 0


def packet_received():
    global cwnd
    global sstresh
    global lock

    lock.acquire()
    if cwnd < sstresh:
        cwnd = cwnd + cwnd
    else:
        cwnd = cwnd + 1
    lock.release()


def pack_retransmit(sock,address_port):
    global segment_pipe
    global timers_queue
    global flag_retransmit
    global segments_in_pipe

    time.sleep(2)
    segments_in_pipe = 0

    while len(timers_queue) > 0:
        lock.acquire()
        timer = timers_queue.pop(0)
        lock.release()

        timer.cancel()

    print('retransmit')
    first_loop = True
    segment_pipe = segment_pipe[1:] # nu se include primul deoarece este ultimul packet receptionat cu succes
    while len(segment_pipe) > 0 :
        segment = segment_pipe.pop(0)

        if first_loop == False and int(segment_decode(segment)['ack']) == last_ack_received + 1:
            segment_pipe.append(segment)
            break

        lock.acquire()
        segments_in_pipe = segments_in_pipe + 1
        lock.release()

        timer = threading.Timer(TIME_TO_WAIT, lambda : packet_dropped(sock,address_port), args=None, kwargs=None)
        timer.start()

        lock.acquire()
        timers_queue.append(timer)
        lock.release()

        sock.sendto(segment, address_port)
        segment_number = segment_decode(segment)['ack']
        print(f'Am trimis pachetul cu segment_number = {segment_number} \n')
        segment_pipe.append(segment)
        first_loop = False
        print('gata retransmisia')
    flag_retransmit = False


def packet_dropped(sock,address_port):  # '''type,pack_to_retransmit'''):
    global cwnd
    global sstresh
    global lock
    global last_ack_received
    global segment_pipe
    global number_ack_duplicate
    global flag_retransmit


    lock.acquire()
    sstresh = cwnd / 2
    cwnd = 1
    lock.release()

    flag_retransmit = True
    number_ack_duplicate = 0
    retransmit_thread = threading.Thread(target=pack_retransmit,args=(sock,address_port))
    retransmit_thread.start()




def TX_read_ack(sock,address_port):
    global timers_queue
    global segments_in_pipe
    global lock
    global sending_done
    global last_ack_of_file
    global pack_ack_to_retransmit
    global last_ack_received
    global segment_pipe
    global number_ack_duplicate
    global flag_retransmit

    print("TX_read_ack thread started")

    number_ack_duplicate = 0
    last_ack_received += 1  # ack = 2 este pentru pachetul de start (are segment number = 1)
    # mai trebuie sa merg niste iteratii cand sending_done, abia am trimis pachetul end, nu am primit ack de la el
    while sending_done == False or (last_ack_received != last_ack_of_file + 1):
        data, addr = sock.recvfrom(DEFAULT_SIZE)  # functie blocanta
        ack_received = int.from_bytes(data, byteorder='big', signed=False)   # segment_number este fix data
        print('last ack received=  {}...'.format(last_ack_received))
        print('A fost receptionat segment_number = {}... \n'.format(ack_received))

        lock.acquire()
        segments_in_pipe = segments_in_pipe - 1
        lock.release()

        print(f"ack received : last_ack_received {ack_received}  {last_ack_received}")
        if ack_received == last_ack_received + 1:  # am primit un ack bun
            segment_pipe.pop(0)

            last_ack_received += 1
            lock.acquire()
            timer = timers_queue.pop(0)
            lock.release()

            timer.cancel()

            packet_received()

        else:   # am primit acelasi ack
            print('--Ack primit este duplicat...')
            number_ack_duplicate = number_ack_duplicate + 1
            if 3 == number_ack_duplicate:
                print('--- 3 ack duplicate!!!')
                packet_dropped(sock,address_port)
                number_ack_duplicate = 0

    sending_done = False
    print('TX_RX_done')




def TX_send(sock, address_port, file_name_to_send):
    global timers_queue
    global segments_in_pipe
    global lock
    global sending_done
    global last_ack_of_file
    global segment_pipe
    global number_ack_duplicate
    global flag_retransmit

    print(f"TX_send thread started sending_done = {sending_done}")
    while sending_done == False:
        for segment in encode_bytes(file_name_to_send):
            # daca pipe-ul e plin

            # de implementat: porneste un TIMER sa nu astepte la infinit

            while segments_in_pipe >= cwnd:
                time.sleep(0.5)
            while retransmit_thread.is_alive() == True:
                retransmit_thread.join()
                #time.sleep(0.5)
                #asteapta un ack
            # else
            #   increamenteaza contor si trimite

            tip = segment_decode(segment)['tip']
            if tip == 3:
                sending_done = True
                last_ack_of_file = segment_decode(segment)['ack']
                print(f'last_ack_of_file = {last_ack_of_file }\n')

            lock.acquire()
            segments_in_pipe = segments_in_pipe + 1
            lock.release()

            # creez si pornesc timer

            timer = threading.Timer(TIME_TO_WAIT, lambda : packet_dropped(sock,address_port), args=None, kwargs=None)
            timer.start()

            lock.acquire()
            timers_queue.append(timer)
            lock.release()

            sock.sendto(segment, address_port)
            segment_number = segment_decode(segment)['ack']
            print(f'Am trimis pachetul cu segment_number = {segment_number} \n')

            segment_pipe.append(segment)

            # adaug timerul in coada de timere


def tahoe_congestion_control(sock, address_port, file_name_to_send):
    print('Trimitem pachetul de start...')
    time.sleep(0.2)
    segment = encode('START', file_name_to_send)
    ack_binary = bytearray([segment[i] for i in range(4)])
    segment_number_sent = int.from_bytes(ack_binary, byteorder='big', signed=False)

    sock.sendto(segment, address_port)
    print('A fost trimis pachetul de start, astept confirmarea primirii...')

    data, addr = sock.recvfrom(BUFFER_SIZE)
    print('A fost receptionat... {}'.format(data))

    ack_binary = bytearray([data[i] for i in range(4)])
    segment_number_received = int.from_bytes(ack_binary, byteorder='big', signed=False)
    if segment_number_received == (segment_number_sent + 1):
        print('Am primit ack pentru pachetul de START')
        # s-a creat fisierul la destinatie, pot incepe popularea acestuia cu informatii

        # creez thread pentru primirea confirmarilor pachetelor
        TX_RX_thread = threading.Thread(target=TX_read_ack, args=(sock,address_port))
        TX_RX_thread.start()

        # creez thread pentru trimiterea pachetelor
        TX_TX_thread = threading.Thread(target=TX_send, args=(sock, address_port, file_name_to_send))
        TX_TX_thread.start()

        # astept ca cele 2 threaduri sa-si fi terminat executia
        TX_RX_thread.join()
        TX_TX_thread.join()
    else:
        print('Am primit ack gresit pentru pachetul de START')


