import threading
import time
from threading import Lock
from RXfun import SegmentDecode

DEFAULT_SIZE = 512
TIME_TO_WAIT = 2
ack = 0     # ack == 1
cwnd = 1
threshold = 30
timers_queue = []
lock = Lock()
pack_ack_to_retransmit = 0
attention = False
segments_in_pipe = 0

def DataFieldDecode(data,length):
    date = ''
    for i in range(length):
        date += chr(data[i])
    return date


def increment_ack():
    global ack
    ack = ack + 1


def encode_start(segment_data):
    increment_ack()
    segment_number = ack.to_bytes(4, byteorder='big', signed=False)
    segment_type = b'\x01'
    segment_data_len = len(segment_data)
    segment_len = segment_data_len.to_bytes(2, byteorder='big', signed=False)
    segment = segment_number + segment_type + segment_len
    for ch in segment_data:
        segment += (ord(ch).to_bytes(1, byteorder='big', signed=False))
    return segment



def encode_data(segment_data):
    increment_ack()
    segment_number = ack.to_bytes(4, byteorder='big', signed=False)
    segment_type = b'\x02'
    segment_data_len = len(segment_data)
    segment_data = segment_data + b'\x00'*(DEFAULT_SIZE - segment_data_len)
    segment_data_len = DEFAULT_SIZE
    segment_len = segment_data_len.to_bytes(2, byteorder='big', signed=False)
    segment = segment_number + segment_type + segment_len + segment_data
    return segment



# in campul de segment_code, al doilea octet va fi lungimea caracterelor utile
def encode_end(segment_data):
    increment_ack()
    segment_number = ack.to_bytes(4, byteorder='big', signed=False)
    segment_type = b'\x03'
    segment_data_len = len(segment_data)
    segment_data = segment_data + b'\x00'*(DEFAULT_SIZE - segment_data_len)
    segment_len = segment_data_len.to_bytes(2, byteorder='big', signed=False)
    segment = segment_number + segment_type + segment_len + segment_data
    return segment


def encode_error(segment_data):
    pass


segment_type = {
    'START': encode_start,
    'DATA': encode_data,
    'END': encode_end
}


def encode(tip, data):
    return segment_type.get(tip, encode_error)(data)


#citirea fisier ca pachete de octeti
def bytes_from_file(filename, chunk_size=DEFAULT_SIZE):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


#codificarea pachetelor de octeti
def encode_bytes(filename):
    for b in bytes_from_file(filename):
        if len(b) == DEFAULT_SIZE:
            yield encode('DATA', b)
        else:
            yield encode('END', b)




def update_good_cwnd():
    global cwnd
    global threshold
    global lock

    lock.acquire()
    if cwnd < threshold:
        cwnd = cwnd + cwnd
    else:
        cwnd = cwnd + 1
    lock.release()


def update_duplicate_cwnd():
    global cwnd
    global threshold
    global lock

    lock.acquire()
    threshold = cwnd / 2
    cwnd = 1
    lock.release()


def update_time_cwnd():
    global cwnd
    global threshold
    global lock

    lock.acquire()
    threshold = cwnd / 2
    cwnd = 1
    lock.relase()


ack_type = {
    'GOOD': update_good_cwnd,
    'DUPLICATE': update_duplicate_cwnd,
    'TIME': update_time_cwnd
}


def update_cwnd(tip):
    return segment_type.get(tip, encode_error)()


def TX_read_ack(sock):
    global timers_queue
    global segments_in_pipe
    global lock
    global pack_ack_to_retransmit
    global attention

    last_ack_received = 2 # ack 1 este pentru pachetul de start
    number_ack_duplicate = 0
    while True:
        print('am ajuns aici')
        data, addr = sock.recvfrom(DEFAULT_SIZE)
        print('A fost receptionat ack = {}...'.format(data))
        ack_received = int.from_bytes(data, byteorder='big', signed=False)   # ack este fix data
        if ack_received != last_ack_received:  # am primit un ack bun
            print('--Ack primit este corect...')
            lock.acquire()
            timer = timers_queue.pop(0)
            lock.relase()

            timer.cancel()

            lock.acquire()
            segments_in_pipe = segments_in_pipe - 1
            lock.release()

            update_good_cwnd()

        else:   # am primit un ack mai mic sau egal specific unui pachet al carui ack deja l-am primit
            print('--Ack primit este duplicat...')
            number_ack_duplicate = number_ack_duplicate + 1
            attention = True
            if 3 == number_ack_duplicate:
                print('--- 3 ack duplicate!!!')
                pack_ack_to_retransmit = ack_received
                update_duplicate_cwnd()
                number_ack_duplicate = 0



def tahoe_congestion_control(sock, address_port, file_name_to_send):
    global timers_queue
    global segments_in_pipe
    global lock
    global pack_ack_to_retransmit
    global attention

    segments_buffer = {} # buffer de 20 de segmente, folosit pt retransmitere
    #thread1 = threading.Thread(target=TX_read_ack, args=(sock,))   # creez thread pentru citire
    #thread1.run()
    print('am ajuns aici')
    data, addr = sock.recvfrom(DEFAULT_SIZE)
    print('A fost receptionat ack = {}...'.format(data))
    time.sleep(1)
    for segment in encode_bytes(file_name_to_send):
        # daca pipe-ul e plin
        #while segments_in_pipe >= cwnd:
         #   print('Pipe plin..')
         #   time.sleep(0.5)
            #asteapta un ack
        # else
        #   increamenteaza contor si trimite

        lock.acquire()
        segments_in_pipe = segments_in_pipe + 1
        lock.release()

        if pack_ack_to_retransmit == 0:
            seg_decoded = SegmentDecode(segment)
            print('Trimitem urmatorul pachet cu ack = {}'.format(seg_decoded['ack']))
            segments_buffer[seg_decoded['ack']] = segment
            sock.sendto(segment, address_port)
            time.sleep(0.025)
        else:
            print('Retransmitem un pachet...')
            sock.sendto(segments_buffer[pack_ack_to_retransmit],address_port)
            pack_ack_to_retransmit = 0
            attention = False

        # start timer
        timer = threading.Timer(TIME_TO_WAIT, update_time_cwnd, args=None, kwargs=None)

        lock.acquire()
        timers_queue.append(timer)
        lock.release()

        if attention == False and len(segments_buffer) == 20:
            segments_buffer = {}


