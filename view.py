import tkinter as tk
import client as client_app

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
 
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class GUI:

    def __init__(self) -> None:
        window = tk.Tk()
        window.title("Message Board System")
        # window.geometry("500x500")
        app = client_app
        app.set_gui(self)

        def send():
            send =  str(app.send_server(e.get()))

            print(send)

            text_board.insert(tk.END, "\n" + send)
        
        
            e.delete(0, tk.END)

        def post(message):
            """Accessed by client object. Upon retrieval of message, tells view to post chat to board.

            Args:
                message (str): Message string to post to board.
            """
            print(send)

            text_board.insert(tk.END, "\n" + send)

        label1= tk.Label(window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
        row=0)

        text_board = tk.Text(window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
        text_board.grid(row=1, column=0, columnspan=2)

        scrollbar = tk.Scrollbar(text_board)
        scrollbar.place(relheight=1, relx=0.974)

        e = tk.Entry(window, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
        e.grid(row=2, column=0)
    
        send = tk.Button(window, text="Send", font=FONT_BOLD, bg=BG_GRAY,
                command=send).grid(row=2, column=1)

        window.mainloop()

GUI()