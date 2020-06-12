import tkinter as tk


class TeacherMain:
    def __init__(self):
        self.window = tk.Tk()  # Create the window
        self.window.after(0, self.loop)  # Start the custom loop
        self.window.mainloop()  # Start the library's window loop

    def loop(self):
        question = ChooseQuestion(self.window)
        DisplayQuestion(question, self.window)
        self.window.after(0, self.loop)  # Start the next cycle of the loop


def clearWindow(window):
    for widget in window.winfo_children():  # Get all the elements in the window and destroy them
        widget.destroy()


def ChooseQuestion(window):
    # Stub
    clearWindow(window)
    label = tk.Label(window, text="Choosing Question")
    label.pack()
    window.update()
    return input(': ')


def DisplayQuestion(question, window):
    # Stub
    clearWindow(window)
    label = tk.Label(window, text=question)
    label.pack()
    window.update()
    input()


if __name__ == "__main__":
    Main = TeacherMain()  # Creates new Instance of the Program and Runs it.
