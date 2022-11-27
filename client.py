#import model as server
import view as view
import socket

# view.open_window()





serverAddressPort   = (socket.gethostname(), 12345)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

udp_host = socket.gethostname()
udp_port = 12345

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)

print("UDP Target IP:", udp_host)
print("UDP Target port:", udp_port)


# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# msgFromServer = UDPClientSocket.recvfrom(bufferSize)
# msg = "Message from Server {}".format(msgFromServer[0])

#print(msg)
