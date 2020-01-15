'''
def pack_retransmit(sock,address_port):
    global segment_pipe
    global timers_queue
    global flag_retransmit
    global segments_in_pipe

    if(flag_retransmit == False):
        flag_retransmit = True
        while len(timers_queue) > 0:
            lock.acquire()
            timer = timers_queue.pop(0)
            lock.release()

            timer.cancel()

        segments_in_pipe = 0
        time.sleep(2)


        print('retransmit')
        first_loop = True
        print(f"intiail len = {len(segment_pipe)}")

        #segment_pipe = segment_pipe[1:] # nu se include primul deoarece este ultimul packet receptionat cu succes
        while len(segment_pipe) > 0:
            segment = segment_pipe.pop(0)
            print(f"while1 len = {len(segment_pipe)}")
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
            print(f'RTX: Am trimis pachetul cu segment_number = {segment_number}')
            #segment_pipe.append(segment)
            first_loop = False
            print(f"while2 len = {len(segment_pipe)}")
        flag_retransmit = False
        print('gata retransmisia')

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
    global retransmit_thread

    print("TX_read_ack thread started")

    number_ack_duplicate = 0
    last_ack_received += 1  # ack = 2 este pentru pachetul de start (are segment number = 1)
    # mai trebuie sa merg niste iteratii cand sending_done, abia am trimis pachetul end, nu am primit ack de la el
    while sending_done == False or (last_ack_received != last_ack_of_file + 1):
        data, addr = sock.recvfrom(DEFAULT_SIZE)  # functie blocanta
        ack_received = int.from_bytes(data, byteorder='big', signed=False)   # segment_number este fix data
        #print('last ack received=  {}...'.format(last_ack_received))
        #print('A fost receptionat segment_number = {}... \n'.format(ack_received))

        lock.acquire()
        segments_in_pipe = segments_in_pipe - 1
        lock.release()

        print(f"RX: ack received : last_ack_received {ack_received}  {last_ack_received}")
        if ack_received == last_ack_received + 1:  # am primit un ack bun
            last_ack_received += 1
            lock.acquire()
            timer = timers_queue.pop(0)
            lock.release()

            timer.cancel()
            if (flag_retransmit == False):
                segment = segment_pipe.pop(0)
                segment_number = segment_decode(segment)['ack']
                print(f'RX:Pop segment_number = {segment_number}')

            packet_received()

        else:   # am primit acelasi ack
            print('--RX: Ack primit este duplicat...')
            number_ack_duplicate = number_ack_duplicate + 1
            if 3 == number_ack_duplicate:
                print(f'--- 3 ack duplicate!!! flag_retransmit = {flag_retransmit}')
                number_ack_duplicate = 0
                if(flag_retransmit == False):
                    packet_dropped(sock, address_port)


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
    global retransmit_thread

    print(f"TX_send thread started sending_done = {sending_done}")
    while sending_done == False:
        for segment in encode_bytes(file_name_to_send):
            # daca pipe-ul e plin

            # de implementat: porneste un TIMER sa nu astepte la infinit

            while segments_in_pipe >= cwnd:
                print ("TX: pipeline is full")
                time.sleep(0.5)
           # while retransmit_thread.is_alive() == True:
            #    retransmit_thread.join()


                #time.sleep(0.5)
                #asteapta un ack
            # else
            #   increamenteaza contor si trimite

            tip = segment_decode(segment)['tip']
            if tip == 3:
                sending_done = True
                last_ack_of_file = segment_decode(segment)['ack']
                print(f'TX: last_ack_of_file = {last_ack_of_file }\n')

            lock.acquire()
            segments_in_pipe = segments_in_pipe + 1
            lock.release()

            # creez si pornesc timer

            while (flag_retransmit == True):
                print("TX: astept sa se termine retransmisia")
                time.sleep(0.5)

            timer = threading.Timer(TIME_TO_WAIT, lambda : packet_dropped(sock,address_port), args=None, kwargs=None)
            timer.start()

            lock.acquire()
            timers_queue.append(timer)
            lock.release()

            segment_pipe.append(segment)
            sock.sendto(segment, address_port)

            segment_number = segment_decode(segment)['ack']
            print(f'TX:Sent segment_number = {segment_number}')



            # adaug timerul in coada de timere

'''