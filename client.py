import json
import model as model
import socket
import threading

BUFFER_SIZE = 1024
COMMANDS = ['join', 'leave', 'register', 'all', 'msg', '?', 'error', 'ch']

WELCOME_MSG = "Connection to the Message Board Server is successful!"
LEAVE_MSG = "Connection closed. Thank you!"

HELP = ''' 
    List of commands:\n
    /join <server_ip_address> <port> \n
    /leave \n
    /register <handle> \n
    /all <message> \n
    /msg <handle> <message> \n
    /? 
'''

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_host = None
udp_port = None
curr_cmd = None
gui = None

connected = False
sending_msg = None
cur_handle = None

def parse_message(message):
    """Parses the message to JSON for reading for the server

    Args:
        message str: The message of the client to be parsed

    Returns:
        JSON: Contains a command field, and a message field and/or handle field.
        err: Output message to be posted into GUI if there is.
    """
    err = None
    
    global udp_host
    global udp_port
    global curr_cmd

    # Splits the string based on parameters
    msg = message[1:].split(" ")
    msg_dict = {'command':'None'}

    if msg[0] == COMMANDS[0] and len(msg) == 3 and udp_host == None:
        # /join <server_ip_add> <port>
        msg_dict['command'] = 'join'
        udp_host = msg[1]
        try:
            udp_port = int(msg[2])
        except:
            udp_host = None
            udp_port = None
            err = get_error(0)
        curr_cmd = COMMANDS[0]
    
    elif msg[0] == COMMANDS[1] and len(msg) == 1 and udp_host != None:
        # /leave
        msg_dict['command'] = 'leave'
        curr_cmd = COMMANDS[1]

    elif msg[0] == COMMANDS[2] and len(msg) == 2 and udp_host != None and cur_handle == None:
        # /register <handle>
        msg_dict['command'] = 'register'
        msg_dict['handle'] = msg[1]
        curr_cmd = COMMANDS[2]

    elif msg[0] == COMMANDS[3] and len(msg) >= 2 and udp_host != None:
        # /all <messsage>
        msg_dict['command'] = 'all'
        msg_dict['message'] = ' '.join(msg[1:])
        curr_cmd = COMMANDS[3]
    
    elif msg[0] == COMMANDS[4] and len(msg) >= 3 and udp_host != None:
        # /msg <handle> <message>
        msg_dict['command'] = 'msg'
        msg_dict['handle'] = msg[1]
        msg_dict['message'] = ' '.join(msg[2:])
        curr_cmd = COMMANDS[4]
    
    elif msg[0] == COMMANDS[5] and len(msg) == 1:
        # /?
        err = HELP
    elif msg[0] not in COMMANDS:
        err = get_error(4)
    elif msg[0] == COMMANDS[0] and udp_host != None:
        err = get_error(1)
    elif msg[0] == COMMANDS[1] and udp_host == None:
        err = get_error(2)
    elif msg[0] in COMMANDS[2:] and udp_host == None:
        err = get_error(3)
    elif msg[0] == COMMANDS[2] and cur_handle != None:
        err = get_error(6)
    else:
        err = get_error(5)

    msg_json = json.dumps(msg_dict)

    return (msg_json, err)

def handle_adder(message):
    if message['command'] == COMMANDS[3]:
        # /all
        if message['handle'] != None:
            return "{handle}: {msg}".format(handle=message['handle'], msg=message['message'])
        else:
            return message['message']
    
    elif message['command'] == COMMANDS[4]:
        # /msg
        return "[From {handle}]: {msg}".format(handle=message['handle'], msg=message['message'])

def connect_server(bytesToSend, serverAddressPort):
    global connected
    global udp_host
    global udp_port

    if not connected:
        try:
            UDPClientSocket.settimeout(5)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            print("Sending to a server...")
            message, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
            connected = True

            print("RECEIVED SERVER CONNECTION")
            decoded_msg = json.loads(message.decode())
            print(decoded_msg)
            print("\n")
            
            UDPClientSocket.settimeout(None)
            if decoded_msg['command'] == COMMANDS[0]: 
                gui.post(WELCOME_MSG, 'join') 
            else:
                gui.post("Error: Unexpected incorrect receive upon joining.", 'error')
        except Exception as e:
            print("Timeout on connecting raised and caught.")
            print(e)
            gui.post("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", 'error')
            udp_host = None
            udp_port = None
            # UDPClientSocket.close()
    else:
        gui.post("Error: Already connected to {host}:{port}".format(host=udp_host, port=udp_port), 'error')

def send_server(message):
    msg, err = parse_message(message)
    
    global connected
    global udp_host
    global udp_port
    global curr_cmd
    global gui

    global sending_msg
    if err == None:
        serverAddressPort = (udp_host, udp_port)
        bytesToSend = str.encode(msg)

        print("UDP Target IP:", udp_host)
        print("UDP Target port:", udp_port)

        if curr_cmd == COMMANDS[0]:
            connect_server(bytesToSend, serverAddressPort)
        else:
            try:
                UDPClientSocket.settimeout(5)
                UDPClientSocket.sendto(bytesToSend, serverAddressPort)

                UDPClientSocket.settimeout(None)
                if curr_cmd == COMMANDS[4]:
                    print('I am sending out a message.')
                    # /msg
                    msg_dict = json.loads(msg)
                    
                    
                    sending_msg = "[To {handle}]: {msg}".format(handle=msg_dict['handle'], msg=msg_dict['message']);
                    print(sending_msg)

            except Exception as e:
                print("Timeout raised and caught.")
                print(e)
                if curr_cmd == COMMANDS[0]:
                    gui.post("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", 'error')
                elif curr_cmd == COMMANDS[1]:
                    gui.post("Error: Disconnection failed. Please connect to the server first.", 'error')
                else:
                    gui.post("Error: Unknown error.", 'error')
                UDPClientSocket.close()

    else:
        gui.post(err, 'error')

def get_error(code):
    """Gets the error message based on code

    Args:
        code (int): Code number to get the error

    Returns:
        str: Error message to be posted
    """

    error = "Error: "

    if code == 1:
        global udp_host
        global udp_port
        return error+"Already connected to {host}:{port}".format(host=udp_host, port=udp_port)
    elif code == 2:
        return error+"Disconnection failed. Please connect to the server first."
    elif code == 3:
        return error+"You need to connect to a server first."
    elif code == 4:
        return error+"Command not found."
    elif code == 5:
        return error+"Command parameters do not match or is not allowed."
    elif code == 6:
        return error+"You already have a registered handle."

def get_handle() -> str:
    global cur_handle
    return cur_handle

def get_host() -> str: 
    global udp_host
    return udp_host
def get_port() -> int: 
    global udp_port
    return udp_port

def set_host(host): udp_host = host
def set_port(port): udp_port = port

def set_gui(g) : 
    global gui
    gui= g

def receiver():
    global udp_host
    global udp_port
    global curr_cmd
    global gui

    global sending_msg
    global cur_handle
    global connected
    while True:
        try:
            if connected:
                message, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
                print("RECEIVED SERVER")
                decoded_msg = json.loads(message.decode())
                print(decoded_msg)
                print("\n")

                if decoded_msg['command'] == COMMANDS[1] and curr_cmd == COMMANDS[1]:
                    udp_host = None
                    udp_port = None
                    gui.post(LEAVE_MSG, 'leave')
                    cur_handle = None
                    connected = False

                elif decoded_msg['command'] == COMMANDS[2] and curr_cmd == COMMANDS[2]:
                    handle_msg = "Welcome "+str(decoded_msg['handle'])+"!"
                    gui.post(handle_msg, 'register')
                    
                    cur_handle = decoded_msg['handle']
                # If command is ALL / MSG / ? / error
                elif decoded_msg['command'] == COMMANDS[3]:
                    gui.post(decoded_msg['message'], 'all')
                elif decoded_msg['command'] == COMMANDS[4]:
                    if sending_msg != None:
                        gui.post(sending_msg, 'msg')
                        sending_msg = None
                    if decoded_msg['handle'] != cur_handle:
                        rcv_msg = "[From {handle}]: {message}".format(handle=str(decoded_msg['handle']), message=str(decoded_msg['message']))
                        gui.post(rcv_msg, 'msg')
                
                elif decoded_msg['command'] == COMMANDS[6]:
                    print("Error received from server!")
                    gui.post(decoded_msg['message'], 'error')
                                
        except Exception as e:
            # This will spam if you print exceptions.
            if e != WindowsError.winerror:
                pass
                #print(e)
                

# Separate thread for receiving from server
t1 = threading.Thread(target=receiver)
t1.start()