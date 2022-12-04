import json
import model as model
import socket
import threading

BUFFER_SIZE = 1024
COMMANDS = ['join', 'leave', 'register', 'all', 'message', '?']

WELCOME_MSG = "Connection to the Message Board Server is successful!"
LEAVE_MSG = "Connection closed. Thank you!"
ERROR_REG = "Error: Registration failed. Handle or alias already exists."

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

    if msg[0] == COMMANDS[0] and len(msg) == 3:
        # /join <server_ip_add> <port>
        msg_dict['command'] = 'join'
        udp_host = msg[1]
        udp_port = int(msg[2])
        curr_cmd = COMMANDS[0]
    
    elif msg[0] == COMMANDS[1] and len(msg) == 1:
        # /leave
        msg_dict['command'] = 'leave'
        curr_cmd = COMMANDS[1]

    elif msg[0] == COMMANDS[2] and len(msg) == 2:
        # /register <handle>
        msg_dict['command'] = 'register'
        msg_dict['handle'] = msg[1]
        curr_cmd = COMMANDS[2]

    elif msg[0] ==  COMMANDS[3] and len(msg) == 2:
        # /all <messsage>
        msg_dict['command'] = 'all'
        msg_dict['message'] = msg[1]
        curr_cmd = COMMANDS[3]
    
    elif msg[0] == COMMANDS[4] and len(msg) == 3:
        # /msg <handle> <message>
        msg_dict['command'] = 'msg'
        msg_dict['handle'] = msg[1]
        msg_dict['message'] = msg[2]
        curr_cmd = COMMANDS[4]
    
    elif msg[0] == COMMANDS[5] and len(msg) == 1:
        # /?
        err = HELP
    elif msg[0] not in COMMANDS:
        err = get_error(4)
    else:
        err = get_error(5)

    print("ERR RECEIVED: " + str(err))
    msg_json = json.dumps(msg_dict)

    return (msg_json, err)

def handle_adder(message):
    if message['command'] == COMMANDS[3]:
        # /all
        if message['handle'] != None:
            return "{handle}: {msg}".format(message['handle'], message['message'])
        else:
            return message['message']
    
    elif message['command'] == COMMANDS[4]:
        # /msg
        return "[From {handle}]: {msg}".format(message['handle'], message['message'])

def send_server(message):
    msg, err = parse_message(message)

    global udp_host
    global udp_port
    global curr_cmd
    global gui

    if err == None:
        serverAddressPort = (udp_host, udp_port)
        bytesToSend = str.encode(msg, 'UTF-8')

        print("UDP Target IP:", udp_host)
        print("UDP Target port:", udp_port)

        

        try:
            UDPClientSocket.settimeout(5)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            
            if curr_cmd == COMMANDS[4]:
                # /msg
                msg_dict = json.dumps(msg)
                gui.post("[To {handle}]: {msg}".format(msg_dict['handle'], msg_dict['message']))
       
        except Exception as e:
            print("Timeout raised and caught.")
            print(e)
            if curr_cmd == COMMANDS[0]:
                gui.post("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            elif curr_cmd == COMMANDS[1]:
                gui.post("Error: Disconnection failed. Please connect to the server first.")
            else:
                gui.post("Error: Unknown error.")
            UDPClientSocket.close()

    else:
        gui.post(err)

def get_error(code):
    """Gets the error message based on code

    Args:
        code (int): Code number to get the error

    Returns:
        str: Error message to be posted
    """

    error = "Error: "

    if code == 4:
        return error+"Command not found."
    elif code == 5:
        return error+"Command parameters do not match or is not allowed."


def get_host() -> str: return udp_host
def get_port() -> int: return udp_port

def set_host(host): udp_host = host
def set_port(port): udp_port = port

def set_gui(g) : 
    global gui
    gui= g

def receiver():
    global udp_host
    global udp_port
    global gui

    while True:
        try:
            message, _ = UDPClientSocket.recvfrom(BUFFER_SIZE)
            print("RECEIVED SERVER: ")

            decoded_msg = json.loads(message)
            print(decoded_msg)
            print("Server message received!")

            # Leave after send/rcv
            # shouldn't be affected by receiving messages after /leave, curr_cmd is a one-time thing
            if decoded_msg['command'] == COMMANDS[0] and curr_cmd == COMMANDS[0]:
                gui.post(WELCOME_MSG) 
            elif decoded_msg['command'] == COMMANDS[1] and curr_cmd == COMMANDS[1]:
                udp_host = None
                udp_port = None
                gui.post(LEAVE_MSG)

            # If command is ALL / MSG / ? / error
            if decoded_msg['command'] == COMMANDS[3]:
                gui.post(decoded_msg['message'])
            elif decoded_msg['command'] == COMMANDS[4]:
                rcv_msg = "[From {handle}]: {message}".format(decoded_msg['handle'], decoded_msg['message'])
                gui.post(rcv_msg)
            
            if decoded_msg['command'] == COMMANDS[6]:
                gui.post(decoded_msg['error'])
                pass
           
        except:
            pass

# Separate thread for receiving from server
t1 = threading.Thread(target=receiver)
t1.start()