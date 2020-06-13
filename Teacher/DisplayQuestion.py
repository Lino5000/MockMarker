import tkinter as tk
import time


def clearWindow(window):
    for widget in window.winfo_children():  # Get all the elements in the window and destroy them
        widget.destroy()


def DisplayQuestion(question, window):
    # TODO: Stub
    clearWindow(window)  # Create a Label
    label = tk.Label(window,
                     text=question)  # Add the label to the window - just puts it directly underneath the last element
    label.pack()  # Let the window know there's something new for it to deal with
    window.update()
    print("continuing in 2 sec")
    end = time.time() + 2
    while time.time() < end:
        window.update()  # This is needed to keep the window responsive while waiting
