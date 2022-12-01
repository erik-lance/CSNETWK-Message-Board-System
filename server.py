import json
import socket
import threading
import queue
import model as model

WELCOME_MSG = "Connection to the Message Board Server is successful!"
LEAVE_MSG = "Connection closed. Thank you!"


ERROR_REG = "Error: Registration failed. Handle or alias already exists."

msg_chat = queue.Queue()
private_msg = queue.Queue()
error_msg = queue.Queue()
broadcast_msg = queue.Queue()
system_msg = queue.Queue()
# Contains tuples of  IP address, user, and 
users = []

clients = []
handles = []


# Commands:
# join, leave, register, all, msg, error

def add_user(address, handle=None):
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
        users.append((address, handle))
    
    return msg

def read_command(cmd, addr):
    """ Parses the JSON input and executes command

    Args:
        cmd  (JSON):         Command to parse
        addr (_RetAddress):  A tuple containing the user's IP and port.

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

def parse_system_cmd():
    while True:
        try:
            while not system_msg.empty():
                message, address = system_msg.get()
                print("SYS: "+message.decode('UTF-8'))

                msg_dict = json.loads(message)

                
                if msg_dict['command'] == 'join':
                    bytesToSend = str.encode(WELCOME_MSG, 'UTF-8')
                    UDPServerSocket.sendto(bytesToSend, address)
                    clients.append(address)
                elif msg_dict['command'] == 'leave':
                    bytesToSend = str.encode(LEAVE_MSG, 'UTF-8')
                    UDPServerSocket.sendto(bytesToSend, address)
                    clients.remove(address)
                #elif msg_dict['command'] == 'register':

        except:
            pass


# Server information
bufferSize = model.get_buffer_size()
udp_host = model.get_udp_host()
udp_port = model.get_udp_port()

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and IP
UDPServerSocket.bind((udp_host, udp_port))

print(f"UDP server up and listening on {udp_host}:{udp_port}")

def receiver():
    while True:
        try:
            message, address = UDPServerSocket.recvfrom(bufferSize)

            client_msg = "Message from Client:{}".format(message)
            client_ip = "Client IP Address:{}".format(address)

            print(client_msg)
            print(client_ip)

            system_msg.put((message,address))
        except:
            pass

# def broadcast():
#     while True:
#         while not broadcast_msg.empty():
#             message, address = broadcast_msg.get()
#             print("BROADCAST: "+message.decode('utf-8'))

#             # Add new client address
#             if address not in clients:
#                 clients.append(address)

#             # Broadcast message to all clients
#             for client in clients:
#                 try:

#                     if message.decode('utf-8').startswith("/"):
#                         name = message.decode('utf-8')[message.decode('utf-8').index(":")+1:]
#                         UDPServerSocket.sendto(read_command(message,), client)
#                     else:
#                         UDPServerSocket.sendto(message, client)
#                 except:
#                     clients.remove(client)

t1 = threading.Thread(target=receiver)
t2 = threading.Thread(target=parse_system_cmd)
# t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()


# # Listen for incoming datagrams
# while (True):
#     pass
#     # msgFromServer = read_command(message, address)
#     # bytesToSend = str.encode(msgFromServer, 'UTF-8')

#     #print("Message from server: "+msgFromServer)
#     # Sending a reply to client
#     # UDPServerSocket.sendto(bytesToSend, address)
