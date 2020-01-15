import random
import time
from threading import RLock

DEFAULT_SIZE = 512
ack = 0
tip = 0
length = 0
data = 0
order_buffer = []
segments_buffer = [[0,0]] * 20
firstdynamic = 0
filepath = ""
console_lock = RLock()

def segment_decode(segment):
    global ack
    global tip
    global length
    global data

    arr        = bytearray(segment)
    ack_binary = bytearray([arr[i] for i in range(4)])
    tip_binary = bytearray([arr[4]])
    len_binary = bytearray([arr[i] for i in (5, 6)])

    ack = int.from_bytes(ack_binary, byteorder='big', signed=False)
    tip = int.from_bytes(tip_binary, byteorder='big', signed=False)
    length = int.from_bytes(len_binary, byteorder='big', signed=False)
    data = bytearray([arr[i] for i in range(7, 7 + length) if arr[i] != b'\x00'])

    return {'ack': ack, 'tip': tip, 'len': length, 'data': data}


def DataFieldDecode(data, length):
    date = ''
    for i in range(length):
        date += chr(data[i])
    return date


def FileNameDecode(window,filename, length):
    global filepath
    filename = DataFieldDecode(filename,length)
    filename = filename[filename.rfind("/")+1:]
    return window.SELECTFILE_TEXT.toPlainText() + "//" + filename


# functie de ordonare dinamica a pachetelor
'''
def SegmentsOrdering(segment):
    global segments_buffer
    global flag
    global firstdynamic
    global order_buffer


    ack = int(segment['ack'])
    data = segment['data']
    if not order_buffer:
        order_buffer.append([ack,data])
    else:
        if ack == order_buffer[-1][0] + 1:
            order_buffer.append([ack,data])
            segments_buffer[segments_buffer[-1][0]-1] = [ack,data]
        elif firstdynamic == 0:
            segments_buffer = [[0,0]] * (ack - order_buffer[-1][0] - 1)
            segments_buffer.insert(0,order_buffer[-1])
            segments_buffer.insert(ack-order_buffer[-1][0],[ack,data])
            firstdynamic = 1
        else:
            if ack > segments_buffer[0][0] and ack < segments_buffer[-1][0]:
                segments_buffer[ack-segments_buffer[-1][0]-1] = [ack,data]
            elif ack > segments_buffer[-1][0]:
                for i in range(ack - segments_buffer[-1][0] - 1):
                    segments_buffer.append([0,0])
                segments_buffer.append([ack,data])
        buffer = []
        for value in segments_buffer:
            if value != [0,0]:
                buffer.append(value)
            else:
                break
        if len(buffer) > 1:
            for element in buffer:
                if element not in order_buffer:
                    order_buffer.append(element)
                segments_buffer.remove(element)
'''
def ConsoleAppendText(window,text):
    console_lock.acquire()
    window.CONSOLE.append(text + "\n")
    window.CONSOLE.update()
    console_lock.release()
    time.sleep(0.05)


def drop_packet(loss_probability):
    x = random.randrange(1000)
    if x < loss_probability:
        return True
    else:
        return False

def tahoe_congestion_control(window,sock, address_port, buffer_size, loss_probability):
    stay_in_loop = True
    ack_waited = 1
    while stay_in_loop:
        data, addr = sock.recvfrom(buffer_size)
        if drop_packet(loss_probability):
            ConsoleAppendText(window,f"A fost pierdut pachetul ... {segment_decode(data)['ack']}")
        else:
            #print('A fost receptionat ... {}'.format(data))
            decoded_data = segment_decode(data)
            ack_received = decoded_data['ack']

            if ack_received == ack_waited:
                if decoded_data['tip'] == 1:
                    ConsoleAppendText(window,f"A fost receptionat pachetul de start..")
                    file_name = FileNameDecode(window,decoded_data['data'], decoded_data['len'])
                    file_write = open(file_name, 'wb')
                    ConsoleAppendText(window,f"Fisierul a fost creat cu succes..\n")
                elif decoded_data['tip'] == 2:
                    file_write.write(decoded_data['data'])
                elif decoded_data['tip'] == 3:
                    file_write.write(decoded_data['data'])
                    ConsoleAppendText(window,f"A fost receptionat pachetul final {decoded_data['ack']} ...")
                    file_write.close()

                elif decoded_data['tip'] == 4:
                    stay_in_loop = False

                ack_transmitted = ack_received + 1
                ack_waited = ack_transmitted
            else:
                ack_transmitted = ack_waited

            segment_number = ack_transmitted.to_bytes(4, byteorder='big', signed=False)
            sock.sendto(segment_number, address_port)
            #print('A fost trimis {}'.format(segment_number))
        # time.sleep(0.2)

        # in while, end of if
    time.sleep(1)
    ConsoleAppendText(window,'Sfarsitul receptiei...')
