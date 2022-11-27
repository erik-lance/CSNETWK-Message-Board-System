#import model as server
import model as model
import view as view
import socket

# view.open_window()

def write_message():
    print('Write a message: ')
    return str.encode(input())

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

bufferSize = model.get_buffer_size()
udp_host = model.get_udp_host()
udp_port = model.get_udp_port()

serverAddressPort = (udp_host, udp_port)

# msgFromClient       = "Hello UDP Server"
# bytesToSend         = str.encode(msgFromClient)

bytesToSend = write_message()

print("UDP Target IP:", udp_host)
print("UDP Target port:", udp_port)


# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# msgFromServer = UDPClientSocket.recvfrom(bufferSize)
# msg = "Message from Server {}".format(msgFromServer[0])

#print(msg)
