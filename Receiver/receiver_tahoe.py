import random
from receiver_data_decoding import DataDecoding
from receiver_network_handler import *
DEFAULT_SIZE = 512


class ReceiverController:
    def __init__(self):
        self.ip = None
        self.port_RX = None
        self.port_TX = None
        self.address_TX = None
        self.address_RX = None
        self.loss_probability = None
        self.sock = None
        self.filepath = None
        self.networkHandler = NetworkHandler()


    def drop_packet(self,loss_probability):
        x = random.randrange(1000)
        if x < loss_probability:
            return True
        else:
            return False

    def tahoe_congestion_control(self,window,buffer_size):
        stay_in_loop = True
        ack_waited = 1
        while stay_in_loop:
            data, addr = self.sock.recvfrom(buffer_size)
            if self.drop_packet(self.loss_probability):
                window.ConsoleAppendText(f"A fost pierdut pachetul ... {DataDecoding.segment_decode(data)['ack']}")
            else:
                print('A fost receptionat ... {}'.format(data))
                decoded_data = DataDecoding.segment_decode(data)
                ack_received = decoded_data['ack']

                if ack_received == ack_waited:
                    if decoded_data['tip'] == 1:
                        window.ConsoleAppendText(f"A fost receptionat pachetul de start..")
                        file_name = DataDecoding.filename_decode(window,decoded_data['data'], decoded_data['len'])
                        file_write = open(file_name, 'wb')
                        window.ConsoleAppendText(f"Fisierul a fost creat cu succes..\n")
                    elif decoded_data['tip'] == 2:
                        file_write.write(decoded_data['data'])
                    elif decoded_data['tip'] == 3:
                        file_write.write(decoded_data['data'])
                        window.ConsoleAppendText(f"A fost receptionat pachetul final {decoded_data['ack']} ...")
                        file_write.close()

                    elif decoded_data['tip'] == 4:
                        stay_in_loop = False

                    ack_transmitted = ack_received + 1
                    ack_waited = ack_transmitted
                else:
                    ack_transmitted = ack_waited

                segment_number = ack_transmitted.to_bytes(4, byteorder='big', signed=False)
                self.sock.sendto(segment_number, self.address_TX)
                print('A fost trimis {}'.format(segment_number))

        time.sleep(1)
        window.ConsoleAppendText('Sfarsitul receptiei...')
