# from tkinter import *
import tkinter as tk
import client as client_app

BG_GRAY = "#ABB2B9"
BG_COLOR = "#261C2C"
TEXT_COLOR = "#EAECEE"

DARK_CLR = "#140E18"
PURPLE = "#5C527F"
BOARD_CLR = "#3E2C41"

FONT = ("Arial", 15 * -1)
FONT_BOLD = ("Arial Bold", 15 * -1)

H1 = ("Arial Bold", 20 * -1)
H3 = "Arial 10 bold"
SEND_BTN = "Arial 16 bold"

MSG_CMD = "#3E2C41"
ALL_CMD = DARK_CLR

handle = None

class GUI:

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Message Board Server")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.configure(bg = "#FFFFFF")
        app = client_app
        app.set_gui(self)

        self.host = app.get_host()
        self.port = app.get_port()


        def send():
            # self.text_board.configure(state="normal")
            """
                Sends to client the written text inside entry for it to send to server.
            """
            app.send_server(e.get("1.0",'end-1c'))
            print("MESSAGE SENT")
            e.delete('1.0', tk.END)

        '''canvas = tk.Canvas(
            self.window,
            bg = "#FFFFFF",
            height = 600,
            width = 500,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.grid()'''

        self.header_frame = tk.Frame(bg=DARK_CLR)
        self.header_frame.place(x=0, y=0, width=500, height=90)
        header_label1 = tk.Label(self.header_frame, bg=DARK_CLR,fg=TEXT_COLOR, text = "Message Board Server", font=H1).place(x=142, y=18)
        self.header_label2 = tk.Label(self.header_frame, bg=PURPLE,fg=TEXT_COLOR, text = "Join the Server!", font=("Arial Bold", 12 * -1), padx=4, pady=6,  anchor="center").place(x=9, y=52, width=482.0, height=31.0)
        self.text_board = tk.Text(self.window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.text_board.place(x=0, y=90, width=500.0, height=456.0)
        self.text_board.tag_config("error", foreground="#F13030")
        self.text_board.tag_config("success", foreground="#30F189")
        self.text_board.tag_config("you", foreground="#EECD58", font=FONT_BOLD)
        self.text_board.tag_config("else", font=FONT_BOLD)
        self.text_board.config(spacing3=10)

        scrollbar = tk.Scrollbar(self.text_board)
        scrollbar.place(relheight=1, relx=0.974)

        e = tk.Text(
            bd=0,
            bg="#3E2C41",
            fg="#FFFFFF",
            font = FONT,
            highlightthickness=4,
            relief = "flat",
            highlightbackground = DARK_CLR,
            highlightcolor = DARK_CLR,
            padx= 3,
            pady = 6
        )
        e.place(
            x=0.0,
            y=546.0,
            width=417.0,
            height=54.0
        )

        send = tk.Button(self.window, text="Send", font=SEND_BTN,
            bg=DARK_CLR,
            fg="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            activebackground="#3E2C41",
            command=send,
            relief="flat")
        send.place(x=416, y=546, width=84.0 ,height=54.0)

        self.window.mainloop()

    def add_text(self, message, cmd):
        if (cmd == "error"):
            color = "#F13030"
        else:
            color="#30F189"
        new_label = tk.Label(self.text_frame, bg=BOARD_CLR, fg=color, text = message, font=FONT_BOLD, wraplength=400, padx=10, pady=15).pack()


    def add_message(self, handle, message, cmd):
        if(cmd == "msg"):
            print("HERE")
            handle_label = tk.Label(self.text_frame, bg=BG_GRAY, fg=TEXT_COLOR, text = handle, font=FONT_BOLD, wraplength=400, padx=10, pady=5, anchor='w').pack(height = 52, width = 485)
            msg_label = tk.Label(self.text_frame, bg=BG_GRAY, fg=TEXT_COLOR, text = message, font=FONT, wraplength=400, padx=10, pady=5, anchor='w').pack()


    def post(self, message, cmd):
        """Accessed by client object. Upon retrieval of message, tells view to post chat to board.

        Args:
            message (str): Message string to post to board.
        """
        print('RECEIVED CLIENT MSG')
        self.curr_msg = message
        print(self.curr_msg)
        print(cmd)
        global handle

        if (cmd == "msg" or cmd == "all"):
            msg_list = self.edit_text(message)

            if (cmd == "all"):
                print(handle)
                print(msg_list[0])
                if (handle == msg_list[0]):
                    self.text_board.insert(tk.END, "\n" + msg_list[0] + ": ", 'you')
                else:
                    self.text_board.insert(tk.END, "\n" + msg_list[0] + ": ", 'else')
            else:
                print("HERE")
                if("To" in msg_list[0]):
                    print("CONTAINS")
                    name = msg_list[0].split("To ")
                    # if (handle == name[1]):
                    self.text_board.insert(tk.END, "\n" + msg_list[0] + ": ", 'you')
                else:
                    self.text_board.insert(tk.END, "\n" + msg_list[0] + ": ", 'else')

            self.text_board.insert(tk.END, msg_list[1])

        else:
            if (cmd== "error"):
                self.text_board.insert(tk.END, "\n" + message, 'error')

            else:
                if (cmd == "register"):
                    split = message.split("Welcome ")
                    name = split[1]
                    handle = name[:-1]
                self.text_board.insert(tk.END, "\n" + message, 'success')

    def edit_text (self, message):
        if (message[0] == "["):
            split = message.split(']')
            handle = split[0][1:]
            print(handle)
            content = split[1][1:].lstrip()
            print(content)
        else:
            split = message.split(':')
            handle = split[0]
            print(handle)
            content = split[1].lstrip()
            print(content)
        full_message = [handle, content]

        return full_message


GUI()
