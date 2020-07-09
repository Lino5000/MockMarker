import tkinter as tk
from PIL import Image, ImageTk
import os.path as path


# Multiple subprograms needed to make DisplayQuestion work.
def clearWindow(window):
    # Get all the elements in the window and destroy them
    for widget in window.winfo_children():
        widget.destroy()


# Need to keep a reference to the image so that it doesn't get forgotten by Python's Garbage Collection.
imgtk = None
origImg = None
scaleFactor = 1


def zoom(canvas, direction):
    global imgtk, origImg, scaleFactor
    # Callback for zooming
    width, height = origImg.size
    if direction > 0:
        scaleFactor *= 1.2
        img = origImg.resize((int(width * scaleFactor), int(height * scaleFactor)), Image.ANTIALIAS)
    elif direction < 0:
        scaleFactor *= 0.8
        img = origImg.resize((int(width * scaleFactor), int(height * scaleFactor)), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(img)
    canvImg = canvas.find_all()[0]
    canvas.itemconfig(canvImg, image=imgtk)
    canvas.configure(scrollregion=canvas.bbox(tk.ALL))


def loadImage(imageName, parent, window):
    global imgtk, origImg
    WIDTH = window.winfo_screenwidth()
    HEIGHT = window.winfo_screenheight()
    # Loads the image called imageName from the Images Folder, and puts it in a tkinter compatible object.
    p = path.abspath("./Teacher/Images/" + imageName)  # TODO: Update Path
    origImg = Image.open(p)
    imgtk = ImageTk.PhotoImage(origImg)

    # Make the Frame to provide scroll bars and zooming.
    frame = tk.Frame(parent)
    # Canvas to hold the image
    canv = tk.Canvas(frame)
    canv.config(width=int(0.9 * WIDTH), height=int(0.7 * HEIGHT))
    canv.config(highlightthickness=0)
    # Add scroll bars
    scrollV = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canv.yview)
    scrollH = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canv.xview)
    canv.config(yscrollcommand=scrollV.set)
    canv.config(xscrollcommand=scrollH.set)

    scrollV.grid(row=0, rowspan=2, column=4, sticky='ns')
    scrollH.grid(row=1, column=0, columnspan=4, sticky='ew')
    canv.grid(row=0, column=0, columnspan=4, sticky='nsew')

    # Set up scrollable region
    width, height = origImg.size
    canv.config(scrollregion=(0, 0, width, height))

    # Add the image to the canvas
    canv.create_image(0, 0, anchor='nw', image=imgtk)

    # Add the Zoom buttons
    zoomInButton = tk.Button(frame, text='+', font=(None, 20), command=(lambda: zoom(canv, 1)))
    zoomInButton.grid(row=2, column=1, padx=10, pady=5, sticky='e')
    zoomOutButton = tk.Button(frame, text='-', font=(None, 20), command=(lambda: zoom(canv, -1)))
    zoomOutButton.grid(row=2, column=2, padx=10, pady=5, sticky='w')

    # Bind the mouse wheel to the scroll
    # TODO: Change to //120 for Windows
    window.bind_all("<MouseWheel>", (lambda e: canv.yview_scroll(-1 * (e.delta // 1), "units")))

    return frame


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
    popup.title("Warning")
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
    HEIGHT = window.winfo_screenheight()
    clearWindow(window)
    window.title("MockMarker - Question: " + question.Code)
    alignmentFrame = tk.Frame(window)
    imagePresent = False
    contBoolean = True
    if question.Img is not None:
        try:
            questionImage = loadImage(question.Img, alignmentFrame, window)
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
            questionImage.grid(row=1, column=0, columnspan=2, pady=5)

        if question.Desc is not None:
            descLabel = tk.Label(alignmentFrame, text=question.Desc, font=(None, 18))
            descLabel.grid(row=2, column=0, columnspan=2, pady=5)

        doneButton = tk.Button(alignmentFrame, text="Done", font=(None, 20), command=done)
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
