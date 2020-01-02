import time
DEFAULT_SIZE = 512
ack = 0
tip = 0
length = 0
data = 0
order_buffer = []
segments_buffer = [[0,0]] * 20
firstdynamic = 0

def SegmentDecode(segment):
    global ack
    global tip
    global length
    global data

    arr        = bytearray(segment)
    ack_binary = bytearray([arr[i] for i in range(4)])
    tip_binary = bytearray([arr[4]])
    len_binary = bytearray([arr[i] for i in (5,6)])

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


def FileNameDecode(filename, length):
    return "output//" + DataFieldDecode(filename, length)[len('input//'):]


def SegmentsOrdering(segment):
    global segments_buffer
    global flag
    global firstdynamic
    global order_buffer


    ack = int(segment['ack'])
    data = segment['data']
    if not order_buffer:
        print('gol')
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

def tahoe_congestion_control(sock, address_port, buffer_size):
    global lock
    global flag
    global firstdynamic
    global order_buffer
    global segments_buffer

    ack_waited = 1
    while True:
        data, addr = sock.recvfrom(buffer_size)
        print('A fost receptionat..{}'.format(data))
        decoded_data = SegmentDecode(data)
        if decoded_data['tip'] == 1:
            print('A fost receptionat pachetul de start..')
            file_name = FileNameDecode(decoded_data['data'], decoded_data['len'])
            file_write = open(file_name, 'wb')
            print('Fisierul a fost creat cu succes..\n\n')
            ack_waited = decoded_data['ack']   #Consider ca primul pachet venit e sigur bun
        elif decoded_data['tip'] == 2:
            SegmentsOrdering(decoded_data)
            print('A fost receptionat un pachet de date {}...'.format(decoded_data['ack']))
            if len(order_buffer) == 20:
                for element in order_buffer:
                    file_write.write(element[1])
                order_buffer = []
        elif decoded_data['tip'] == 3:
            print('\n\nA fost receptionat pachetul final {} ...'.format(decoded_data['ack']))
            file_write.write(decoded_data['data'])
            break

        ack_received = decoded_data['ack']

        if ack_received == ack_waited:
            ack_transmitted = ack_received + 1
            ack_waited = ack_transmitted
        else:
            ack_transmitted = ack_waited
        segment_number = ack_transmitted.to_bytes(4, byteorder='big', signed=False)
        time.sleep(3)
        sock.sendto(segment_number,address_port)
        print('A fost trimis {}'.format(segment_number))

    file_write.close()
