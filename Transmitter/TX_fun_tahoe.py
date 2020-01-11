import threading
import time
from threading import Lock
from TX_fun_encode import *


BUFFER_SIZE = DEFAULT_SIZE + 8  # 4 segment_number, 1 tip, 2 lungime
TIME_TO_WAIT = 2  # Round Trip Time
cwnd = 2  # congestion window pleaca de la 2, pentru ca pentru cwnd 1 am functia recvfrom care e blocanta
sstresh = 30  # slow strat threshhold
timers_queue = []
lock = Lock()
pack_ack_to_retransmit = 0
attention = False
segments_in_pipe = 0
sending_done = False
last_ack_of_file = 0

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


def packet_dropped():
    global cwnd
    global sstresh
    global lock

    lock.acquire()
    sstresh = cwnd / 2
    cwnd = 1
    lock.release()

    # RESTRANSMITE PACHETE INCEPAND CU last_ack_received



def TX_read_ack(sock):
    global timers_queue
    global segments_in_pipe
    global lock
    global sending_done
    global last_ack_of_file
    global pack_ack_to_retransmit
    global attention


    print("TX_read_ack thread started")
    last_ack_received = 2 # ack 2 este pentru pachetul de start
    number_ack_duplicate = 0

    # mai trebuie sa merg niste iteratii cand sending_done, abia am trimis pachetul end, nu am primit ack de la el
    while sending_done == False or last_ack_of_file == (last_ack_received - 1):
        data, addr = sock.recvfrom(DEFAULT_SIZE)  # functie blocanta
        ack_received = int.from_bytes(data, byteorder='big', signed=False)   # segment_number este fix data
        print('last ack =  {}...'.format(last_ack_received))
        print('A fost receptionat segment_number = {}... \n'.format(ack_received))

        if ack_received == last_ack_received + 1:  # am primit un ack bun
            last_ack_received += 1
            lock.acquire()
            timer = timers_queue.pop(0)
            lock.release()

            timer.cancel()

            lock.acquire()
            segments_in_pipe = segments_in_pipe - 1
            lock.release()

            packet_received()

        else:   # am primit un ack mai mic sau egal specific unui pachet al carui ack deja l-am primit
            print('--Ack primit este duplicat...')
            number_ack_duplicate = number_ack_duplicate + 1
            attention = True
            if 3 == number_ack_duplicate:
                print('--- 3 ack duplicate!!!')
                pack_ack_to_retransmit = ack_received
                packet_dropped()
                number_ack_duplicate = 0



def TX_send(sock, address_port, file_name_to_send):
    global timers_queue
    global segments_in_pipe
    global lock
    global sending_done
    global last_ack_of_file

    print(f"TX_send thread started sending = {sending_done}")
    while sending_done == False:
        for segment in encode_bytes(file_name_to_send):
            # daca pipe-ul e plin
            while segments_in_pipe >= cwnd:
                time.sleep(0.5)
                #asteapta un ack
            # else
            #   increamenteaza contor si trimite

            tip = segment_decode(segment)['tip']
            if tip == 3:
                sending_done = True
                last_ack_of_file = segment_decode(segment)['ack']

            lock.acquire()
            segments_in_pipe = segments_in_pipe + 1
            lock.release()

            # creez si pornesc timer
            timer = threading.Timer(TIME_TO_WAIT, packet_dropped, args=None, kwargs=None)
            timer.start()

            lock.acquire()
            timers_queue.append(timer)
            lock.release()

            sock.sendto(segment, address_port)
            segment_number = segment_decode(segment)['ack']
            print(f'Am trimis pachetul cu ack = {segment_number} \n')


            # adaug timerul in coada de timere



def tahoe_congestion_control(sock, address_port, file_name_to_send):
    print('Trimitem pachetul de start...')
    time.sleep(0.2)
    segment = encode('START', file_name_to_send)
    sock.sendto(segment, address_port)
    print('A fost trimis pachetul de start, astept confirmarea primirii...')
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print('A fost receptionat... {}'.format(data))
    ack_binary = bytearray([data[i] for i in range(4)])
    segment_number = int.from_bytes(ack_binary, byteorder='big', signed=False)
    if segment_number == 2:
        print('Am primit ack pentru pachetul de START')
    else:
        print('Am primit ack gresit pentru pachetul de START')

    # s-a creat fisierul la destinatie, pot incepe popularea acestuia cu informatii

    # creez thread pentru primirea confirmarilor pachetelor
    TX_RX_thread = threading.Thread(target=TX_read_ack, args=(sock, ))
    TX_RX_thread.start()

    # creez thread pentru trimiterea pachetelor
    TX_TX_thread = threading.Thread(target=TX_send, args=(sock, address_port, file_name_to_send))
    TX_TX_thread.start()

    #astept ca cele 2 threaduri sa-si fi terminat executia
    TX_RX_thread.join()
    TX_TX_thread.join()
