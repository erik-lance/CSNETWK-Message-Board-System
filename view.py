import tkinter as tk
import client as client_app

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
 
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class GUI:

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Message Board System")
        # window.geometry("500x500")
        app = client_app
        app.set_gui(self)


        def send():
            """
                Sends to client the written text inside entry for it to send to server.
            """
            app.send_server(e.get())
            print("MESSAGE SENT")
            e.delete(0, tk.END)

        
        label1= tk.Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
        row=0)

        self.text_board = tk.Text(self.window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
        self.text_board.grid(row=1, column=0, columnspan=2)

        scrollbar = tk.Scrollbar(self.text_board)
        scrollbar.place(relheight=1, relx=0.974)

        e = tk.Entry(self.window, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
        e.grid(row=2, column=0)
    
        send = tk.Button(self.window, text="Send", font=FONT_BOLD, bg=BG_GRAY,
                command=send).grid(row=2, column=1)

        self.window.mainloop()
    
    def post(self, message):
        """Accessed by client object. Upon retrieval of message, tells view to post chat to board.

        Args:
            message (str): Message string to post to board.
        """
        print('RECEIVED CLIENT MSG')
        print(message)
        print("\n")

        self.text_board.insert(tk.END, "\n" + message)

GUI()