import tkinter as tk
from PIL import Image, ImageTk
import os.path as path


# Multiple subprograms needed to make DisplayQuestion work.
def clearWindow(window):
    # Get all the elements in the window and destroy them
    for widget in window.winfo_children():
        widget.destroy()


def loadImage(imageName):
    # Loads the image called imageName from the Images Folder, and puts it in a tkinter compatible object.
    p = path.abspath("./Teacher/Images/" + imageName)
    img = Image.open(p)
    return ImageTk.PhotoImage(img)


# This section is related to the Popup for a missing Image.
popOpen = True
shouldContinue = True


def popCancel():
    global popOpen, shouldContinue
    popOpen = False
    shouldContinue = False


def popOk():
    global popOpen, shouldContinue
    popOpen = False
    shouldContinue = True


def displayPopup(Type):
    global popOpen, shouldContinue
    popup = tk.Tk()  # Make new window.
    popup.grid()
    popOpen = True

    if Type == 0:
        textLabel = tk.Label(popup, text="Warning:\nThe image for this question\ncould not be found.")
    elif Type == 1:
        textLabel = tk.Label(popup, text="Warning:\nThis question has no image attached.")
    else:
        textLabel = tk.Label(popup, "Sorry, something's gone wrong, and I don't know what.")
    textLabel.grid(column=0, row=0, columnspan=2, padx=10, pady=5)

    cancelButton = tk.Button(popup, text="Cancel", command=popCancel)
    cancelButton.grid(row=1, column=0, padx=90, pady=10)
    contButton = tk.Button(popup, text="Ok", command=popOk)
    contButton.grid(row=1, column=1, padx=90, pady=10)

    while popOpen:
        popup.update()

    popup.destroy()
    return shouldContinue


# The Following Section is the DisplayQuestion subprogram itself, which is called y the TeacherMain program.
showing = True


def done():
    # Callback to close the window
    global showing
    showing = False


def DisplayQuestion(question, window):
    global showing
    WIDTH = window.winfo_screenwidth()
    clearWindow(window)
    alignmentFrame = tk.Frame(window)
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
        codeLabel = tk.Label(alignmentFrame, text=question.Code)
        codeLabel.grid(row=0, column=1, sticky='ne', pady=15)

        if imagePresent:
            # PyCharm reckons questionImage may not be set, but it will because that's the way imagePresent gets set.
            imageLabel = tk.Label(alignmentFrame, image=questionImage)
            imageLabel.grid(row=1, column=0, columnspan=2, pady=5)

        if question.Desc is not None:
            descLabel = tk.Label(alignmentFrame, text=question.Desc)
            descLabel.grid(row=2, column=0, columnspan=2, pady=5)

        doneButton = tk.Button(alignmentFrame, text="Done", command=done)
        doneButton.grid(row=3, column=0, columnspan=2, pady=5)

        # Work out the width of the frame and move it to the center of the screen. Unfortunately causes the question
        # to appear briefly on screen before moving, but there is not enough time to fix it right now. This weird
        # process seems to be required because tkinter doesn't calculate the width of everything until it has been
        # displayed.
        alignmentFrame.grid(row=0, column=0)
        alignmentFrame.update()
        alignmentFrame.grid_forget()
        alignmentFrame.grid(row=0, column=0, padx=(WIDTH - alignmentFrame.winfo_width()) / 2)

        showing = True
        while showing:
            window.update()
