import tkinter as tk


class TeacherMain:
    def __init__(self):
        self.window = tk.Tk()  # Create the window
        self.window.after(0, self.loop)  # Start the custom loop
        self.window.mainloop()  # Start the library's window loop - handles inputs and display

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
    label = tk.Label(window, text="Choosing Question")  # Create a Label
    label.pack()  # Add the label the window - just puts it directly underneath the last element
    window.update()  # Let the window know there's something new for it to deal with
    return input(': ')


def DisplayQuestion(question, window):
    # Stub
    clearWindow(window)  # Create a Label
    label = tk.Label(window,
                     text=question)  # Add the label the window - just puts it directly underneath the last element
    label.pack()  # Let the window know there's something new for it to deal with
    window.update()
    input()  # Wait for user rather than continuing immediately


if __name__ == "__main__":
    Main = TeacherMain()  # Creates new Instance of the Program and Runs it.
