size = 512

#impachetarea primului segment care va contine numele si extensia
def encode_start(data):
#    ack = b'\x00\x00\x00\x00'
#   startCode = b'\x00\x01'
    ack = 0x00_00_00_00
    segment_code = 0x_00_00_00_01
    segment = bytes(ack, segment_code)
    return segment

#impachetarea unui segment din interiorul fisierului
def encode_data(data):
    pass


#impachetarea ulitmului segment
#in campul de segment_code, al doilea octet va fi lungimea caracterelor utile
def encode_end(data):

    pass


def encode_error(data):
    pass


segment_type = {
        'START': encode_start,
        'DATA': encode_data,
        'END': encode_end
    }


def encode(tip, data):
    return segment_type.get(tip, encode_error)(data)  # un fel de switch


#citirea fisier ca pachete de octeti
def bytes_from_file(filename, chunk_size=(size - 6)):
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
        if len(b) == (size - 6):
            yield encode('DATA', b)
        else:
            yield encode('END', b)
