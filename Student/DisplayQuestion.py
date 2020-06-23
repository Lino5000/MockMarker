import tkinter as tk
from tkinter.scrolledtext import ScrolledText


def clearWindow(window):
    # Get all the elements in the window and destroy them
    for widget in window.winfo_children():
        widget.destroy()


def MakeStrengthMeter(strength, window):
    # TODO: Stub
    return tk.Label(window, text=str(strength))


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

    codeLabel = tk.Label(window, text=question.Code)
    codeLabel.grid(row=0, column=1, padx=5, pady=5)

    bandLabel = tk.Label(window, text="Overall Band:")
    bandLabel.grid(row=1, column=0, padx=10, pady=2)
    bandDropDownValue = tk.StringVar(window, "Choose a Band")
    bandDropDown = tk.OptionMenu(window, bandDropDownValue, "1-2", "3-4", "5-6")
    bandDropDown.grid(row=2, column=0, padx=20, pady=3)

    posLabel = tk.Label(window, text="Good Points:")
    posLabel.grid(row=3, column=0, padx=10, pady=2)
    posTextBorder = tk.Frame(window, bg='black')
    posTextBox = ScrolledText(posTextBorder, height=10, width=150, wrap=tk.WORD, bd=0, bg='light grey')
    posTextBox.grid(row=0, column=0, padx=3, pady=3)
    posTextBorder.grid(row=4, column=0, padx=10, pady=3)

    negLabel = tk.Label(window, text="Poor Points:")
    negLabel.grid(row=5, column=0, padx=10, pady=2)
    negTextBorder = tk.Frame(window, bg='black')
    negTextBox = ScrolledText(negTextBorder, height=10, width=150, wrap=tk.WORD, bd=0, bg='light grey')
    negTextBox.grid(row=0, column=0, padx=3, pady=3)
    negTextBorder.grid(row=6, column=0, padx=10, pady=3)

    markButton = tk.Button(window, text="Mark", command=startMarking)
    markButton.grid(row=7, column=0, columnspan=2, padx=50, pady=5)

    while answering:
        window.update()

    studentBand = bandDropDownValue.get()
    studentPos = posTextBox.get("1.0", tk.END).strip('\n')
    studentNeg = negTextBox.get("1.0", tk.END).strip('\n')

    print(studentBand, studentPos, studentNeg)
