import model as server
import view as view
import socket

# view.open_window()



def user_input():
    """_summary_

    Returns:
        _type_: _description_
    """
    return input()

def test_client():
    msgFromClient       = "Hello UDP Server"

    bytesToSend         = str.encode(msgFromClient)
    serverAddressPort   = ("127.0.0.1", 20001)
    bufferSize          = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])

    print(msg)

test_client()