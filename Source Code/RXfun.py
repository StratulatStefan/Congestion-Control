DEFAULT_SIZE = 512
ack = 0
tip = 0
length = 0
data = 0

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


def tahoe_congestion_control(sock, address_port, buffer_size):
    global lock
    ack_waited = 1
    while True:
        data, addr = sock.recvfrom(buffer_size)
        decoded_data = SegmentDecode(data)
        if decoded_data['tip'] == 1:
            print('A fost generat pachetul de start..')

            file_name = FileNameDecode(decoded_data['data'], decoded_data['len'])
            print('Numele fisierului : ', file_name)

            file_write = open(file_name, 'wb')
            print('Fisierul a fost creat cu succes..')
            ack_waited = decoded_data['ack']   #Consider ca primul pachet venit e sigur bun
        elif decoded_data['tip'] == 2:
            # print('A fost receptionat un pachet de date...')
            file_write.write(decoded_data['data'])
            # print('Fisierul a fost modificat')
        elif decoded_data['tip'] == 3:
            print('\n\nReceptia a luat sfarsit deoarece a fost transmit pachetul final...')
            file_write.write(decoded_data['data'])
            break


        ack_received = decoded_data['ack']

        if ack_received == ack_waited:
            ack_transmitted = ack_received + 1
            ack_waited = ack_transmitted
        else:
            ack_transmitted = ack_waited
        segment_number = ack_transmitted.to_bytes(4, byteorder='big', signed=False)
        sock.sendto(segment_number, address_port)

