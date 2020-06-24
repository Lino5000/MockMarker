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

    meterCanvas = tk.Canvas(window, width=rectWidth * 4 + offset, height=rectHeight * 4 + offset, bg='white')

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

    # Step 1: Take input
    codeLabel = tk.Label(window, text=question.Code)
    codeLabel.grid(row=0, column=1, padx=5, pady=5, sticky='ne')

    bandLabel = tk.Label(window, text="Overall Band:")
    bandLabel.grid(row=1, column=0, columnspan=2, padx=10, pady=2)
    bandDropDownValue = tk.StringVar(window, "Choose a Band")
    bandDropDown = tk.OptionMenu(window, bandDropDownValue, "1-2", "3-4", "5-6")
    bandDropDown.grid(row=2, column=0, columnspan=2, padx=20, pady=3)

    posLabel = tk.Label(window, text="Good Points:")
    posLabel.grid(row=3, column=0, columnspan=2, padx=10, pady=2)
    posTextBorder = tk.Frame(window, bg='black')
    posTextBox = ScrolledText(posTextBorder, height=8, width=100, wrap=tk.WORD, bd=0, bg='light grey')
    posTextBox.grid(row=0, column=0, padx=3, pady=3)
    posTextBorder.grid(row=4, column=0, columnspan=2, padx=10, pady=3)

    negLabel = tk.Label(window, text="Poor Points:")
    negLabel.grid(row=5, column=0, columnspan=2, padx=10, pady=2)
    negTextBorder = tk.Frame(window, bg='black')
    negTextBox = ScrolledText(negTextBorder, height=8, width=100, wrap=tk.WORD, bd=0, bg='light grey')
    negTextBox.grid(row=0, column=0, padx=3, pady=3)
    negTextBorder.grid(row=6, column=0, columnspan=2, padx=10, pady=3)

    markButton = tk.Button(window, text="Mark", command=startMarking)
    markButton.grid(row=7, column=0, columnspan=2, padx=30, pady=5)

    while answering:
        window.update()

    studentBand = bandDropDownValue.get()
    studentPos = posTextBox.get("1.0", tk.END).strip('\n')
    studentNeg = negTextBox.get("1.0", tk.END).strip('\n')

    # Step 2: Mark Response
    studentMark = MarkResponse(studentBand, studentPos, studentNeg, question)

    # Step 3: Display Marks
    clearWindow(window)

    # Clearing the window means we need to re-make these elements.
    codeLabel = tk.Label(window, text=question.Code)
    posLabel = tk.Label(window, text="Good Points:")
    negLabel = tk.Label(window, text="Poor Points:")

    posTextBorder = tk.Frame(window, bg='black')
    posTextBox = ScrolledText(posTextBorder, height=16, width=60, wrap=tk.WORD, bd=0, bg='light grey')
    posTextBox.insert(tk.END, studentPos)
    posTextBox.config(state=tk.DISABLED)
    posTextBox.grid(row=0, column=0, padx=3, pady=3)

    negTextBorder = tk.Frame(window, bg='black')
    negTextBox = ScrolledText(negTextBorder, height=16, width=60, wrap=tk.WORD, bd=0, bg='light grey')
    negTextBox.insert(tk.END, studentNeg)
    negTextBox.config(state=tk.DISABLED)
    negTextBox.grid(row=0, column=0, padx=3, pady=3)

    bandDropLabel = tk.Label(window, text="Band: " + studentBand)
    bands = ['1-2', '3-4', '5-6']
    correctBand = bands[math.ceil(question.Band / 2) - 1]
    correctBandLabel = tk.Label(window, text="Correct: " + correctBand)
    if studentMark.Band:
        correctBandLabel.config(fg='dark green')
    else:
        correctBandLabel.config(fg='red')

    posExpectedLabel = tk.Label(window, text="Expected Phrases:")
    if len(studentMark.PosList) > 0:
        posExpected = studentMark.PosList[0]
        for index in range(1, len(studentMark.PosList)):
            posExpected += ", " + studentMark.PosList[index]
    else:
        posExpected = ''
    posExpectedTextBorder = tk.Frame(window, bg='black')
    posExpectedText = ScrolledText(
        posExpectedTextBorder, wrap=tk.WORD, width=60, height=16, bg='light grey'
    )
    posExpectedText.insert(tk.END, posExpected)
    posExpectedText.config(state=tk.DISABLED)
    posExpectedText.grid(row=0, column=0, padx=3, pady=3)

    posStrength = MakeStrengthMeter(studentMark.PosScore, window)

    negExpectedLabel = tk.Label(window, text="Expected Phrases:")
    if len(studentMark.NegList) > 0:
        negExpected = studentMark.NegList[0]
        for index in range(1, len(studentMark.NegList)):
            negExpected += ", " + studentMark.NegList[index]
    else:
        negExpected = ''
    negExpectedTextBorder = tk.Frame(window, bg='black')
    negExpectedText = ScrolledText(
        negExpectedTextBorder, wrap=tk.WORD, width=60, height=16, bg='light grey'
    )
    negExpectedText.insert(tk.END, negExpected)
    negExpectedText.config(state=tk.DISABLED)
    negExpectedText.grid(row=0, column=0, padx=3, pady=3)

    negStrength = MakeStrengthMeter(studentMark.NegScore, window)

    doneButton = tk.Button(window, text="Done", command=closeMarks)

    codeLabel.grid(row=0, column=2, padx=5, pady=5, sticky='ne')

    bandDropLabel.grid(row=1, column=0, padx=5, pady=5)
    correctBandLabel.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

    posLabel.grid(row=2, column=0, padx=10, pady=2)
    posTextBorder.grid(row=3, column=0, padx=20, pady=3)
    posStrength.grid(row=3, column=1, padx=0, pady=3)
    posExpectedLabel.grid(row=2, column=2, padx=10, pady=2)
    posExpectedTextBorder.grid(row=3, column=2, padx=20, pady=3)

    negLabel.grid(row=4, column=0, padx=10, pady=2)
    negTextBorder.grid(row=5, column=0, padx=20, pady=3)
    negStrength.grid(row=5, column=1, padx=0, pady=3)
    negExpectedLabel.grid(row=4, column=2, padx=10, pady=2)
    negExpectedTextBorder.grid(row=5, column=2, padx=20, pady=3)

    doneButton.grid(row=6, column=1, padx=50, pady=5)

    while showing:
        window.update()
