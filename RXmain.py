import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP
address_port = ("127.0.0.1", 5005)
buffer_size = 1024  # pachetul va contine 512B

sock.bind(address_port)


while True:
    data, addr = sock.recvfrom(buffer_size)
    print(data.decode("UTF-8") + " received from" + str(addr))



