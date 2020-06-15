import tkinter as tk
from PIL import Image, ImageTk
import os.path as path


def clearWindow(window):
    # Get all the elements in the window and destroy them
    for widget in window.winfo_children():
        widget.destroy()


def loadImage(imageName):
    # Loads the image called imageName from the Images Folder, and puts it in a tkinter compatible object.
    p = path.abspath("./Teacher/Images/" + imageName)
    return ImageTk.PhotoImage(Image.open(p))


def displayPopup(type):
    # TODO: Stub
    print("popup")
    return True


showing = True


def done():
    # Callback to close the window
    global showing
    showing = False


def DisplayQuestion(question, window):
    global showing
    clearWindow(window)
    imagePresent = False
    contBoolean = True
    if question.Img is not None:
        try:
            questionImage = loadImage(question.Img)
            imagePresent = True
        except FileNotFoundError:
            contBoolean = displayPopup(0)
    else:
        contBoolean = displayPopup(1)

    if contBoolean:
        codeLabel = tk.Label(window, text=question.Code)
        codeLabel.grid(row=0, column=1, sticky='ne', padx=10, pady=15)

        if imagePresent:
            imageLabel = tk.Label(window, image=questionImage)
            imageLabel.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        if question.Desc is not None:
            descLabel = tk.Label(window, text=question.Desc)
            descLabel.grid(row=2, column=0, columnspan=2, pady=5)

        doneButton = tk.Button(window, text="Done", command=done)
        doneButton.grid(row=3, column=0, columnspan=2, pady=5)

        showing = True
        while showing:
            window.update()
