# from tkinter import *
import tkinter as tk
import client as client_app

BG_GRAY = "#ABB2B9"
BG_COLOR = "#3E2C41"
TEXT_COLOR = "#EAECEE"

DARK_CLR = "#140E18"
PURPLE = "#5C527F"
BOARD_CLR = "#3E2C41"

FONT = ("Arial", 15 * -1)
# HANDLE = ("Arial Bold", 15 * -1)
FONT_BOLD = ("Arial Bold", 15 * -1)

H1 = ("Arial Bold", 20 * -1)
H3 = "Arial 10 bold"
SEND_BTN = "Arial 16 bold"

class GUI:

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Message Board Server")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.configure(bg = "#FFFFFF")
        app = client_app
        app.set_gui(self)


        def send():
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

        header_frame = tk.Frame(bg=DARK_CLR)
        header_frame.place(x=0, y=0, width=500, height=90)
        header_label1 = tk.Label(header_frame, bg=DARK_CLR,fg=TEXT_COLOR, text = "The Best Message Board Server", font=H1).place(x=97, y=18)
        header_label2 = tk.Label(header_frame, bg=PURPLE,fg=TEXT_COLOR, text = "Connected to 127.0.0.1:12345", font=("Arial Bold", 12 * -1), padx=4, pady=6,  anchor="w").place(x=9, y=52, width=482.0, height=31.0)

        self.text_frame = tk.Frame(bg=BOARD_CLR)
        self.text_frame.place(x=0, y=90, width=500.0, height=456.0)
        # scrollbar = tk.Scrollbar(self.text_frame)
        # scrollbar.place(relheight=1, relx=0.964)
        myscrollbar=tk.Scrollbar(self.text_frame,orient="vertical")
        myscrollbar.pack(side="right",fill="y")

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

        '''
        canvas.create_rectangle(0.0, 0.0, 500.0, 90.0, fill=DARK_CLR, outline="")
        canvas.create_text(
            97.0,
            18.0,
            anchor="nw",
            text="The Best Message Board Server",
            fill="#FFFFFF",
            font=("Arial Bold", 20 * -1)
        )
        canvas.create_rectangle(
            9.0,
            52.0,
            491.0,
            83.0,
            fill="#5C527F",
            outline="")

        canvas.create_text(
            16.0,
            60.0,
            anchor="nw",
            text="Connected to 127.0.0.1:12345",
            fill="#FFFFFF",
            font=("Arial Bold", 12 * -1)
        )
        '''

        # canvas.create_rectangle(
        #     0.0,
        #     90.0,
        #     485.0,
        #     546.0,
        #     fill="#261C2C",
        #     outline="")


        '''
        self.text_canvas = tk.Canvas(
            canvas,
            bg = "#261C2C",
            height = 456.0,
            width = 500.0,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.text_canvas.place(x=0, y=90)
        '''

        # scrollbar = tk.Scrollbar(self.text_canvas)
        # scrollbar.place(relheight=1, relx=0.964)

        '''
        self.text_board = tk.Text(self.text_canvas, bg=BG_COLOR, fg=TEXT_COLOR, width=50, font=FONT, wrap=tk.WORD)
        self.text_board.place(height = 456.0,x=0,y=0)
        # self.text_board.configure(state="disabled")
        self.text_board.insert(tk.END, "Hi")
        scrollbar = tk.Scrollbar(self.text_board)
        scrollbar.place(relheight=1, relx=0.974)'''

        '''
        entry_canvas = tk.Canvas(canvas,
            bg=DARK_CLR,
            height =54.0,
            width = 416.0,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        entry_canvas.place(x=0, y=546)
        '''
        '''
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

        send = tk.Button(canvas, text="Send", font=SEND_BTN,
            bg=DARK_CLR,
            fg="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            activebackground="#3E2C41",
            command=send,
            relief="flat")
        send.place(x=416, y=546, width=84.0 ,height=54.0)
        '''

        # button_1 = tk.Button(
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: print("button_1 clicked"),
        #     relief="flat"
        # )
        # button_1.place(
        #     x=416.0,
        #     y=546.0,
        #     width=84.0,
        #     height=54.0
        # )

        # header_label1 = tk.Label(header_frame, bg=DARK_CLR,fg=TEXT_COLOR, text = "The Best Message Board Server", font=H1, height=1).place(x=97, y=18)
        #TODO: CHANGE TEXT TO BE UPDATABLE
        # header_label2 = tk.Label(canvas, bg=PURPLE,fg=TEXT_COLOR, text = "Connected to 127.0.0.1:12345", font=H3, padx=4, pady=6, width=59).place(x=9, y=52)
        # header_text = tk.Text(header_frame, bg=PURPLE, fg=TEXT_COLOR, font=H1, width=482, height=31)

        # self.text_board = tk.Text(self.window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=10).place(x=0, y=90)


        # label1= tk.Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
        # row=0)
        #
        # self.text_board = tk.Text(self.window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
        # self.text_board.grid(row=1, column=0, columnspan=2)
        #
        # scrollbar = tk.Scrollbar(self.text_board)
        # scrollbar.place(relheight=1, relx=0.974)
        #
        # e = tk.Entry(self.window, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
        # e.grid(row=2, column=0)
        #
        # send = tk.Button(self.window, text="Send", font=FONT_BOLD, bg=BG_GRAY,
        #         command=send).grid(row=2, column=1)
        #
        # # frame = Frame(width=100, height=100, bg="red", colormap="new")
        # # frame.grid(sticky ='wn', row = 1, column = 0)
        #
        # self.text_board.tag_config('user', background="yellow", foreground="red")

        self.window.mainloop()

    def add_text(self, message, cmd):
        if (cmd == "error"):
            color = "#F13030"
        else:
            color="#30F189"
        new_label = tk.Label(self.text_frame, bg=BOARD_CLR, fg=color, text = message, font=FONT_BOLD, wraplength=400, padx=10, pady=15).pack()

    def post(self, message, cmd):
        """Accessed by client object. Upon retrieval of message, tells view to post chat to board.

        Args:
            message (str): Message string to post to board.
        """
        print('RECEIVED CLIENT MSG')
        self.curr_msg = message
        print(self.curr_msg)
        print("\n")

        if (cmd == "msg" or cmd == "all"):
            msg_list = self.edit_text(self.curr_msg)
            # self.text_board.insert(tk.END, "\n" + msg_list[0], user)
            # self.text_board.insert(tk.END, "\n" + msg_list[1])
            # new_msg = ("\n").join(msg_list)

        else:
            new_msg = message
            self.add_text(message, cmd)
            # self.text_board.insert(tk.END, "\n" + new_msg)
            # self.text_canvas.create_text(
            #     87.0,
            #     512.0,
            #     anchor="nw",
            #     text=new_msg,
            #     fill="#F03030",
            #     font=("Arial BoldMT", 15 * -1)
            # )

        # self.insert_msg(new_msg)




    # def insert_msg(self, new_msg):
    #     # frame = Frame(width=100, height=100, bg="red", colormap="new")
    #     # frame.grid(sticky ='wn', row = 1, column = 0)
    #     self.text_board.insert(tk.END, "\n" + new_msg)

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
