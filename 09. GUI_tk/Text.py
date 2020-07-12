from tkinter import Tk, Label, Button, Message

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.msg = Message(master, text='text')
        self.msg.pack()

    def greet(self):
        print("Greetings!")

def pt(event):
    print(event)

root = Tk()
root.bind('<Control-c>', pt)
my_gui = MyFirstGUI(root)
root.mainloop()