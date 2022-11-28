import json
import model as model
import socket

BUFFER_SIZE = 1024
COMMANDS = ['join', 'leave', 'register', 'all', 'message', '?']

class Client:
    bufferSize = model.get_buffer_size()
    udp_host = model.get_udp_host()
    udp_port = model.get_udp_port()

    def __init__(self) -> None:
        # Create a UDP socket at client side
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        


    def connect_server(self, host, port):
        self.udp_host = host
        self.udp_port = port


        msgFromServer = self.UDPClientSocket.recvfrom(BUFFER_SIZE)

    def parse_message(self, message):
        """Parses the message to JSON for reading for the server

        Args:
            message str: The message of the client to be parsed

        Returns:
            JSON: Contains a command field, and a message field and/or handle field.
            err: Output message to be posted into GUI if there is.
        """
        err = None

        # Splits the string based on parameters
        msg = message[1:].split(" ")
        msg_dict = {'command':'None', 'handle':'None', 'message':'None'}

        if msg[0] == COMMANDS[0] and len(msg) == 3:
            # /join <server_ip_add> <port>
            msg_dict['command'] = 'join'

        
        elif msg[0] == COMMANDS[1] and len(msg) == 1:
            # /leave
            msg_dict['command'] = 'leave'

        elif msg[0] == COMMANDS[2] and len(msg) == 2:
            # /register <handle>
            msg_dict['command'] = 'register'
            msg_dict['handle'] = msg[1]

        elif msg[0] ==  COMMANDS[3] and len(msg) == 2:
            # /all <messsage>
            msg_dict['command'] = 'all'
            msg_dict['message'] = msg[1]
        
        elif msg[0] == COMMANDS[4] and len(msg) == 3:
            # /msg <handle> <message>
            msg_dict['command'] = 'msg'
            msg_dict['handle'] = msg[1]
            msg_dict['message'] = msg[2]
        
        elif msg[0] == COMMANDS[5] and len(msg) == 1:
            # /?
            pass
        elif msg[0] not in COMMANDS:
            err = self.get_error(4)
        else:
            err = self.get_error(5)


        msg_json = json.dumps(msg_dict)
        parsed = "test"

        return (parsed, err)

    def send_server(self, message):
        msg, err = self.parse_message(message)

        if err == None:
            serverAddressPort = (self.udp_host, self.udp_port)
            


            self.UDPClientSocket.sendto(bytes, serverAddressPort)
            return self.UDPClientSocket.recvfrom(BUFFER_SIZE)
        else:
            return err


    def write_message():
        print('Write a message: ', end='')
        return str.encode(input())

    def get_error(self, code):
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


    def get_host(self) -> str: self.return udp_host
    def get_port(self) -> str: self.return udp_port

    def set_host(self, host): self.udp_host = host
    def set_port(self, port): self.udp_port = port

    

    # msgFromClient       = "Hello UDP Server"
    # bytesToSend         = str.encode(msgFromClient)

    bytesToSend = write_message()

    print("UDP Target IP:", udp_host)
    print("UDP Target port:", udp_port)


    # Send to server using created UDP socket
    

    # msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    # msg = "Message from Server {}".format(msgFromServer[0])

    #print(msg)
