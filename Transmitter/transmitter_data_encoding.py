DEFAULT_SIZE = 512

class DataEncoding:
    @staticmethod
    def segment_decode(segment):
        arr        = bytearray(segment)
        ack_binary = bytearray([arr[i] for i in range(4)])
        tip_binary = bytearray([arr[4]])
        len_binary = bytearray([arr[i] for i in (5,6)])

        ack = int.from_bytes(ack_binary, byteorder='big', signed=False)
        tip = int.from_bytes(tip_binary, byteorder='big', signed=False)
        length = int.from_bytes(len_binary, byteorder='big', signed=False)
        data = bytearray([arr[i] for i in range(7, 7 + length) if arr[i] != b'\x00'])

        return {'ack': ack, 'tip': tip, 'len': length, 'data': data}


    # codificare: (segment_number, segment_type, segment_len), segment_data
    # creeaza primul pachet, cel care contine numele
    @staticmethod
    def encode_start(transmitter,nume_fisier):
        transmitter.ack = transmitter.ack + 1  # primul ack trimis este 1
        segment_number = transmitter.ack.to_bytes(4, byteorder='big', signed=False)

        segment_type = b'\x01'
        lungime_nume = len(nume_fisier)
        segment_len = lungime_nume.to_bytes(2, byteorder='big', signed=False)
        segment = segment_number + segment_type + segment_len

        for ch in nume_fisier:
            segment += (ord(ch).to_bytes(1, byteorder='big', signed=False))

        return segment


    # creeaza pachetele care contine bitii din fisier
    @staticmethod
    def encode_data(transmitter,segment_data):
        transmitter.ack = transmitter.ack + 1  # primul ack trimis este 1
        segment_number = transmitter.ack.to_bytes(4, byteorder='big', signed=False)

        segment_type = b'\x02'
        segment_len = DEFAULT_SIZE.to_bytes(2, byteorder='big', signed=False)
        segment = segment_number + segment_type + segment_len + segment_data

        return segment

    # in campul de segment_code, al doilea octet va fi lungimea caracterelor utile
    @staticmethod
    def encode_end(transmitter,segment_data):
        global end_transmission
        transmitter.ack = transmitter.ack + 1  # primul ack trimis este 1
        segment_number = transmitter.ack.to_bytes(4, byteorder='big', signed=False)

        segment_type = b'\x03'
        segment_data_len = len(segment_data)
        segment_data = segment_data + b'\x00'*(DEFAULT_SIZE - segment_data_len)
        segment_len = segment_data_len.to_bytes(2, byteorder='big', signed=False)
        segment = segment_number + segment_type + segment_len + segment_data

        return segment

    @staticmethod
    def encode_error(transmitter,segment_data):
        pass


    @staticmethod
    def encode(transmitter,tip, data):
        segment_type = {
            'START': DataEncoding.encode_start,
            'DATA' : DataEncoding.encode_data,
            'END'  : DataEncoding.encode_end
        }
        return segment_type.get(tip, DataEncoding.encode_error)(transmitter,data)


    #citirea fisier ca pachete de octeti
    @staticmethod
    def bytes_from_file(transmitter, chunk_size=DEFAULT_SIZE):
        with open(transmitter.filepath, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    break

    #codificarea pachetelor de octeti
    @staticmethod
    def encode_bytes(transmitter):
        for b in DataEncoding.bytes_from_file(transmitter.filepath):
            if len(b) == DEFAULT_SIZE:
                yield DataEncoding.encode(transmitter,'DATA', b)
            else:
                yield DataEncoding.encode(transmitter,'END', b)


