import tkinter as tk



def open_main_window():
    window = tk.Tk()
    window.title("Message Board System")
    window.geometry("500x500")

    label = tk.Label(text="Hello, Tkinter", background="#34A2FE")
    label.pack()

    entry = tk.Entry(fg="yellow", bg="blue", width=50)
    entry.pack()

    button = tk.Button(
        text="Click me!",
        width=25,
        height=5,
        bg="blue",
        fg="yellow",
    )
    button.pack()


    window.mainloop()