from threading import Lock
import os
from transmitter_data_encoding import *
from transmitter_network_handler import *

BUFFER_SIZE = DEFAULT_SIZE + 8
TIME_TO_WAIT = 0.8

class TransmitterController:
    def __init__(self):
        self.ip = None
        self.port_RX = None
        self.port_TX = None
        self.address_TX = None
        self.address_RX = None
        self.sock = None
        self.filepath = None
        self.cwnd = 2
        self.sstresh = 30
        self.timers_queue = []
        self.lock = Lock()
        self.flag_retransmit = False
        self.segments_in_pipe = 0
        self.sending_done = False
        self.last_ack_of_file = 0
        self.last_ack_received = 1
        self.number_ack_duplicate = 0
        self.last_ack_of_file_final = 0
        self.ack = 0
        self.networkHandler = NetworkHandler()

    def packet_received(self):
        self.lock.acquire()
        if self.cwnd < self.sstresh:
            self.cwnd = self.cwnd + self.cwnd
        else:
            self.cwnd = self.cwnd + 1
        self.lock.release()


    def packet_dropped(self):
        self.flag_retransmit = True
        self.lock.acquire()
        self.sstresh = self.cwnd / 2
        self.cwnd = 1
        self.lock.release()


    def segments_to_list(self):
        list_of_bytes = []
        segment_number = 0
        for segment in DataEncoding.encode_bytes(self):
            list_of_bytes.append(segment)
            segment_number += 1
        return list_of_bytes


    def TX_RX_fun(self,window):
        window.ConsoleAppendText("TX_read_ack thread started",1)
    
        self.number_ack_duplicate = 0
        self.last_ack_received += 1  # ack = 2 este pentru pachetul de start (are segment number = 1)
        # mai trebuie sa merg niste iteratii cand sending_done, abia am trimis pachetul end, nu am primit ack de la el
        while self.sending_done == False or (self.last_ack_received != self.last_ack_of_file + 1):
            data, addr = self.sock.recvfrom(DEFAULT_SIZE)  # functie blocanta
            ack_received = int.from_bytes(data, byteorder='big', signed=False)   # segment_number este fix data
            print('last ack received=  {}...'.format(self.last_ack_received))
            print('A fost receptionat segment_number = {}... \n'.format(ack_received))

            self.lock.acquire()
            self.segments_in_pipe = self.segments_in_pipe - 1
            self.lock.release()
    
            if ack_received == self.last_ack_received + 1:  # am primit un ack bun
                window.ConsoleAppendText(f"Pachetul {ack_received} a fost primit cu succes!!!",0)
                self.last_ack_received += 1
                self.lock.acquire()
                timer = self.timers_queue.pop(0)
                self.lock.release()
    
                timer.cancel()

                self.number_ack_duplicate = 0
                self.packet_received()
    
            else:   # am primit acelasi ack
                window.ConsoleAppendText(f'--RX: Ack primit {ack_received} este duplicat...',1)
                self.number_ack_duplicate = self.number_ack_duplicate + 1
                if 3 == self.number_ack_duplicate:
                    self.number_ack_duplicate = 0
                    if self.flag_retransmit == False :
                        self.flag_retransmit = True
                        window.ConsoleAppendText(f'--- RX : 3 ack duplicate {ack_received} !!!',1)
                        window.ConsoleAppendText(f'--- RX : Retransmitem pachetul {ack_received} !!!',0)
                        self.packet_dropped()

        self.sending_done = False
        window.ConsoleAppendText('TX_RX_done',0)
    
    
    
    def TX_TX_fun(self,window):

        window.ConsoleAppendText(f"TX_send thread started sending_done = {self.sending_done}",0)
        list_of_bytes = self.segments_to_list()
    
        filesize = os.path.getsize(self.filepath)
        window.ConsoleAppendText('Filesize = {} Bytes'.format(filesize),0)
        number_of_chunks = round(filesize/DEFAULT_SIZE)
        window.ConsoleAppendText('Number of chunks = {} '.format(number_of_chunks),0)
    
    
        i = 0
        while i < len(list_of_bytes) or self.segments_in_pipe != 0:
            while self.segments_in_pipe >= self.cwnd and self.flag_retransmit == False:
                window.ConsoleAppendText("TX: pipeline is full",1)
                time.sleep(0.25)

            if i >= len(list_of_bytes):
                time.sleep(2)
                if(self.segments_in_pipe == 0):
                    break
    
    
            if self.flag_retransmit == True:
                while len(self.timers_queue) > 0:
                    self.lock.acquire()
                    timer = self.timers_queue.pop(0)
                    self.lock.release()
    
                    timer.cancel()
                time.sleep(0.5)

                self.lock.acquire()
                segments_in_pipe = 0
                self.lock.release()

                self.lock.acquire()
                self.flag_retransmit = False
                self.lock.release()
    
                i = self.last_ack_received - 2 - self.last_ack_of_file_final
                window.ConsoleAppendText(f"Incep retransmisia cu segment_number = {self.last_ack_received}",1)
    
                # !! retransmite pachete aici
                continue
    
            segment = list_of_bytes[i]
            tip = DataEncoding.segment_decode(segment)['tip']
            if tip == 3:
                self.lock.acquire()
                sending_done = True
                self.lock.release()
                last_ack_of_file = DataEncoding.segment_decode(segment)['ack']
                window.ConsoleAppendText(f'TX: last_ack_of_file = {last_ack_of_file }\n',0)

            self.lock.acquire()
            self.segments_in_pipe = self.segments_in_pipe + 1
            self.lock.release()
    
            # creez si pornesc timer
    
            timer = threading.Timer(TIME_TO_WAIT, lambda : self.packet_dropped(), args=None, kwargs=None)
            timer.start()

            self.lock.acquire()
            self.timers_queue.append(timer)
            self.lock.release()


            self.sock.sendto(segment, self.address_TX)
    
            segment_number = DataEncoding.segment_decode(segment)['ack']
            window.ConsoleAppendText(f'TX:Sent segment_number = {segment_number}',1)
    
            i += 1
        time.sleep(1)

    def tahoe_congestion_control(self,window):

        window.ConsoleAppendText('Trimitem pachetul de start...',0)
        time.sleep(0.2)
    
        segment = DataEncoding.encode(self,'START',self.filepath)
        ack_binary = bytearray([segment[i] for i in range(4)])
        segment_number_sent = int.from_bytes(ack_binary, byteorder='big', signed=False)
    
        self.sock.sendto(segment, self.address_TX)
    
        timer_start = threading.Timer(TIME_TO_WAIT, lambda : self.sock.sendto(segment, self.address_TX), args=None, kwargs=None)
        timer_start.start()
    
        window.ConsoleAppendText('A fost trimis pachetul de start, astept confirmarea primirii...',1)
    
        data, addr = self.sock.recvfrom(BUFFER_SIZE) # functie blocanta
    
        timer_start.cancel()
    
        ack_binary = bytearray([data[i] for i in range(4)])
        segment_number_received = int.from_bytes(ack_binary, byteorder='big', signed=False)
        if segment_number_received == (segment_number_sent + 1):
            window.ConsoleAppendText('Am primit ack pentru pachetul de START\n',0)
            # s-a creat fisierul la destinatie, pot incepe popularea acestuia cu informatii
    
            # creez thread pentru primirea confirmarilor pachetelor
            TX_RX_thread = threading.Thread(target=self.TX_RX_fun, args=(window,))
            TX_RX_thread.start()
    
            # creez thread pentru trimiterea pachetelor
            TX_TX_thread = threading.Thread(target=self.TX_TX_fun, args=(window,))
            TX_TX_thread.start()
    
            # astept ca cele 2 threaduri sa-si fi terminat executia
            TX_RX_thread.join()
            TX_TX_thread.join()
            self.last_ack_of_file_final = self.last_ack_of_file
        else:
            window.ConsoleAppendText('Am primit ack gresit pentru pachetul de START !\nReincercati conexiunea\n',0)
