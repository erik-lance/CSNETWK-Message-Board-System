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

def find_handle(address):
    found_handle = None 
    
    for user in users:
        if user[0] == address:
            found_handle = user[1]
            break
    
    return found_handle

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
    elif cmd_dict['command'] == 'leave': msg = "Connection closed. Thank you!"


    return msg;

def parse_system_cmd():
    while True:
        try:
            while not system_msg.empty():
                message, address = system_msg.get()
                print("SYS: "+message.decode('UTF-8'))

                msg_dict = json.loads(message)
                ret_msg = {'command':'None'}
                
                if msg_dict['command'] == 'join':
                    ret_msg['command'] = 'join'
                    ret_msg = json.dumps(ret_msg)

                    bytesToSend = str.encode(ret_msg, 'UTF-8')
                    UDPServerSocket.sendto(bytesToSend, address)
                    clients.append(address)

                elif msg_dict['command'] == 'leave':
                    ret_msg['command'] = 'leave'
                    ret_msg = json.dumps(ret_msg)

                    bytesToSend = str.encode(ret_msg, 'UTF-8')
                    UDPServerSocket.sendto(bytesToSend, address)
                    clients.remove(address)
                    # Do we remove the handle upon leave? take note! 
                elif msg_dict['command'] == 'register':
                    
                    handle = msg_dict['handle']

                    if handle not in handles:
                        ret_msg['command'] = 'register'
                        ret_msg = json.dumps(ret_msg)

                        new_user = (address, handle)
                        # Give handle to address 
                        users.append(new_user)
                        handles.append(handle)
                        
                        bytesToSend = str.encode(ret_msg, 'UTF-8')
                        UDPServerSocket.sendto(bytesToSend, address)
                        
                    else:
                        ret_msg['command'] = 'error'
                        ret_msg['message'] = 'Registration failed. Handle or alias already exists.'
                        ret_msg = json.dumps(ret_msg)

                        bytesToSend = str.encode(LEAVE_MSG, 'UTF-8')
                        UDPServerSocket.sendto(bytesToSend, address)
                elif msg_dict['command'] == 'all':
                    ret_msg['command'] == 'all'

                    user_handle = find_handle(address)
                    handled_msg = "{handle}: {message}".format(user_handle, msg_dict['message'])
                
                    ret_msg['message'] = handled_msg
                    ret_msg = json.dumps(ret_msg)

                    # The handled message now contains the handle to broadcast
                    bytesToSend = str.encode(LEAVE_MSG, 'UTF-8')
                    for client in clients:
                        UDPServerSocket.sendto(bytesToSend, client)

                elif msg_dict['command'] == 'msg':
                    ret_msg['command'] = 'msg'
                    ret_msg['message'] = msg_dict['message']
                    ret_msg['handle'] = find_handle(address)
                    ret_msg = json.dumps(ret_msg)

                    dest_address = msg_dict['handle']

                    bytesToSend = str.encode(LEAVE_MSG, 'UTF-8')
                    UDPServerSocket.sendto(bytesToSend, dest_address)
                     
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
