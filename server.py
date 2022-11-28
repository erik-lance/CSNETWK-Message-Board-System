import json
import socket
import model as model

handles = []

# Contains tuples of  IP address, user, and 
users = []

# Commands:
# join, leave, register, all, msg, error

def add_user(addr, handle=None):
    msg = ""

    if handle != None:
        if handle not in handles:
            # Give handle to address 
            users[users.index((address,None))] = (address,handle)
            handles.append(handle)
            msg = "Welcome "+handle+"!"
        else:
            msg = "Error: Registration failed. Handle or alias already exists."
    else:
        users.append((addr, handle))
    
    return msg


def read_command(cmd, addr):
    """ Parses the JSON input and executes command

    Args:
        cmd  (JSON):         Command to parse
        addr (_RetAddress): A tuple containing the user's IP and port.

    Returns:
        str: Server reply
    """
    cmd_dict = json.loads(cmd)
    msg = ""

    if cmd_dict['command'] == 'join':  
        msg = "Connection to the Message Board Server is successful!"
        add_user(addr)
    elif cmd_dict['command'] == 'leave': msg = "Connection closed. Thank you!"
    elif cmd_dict['command'] == 'register':
        # No handle checking yet
        msg = add_user(addr, cmd_dict['handle'])


    return msg;

# Server information
bufferSize = model.get_buffer_size()
udp_host = model.get_udp_host()
udp_port = model.get_udp_port()



# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Bind to address and IP
UDPServerSocket.bind((udp_host, udp_port))

print("UDP server up and listening")

# Listen for incoming datagrams
while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode('UTF-8')
    address = bytesAddressPair[1]

    client_msg = "Message from Client:{}".format(message)
    client_ip = "Client IP Address:{}".format(address)

    print(client_msg)
    print(client_ip)


    msgFromServer = read_command(message, address)
    bytesToSend = str.encode(msgFromServer, 'UTF-8')

    #print("Message from server: "+msgFromServer)
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
