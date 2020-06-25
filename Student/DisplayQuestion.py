import math
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from MarkResponse import MarkResponse


def clearWindow(window):
    # Get all the elements in the window and destroy them
    for widget in window.winfo_children():
        widget.destroy()


def MakeStrengthMeter(strength, window):
    rectWidth = 20
    rectHeight = 20
    offset = 3  # Canvas Element has weird coordinates, need an offset so the border is visible.

    meterCanvas = tk.Canvas(
        window,
        width=rectWidth * 4 + offset,
        height=rectHeight * 4 + offset,
        bg='white',
        highlightthickness=0
    )

    if strength >= 0.25:
        colour1 = 'red'
    else:
        colour1 = 'grey'
    meterCanvas.create_rectangle(
        offset, rectHeight * 3 + offset, rectWidth + offset, rectHeight * 4 + offset, fill=colour1
    )

    if strength >= 0.5:
        colour2 = 'orange'
    else:
        colour2 = 'grey'
    meterCanvas.create_rectangle(
        rectWidth + offset, rectHeight * 2 + offset, rectWidth * 2 + offset, rectHeight * 4 + offset, fill=colour2
    )

    if strength >= 0.75:
        colour3 = 'yellow'
    else:
        colour3 = 'grey'
    meterCanvas.create_rectangle(
        rectWidth * 2 + offset, rectHeight + offset, rectWidth * 3 + offset, rectHeight * 4 + offset, fill=colour3
    )

    if strength >= 1:
        colour4 = 'green'
    else:
        colour4 = 'grey'
    meterCanvas.create_rectangle(
        rectWidth * 3 + offset, offset, rectWidth * 4 + offset, rectHeight * 4 + offset, fill=colour4
    )

    return meterCanvas


answering = True


def startMarking():
    global answering
    answering = False


showing = True


def closeMarks():
    global showing
    showing = False


def DisplayQuestion(question, window):
    global answering, showing
    answering = True
    clearWindow(window)
    window.title("Answering " + question.Code)

    alignmentFrame = tk.Frame(window)
    alignmentFrame.config(bg='white')

    # Step 1: Take input
    codeLabel = tk.Label(alignmentFrame, text=question.Code, bg='white')
    codeLabel.grid(row=0, column=1, padx=5, pady=5, sticky='ne')

    bandLabel = tk.Label(alignmentFrame, text="Overall Band:", bg='white')
    bandLabel.grid(row=1, column=0, columnspan=2, padx=10, pady=2)
    bandDropDownValue = tk.StringVar(alignmentFrame, "Choose a Band")
    bandDropDown = tk.OptionMenu(alignmentFrame, bandDropDownValue, "1-2", "3-4", "5-6")
    bandDropDown.grid(row=2, column=0, columnspan=2, padx=20, pady=3)

    posLabel = tk.Label(alignmentFrame, text="Good Points:", bg='white')
    posLabel.grid(row=3, column=0, columnspan=2, padx=10, pady=2)
    posTextBorder = tk.Frame(alignmentFrame, bg='black')
    posTextBox = ScrolledText(posTextBorder, height=8, width=100, wrap=tk.WORD, bd=0, bg='light grey')
    posTextBox.grid(row=0, column=0, padx=3, pady=3)
    posTextBorder.grid(row=4, column=0, columnspan=2, padx=10, pady=3)

    negLabel = tk.Label(alignmentFrame, text="Poor Points:", bg='white')
    negLabel.grid(row=5, column=0, columnspan=2, padx=10, pady=2)
    negTextBorder = tk.Frame(alignmentFrame, bg='black')
    negTextBox = ScrolledText(negTextBorder, height=8, width=100, wrap=tk.WORD, bd=0, bg='light grey')
    negTextBox.grid(row=0, column=0, padx=3, pady=3)
    negTextBorder.grid(row=6, column=0, columnspan=2, padx=10, pady=3)

    markButton = tk.Button(alignmentFrame, text="Mark", command=startMarking)
    markButton.grid(row=7, column=0, columnspan=2, padx=30, pady=5)

    # Handle the alignment
    # Work out the width of the frame and move it to the center of the screen. Unfortunately causes the question
    # to appear briefly on screen before moving, but there is not enough time to fix it right now. This weird
    # process seems to be required because tkinter doesn't calculate the width of everything until it has been
    # displayed.
    alignmentFrame.grid(row=0, column=0)
    alignmentFrame.update()
    alignmentFrame.grid_forget()
    alignmentFrame.grid(
        row=0,
        column=0,
        padx=(window.winfo_width() - alignmentFrame.winfo_width()) / 2,
        pady=(window.winfo_height() - alignmentFrame.winfo_height()) / 2 - 100
    )
    while answering:
        alignmentFrame.update()

    studentBand = bandDropDownValue.get()
    studentPos = posTextBox.get("1.0", tk.END).strip('\n')
    studentNeg = negTextBox.get("1.0", tk.END).strip('\n')

    # Step 2: Mark Response
    studentMark = MarkResponse(studentBand, studentPos, studentNeg, question)

    # Step 3: Display Marks
    showing = True
    clearWindow(alignmentFrame)
    window.title("Marks for " + question.Code)

    # Clearing the window means we need to re-make these elements.
    codeLabel = tk.Label(alignmentFrame, text=question.Code, bg='white')
    posLabel = tk.Label(alignmentFrame, text="Good Points:", bg='white')
    negLabel = tk.Label(alignmentFrame, text="Poor Points:", bg='white')

    posTextBorder = tk.Frame(alignmentFrame, bg='black')
    posTextBox = ScrolledText(posTextBorder, height=16, width=60, wrap=tk.WORD, bd=0, bg='light grey')
    posTextBox.insert(tk.END, studentPos)
    posTextBox.config(state=tk.DISABLED)
    posTextBox.grid(row=0, column=0, padx=3, pady=3)

    negTextBorder = tk.Frame(alignmentFrame, bg='black')
    negTextBox = ScrolledText(negTextBorder, height=16, width=60, wrap=tk.WORD, bd=0, bg='light grey')
    negTextBox.insert(tk.END, studentNeg)
    negTextBox.config(state=tk.DISABLED)
    negTextBox.grid(row=0, column=0, padx=3, pady=3)

    bandDropLabel = tk.Label(alignmentFrame, text="Band: " + studentBand, bg='white')
    bands = ['1-2', '3-4', '5-6']
    correctBand = bands[math.ceil(question.Band / 2) - 1]
    correctBandLabel = tk.Label(alignmentFrame, text="Correct: " + correctBand, bg='white')
    if studentMark.Band:
        correctBandLabel.config(fg='dark green')
    else:
        correctBandLabel.config(fg='red')

    posExpectedLabel = tk.Label(alignmentFrame, text="Expected Phrases:", bg='white')
    if len(studentMark.PosList) > 0:
        posExpected = studentMark.PosList[0]
        for index in range(1, len(studentMark.PosList)):
            posExpected += ", " + studentMark.PosList[index]
    else:
        posExpected = ''
    posExpectedTextBorder = tk.Frame(alignmentFrame, bg='black')
    posExpectedText = ScrolledText(
        posExpectedTextBorder, wrap=tk.WORD, width=54, height=16, bg='light grey'
    )
    posExpectedText.insert(tk.END, posExpected)
    posExpectedText.config(state=tk.DISABLED)
    posExpectedText.grid(row=0, column=0, padx=3, pady=3)

    posStrength = MakeStrengthMeter(studentMark.PosScore, alignmentFrame)

    negExpectedLabel = tk.Label(alignmentFrame, text="Expected Phrases:", bg='white')
    if len(studentMark.NegList) > 0:
        negExpected = studentMark.NegList[0]
        for index in range(1, len(studentMark.NegList)):
            negExpected += ", " + studentMark.NegList[index]
    else:
        negExpected = ''
    negExpectedTextBorder = tk.Frame(alignmentFrame, bg='black')
    negExpectedText = ScrolledText(
        negExpectedTextBorder, wrap=tk.WORD, width=54, height=16, bg='light grey'
    )
    negExpectedText.insert(tk.END, negExpected)
    negExpectedText.config(state=tk.DISABLED)
    negExpectedText.grid(row=0, column=0, padx=3, pady=3)

    negStrength = MakeStrengthMeter(studentMark.NegScore, alignmentFrame)

    doneButton = tk.Button(alignmentFrame, text="Done", command=closeMarks)

    codeLabel.grid(row=0, column=2, padx=5, pady=5, sticky='ne')

    bandDropLabel.grid(row=1, column=0, padx=5, pady=5)
    correctBandLabel.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

    posLabel.grid(row=2, column=0, padx=10, pady=2)
    posTextBorder.grid(row=3, column=0, padx=0, pady=3)
    posStrength.grid(row=3, column=1, padx=0, pady=3)
    posExpectedLabel.grid(row=2, column=2, padx=10, pady=2)
    posExpectedTextBorder.grid(row=3, column=2, padx=0, pady=3)

    negLabel.grid(row=4, column=0, padx=10, pady=2)
    negTextBorder.grid(row=5, column=0, padx=0, pady=3)
    negStrength.grid(row=5, column=1, padx=0, pady=3)
    negExpectedLabel.grid(row=4, column=2, padx=10, pady=2)
    negExpectedTextBorder.grid(row=5, column=2, padx=0, pady=3)

    doneButton.grid(row=6, column=1, padx=50, pady=5)

    # Handle the alignment
    # Work out the width of the frame and move it to the center of the screen. Unfortunately causes the question
    # to appear briefly on screen before moving, but there is not enough time to fix it right now. This weird
    # process seems to be required because tkinter doesn't calculate the width of everything until it has been
    # displayed.
    alignmentFrame.grid(row=0, column=0)
    alignmentFrame.update()
    alignmentFrame.grid_forget()
    alignmentFrame.grid(row=0, column=0, padx=(window.winfo_width() - alignmentFrame.winfo_width()) / 2)

    while showing:
        window.update()
