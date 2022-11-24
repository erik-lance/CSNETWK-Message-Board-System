import socket

def test_server():

    localIP = "127.0.0.1"
    localPort = 20001
    bufferSize = 1024

    msgFromServer = "Hello UDP Client"
    bytesToSend = str.encode(msgFromServer)

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and IP
    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")

    # Listen for incoming datagrams
    while (True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        client_msg = "Message from Clinet:{}".format(message)
        client_ip = "Client IP Address:{}".format(address)

        print(client_msg)
        print(client_ip)

        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)

test_server()