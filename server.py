import socket

bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

udp_host = socket.gethostname()
udp_port = 12345

# Bind to address and IP
UDPServerSocket.bind((udp_host, udp_port))

print("UDP server up and listening")

# Listen for incoming datagrams
while (True):
    print('hi')
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    print('reach')
    client_msg = "Message from Client:{}".format(message)
    client_ip = "Client IP Address:{}".format(address)

    print(client_msg)
    print(client_ip)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
