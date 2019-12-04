DEFAULT_SIZE = 512
ack = 0
tip = 0
len = 0
data = 0

def SegmentDecode(segment):
    global ack
    global tip
    global len
    global data

    arr        = bytearray(segment)
    ack_binary = bytearray([arr[i] for i in range(4)])
    tip_binary = bytearray([arr[4]])
    len_binary = bytearray([arr[i] for i in (5,6)])

    ack  = int.from_bytes(ack_binary,byteorder='big',signed=False)
    tip  = int.from_bytes(tip_binary,byteorder='big',signed=False)
    len  = int.from_bytes(len_binary,byteorder='big',signed=False)
    data = bytearray([arr[i] for i in range(7,7 + len) if arr[i] != ord('0')])

    return {'ack' : ack, 'tip' : tip, 'len' : len,'data' : data}


def DataFieldDecode(data,length):
    date = ''
    for i in range(length):
        date += chr(data[i])
    return date


def FileNameDecode(filename,length):
    return 'output_' + DataFieldDecode(filename,length)

