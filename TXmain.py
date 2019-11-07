import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP
address_port = ("127.0.0.1", 5002)


sock.sendto("Mesaj trimis", address_port)

