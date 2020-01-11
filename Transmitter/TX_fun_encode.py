DEFAULT_SIZE = 512
ack = 0     # primul segment_number trimis este 1
end_transmission = False

def segment_decode(segment):
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


def increment_ack():
    global ack
    ack = ack + 1


# codificare: (segment_number, segment_type, segment_len), segment_data
# creeaza primul pachet, cel care contine numele
def encode_start(nume_fisier):
    increment_ack()  # primul ack trimis este 1
    segment_number = ack.to_bytes(4, byteorder='big', signed=False)

    segment_type = b'\x01'

    lungime_nume = len(nume_fisier)
    segment_len = lungime_nume.to_bytes(2, byteorder='big', signed=False)

    segment = segment_number + segment_type + segment_len

    for ch in nume_fisier:
        segment += (ord(ch).to_bytes(1, byteorder='big', signed=False))

    return segment


# creeaza pachetele care contine bitii din fisier
def encode_data(segment_data):
    increment_ack()
    segment_number = ack.to_bytes(4, byteorder='big', signed=False)

    segment_type = b'\x02'

    segment_len = DEFAULT_SIZE.to_bytes(2, byteorder='big', signed=False)

    segment = segment_number + segment_type + segment_len + segment_data
    return segment



# in campul de segment_code, al doilea octet va fi lungimea caracterelor utile
def encode_end(segment_data):
    global end_transmission
    increment_ack()
    segment_number = ack.to_bytes(4, byteorder='big', signed=False)
    segment_type = b'\x03'
    segment_data_len = len(segment_data)
    segment_data = segment_data + b'\x00'*(DEFAULT_SIZE - segment_data_len)
    segment_len = segment_data_len.to_bytes(2, byteorder='big', signed=False)
    segment = segment_number + segment_type + segment_len + segment_data
  #  end_transmission = True
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
