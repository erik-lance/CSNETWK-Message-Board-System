import socket

bufferSize = 1024

udp_host = socket.gethostname()
udp_port = 12345


def get_buffer_size(): return bufferSize
def get_udp_host(): return udp_host
def get_udp_port(): return udp_port