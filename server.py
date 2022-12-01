import json
import socket
import select
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

def message_user(handle, message):
    pass

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
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to address and IP
UDPServerSocket.bind((udp_host, udp_port))
UDPServerSocket.listen()

print(f"UDP server up and listening on {udp_host}:{udp_port}")

socket_list = [UDPServerSocket]
clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recvfrom(bufferSize)

        if not len(message_header):
            return False

        message = message_header.decode('UTF-8').strip()

        # Object containing header and msg data
        return {'header':message_header, 'data': client_socket.recv(len(message))}

    except:
        # Violent connection close. Can simply be closing the client or socket.close()
        return False

# Listen for incoming datagrams
while (True):
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for notified_socket in read_sockets:

        if notified_socket == UDPServerSocket:
            client_socket, client_addr = UDPServerSocket.accept()

            user = receive_message(client_socket)

            # Go to next socket due to lack of header
            if user is False:
                continue

            socket_list.append(client_socket)

            clients[client_socket] = user

            client_port = user['data'].decode('utf-8')

            print(f'Accepted new connection from {client_addr}:{client_port}')
        
        else:
            message = receive_message(notified_socket)

            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                socket_list.remove(notified_socket)

                del clients[notified_socket]

                continue
            
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for client_socket in clients:

                if client_socket != notified_socket:

                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        socket_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]

    # bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    # message = bytesAddressPair[0].decode('UTF-8')
    # address = bytesAddressPair[1]

    # client_msg = "Message from Client:{}".format(message)
    # client_ip = "Client IP Address:{}".format(address)

    # print(client_msg)
    # print(client_ip)


    # msgFromServer = read_command(message, address)
    # bytesToSend = str.encode(msgFromServer, 'UTF-8')

    #print("Message from server: "+msgFromServer)
    # Sending a reply to client
    # UDPServerSocket.sendto(bytesToSend, address)
