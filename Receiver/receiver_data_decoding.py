class DataDecoding:
    @staticmethod
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

    @staticmethod
    def data_field_decode(data, length):
        date = ''
        for i in range(length):
            date += chr(data[i])
        return date

    @staticmethod
    def filename_decode(window,filename, length):
        global filepath
        filename = DataDecoding.data_field_decode(filename,length)
        filename = filename[filename.rfind("/")+1:]
        return window.SELECTFILE_TEXT.toPlainText() + "//" + filename