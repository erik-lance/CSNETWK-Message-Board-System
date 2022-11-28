import tkinter as tk
import client

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
 
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"



def open_main_window():
    window = tk.Tk()
    window.title("Message Board System")
    # window.geometry("500x500")

    def send():
        send = "You -> " + e.get()
        text_board.insert(tk.END, "\n" + send)
    
        user = e.get().lower()
    
        if (user == "hello"):
            text_board.insert(tk.END, "\n" + "Bot -> Hi there, how can I help?")
    
        elif (user == "hi" or user == "hii" or user == "hiiii"):
            text_board.insert(tk.END, "\n" + "Bot -> Hi there, what can I do for you?")
    
        elif (user == "how are you"):
            text_board.insert(tk.END, "\n" + "Bot -> fine! and you")
    
        elif (user == "fine" or user == "i am good" or user == "i am doing good"):
            text_board.insert(tk.END, "\n" + "Bot -> Great! how can I help you.")
    
        elif (user == "thanks" or user == "thank you" or user == "now its my time"):
            text_board.insert(tk.END, "\n" + "Bot -> My pleasure !")
    
        elif (user == "what do you sell" or user == "what kinds of items are there" or user == "have you something"):
            text_board.insert(tk.END, "\n" + "Bot -> We have coffee and tea")
    
        elif (user == "tell me a joke" or user == "tell me something funny" or user == "crack a funny line"):
            text_board.insert(
                tk.END, "\n" + "Bot -> What did the buffalo say when his son left for college? Bison.! ")
    
        elif (user == "goodbye" or user == "see you later" or user == "see yaa"):
            text_board.insert(tk.END, "\n" + "Bot -> Have a nice day!")
    
        else:
            text_board.insert(tk.END, "\n" + "Bot -> Sorry! I didn't understand that")
    
        e.delete(0, tk.END)
    # label = tk.Label(text="Hello, Tkinter", background="#34A2FE")
    # label.pack()

    # entry = tk.Entry(fg="yellow", bg="blue", width=50)
    # entry.pack()

    # button = tk.Button(
    #     text="Click me!",
    #     width=25,
    #     height=5,
    #     bg="blue",
    #     fg="yellow",
    # )
    # button.pack()


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

open_main_window()