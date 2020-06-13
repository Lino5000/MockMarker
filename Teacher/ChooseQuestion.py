import tkinter as tk
import time


def clearWindow(window):
    for widget in window.winfo_children():  # Get all the elements in the window and destroy them
        widget.destroy()


def ChooseQuestion(questions, window):
    # TODO: Stub
    clearWindow(window)
    label = tk.Label(window, text="Choosing Question")  # Create a Label
    label.pack()  # Add the label the window - just puts it directly underneath the last element
    window.update()  # Let the window know there's something new for it to deal with
    print("continuing in 2 sec")
    end = time.time() + 2
    while time.time() < end:
        window.update()  # This is needed to keep the window responsive while waiting
    return questions[0]
