import tkinter as tk


def clearWindow(window):
    # Get all the elements in the window and destroy them
    for widget in window.winfo_children():
        widget.destroy()


popOpen = False


def popClose():
    # A callback to close the popup
    global popOpen
    popOpen = False


def DisplayPopup():
    global popOpen
    popup = tk.Tk()
    popOpen = True
    tk.Label(popup, text="That question does not exist").grid(row=0, column=0, padx=10, pady=5)
    tk.Button(popup, text="Try Again", command=popClose).grid(row=1, column=0, padx=50, pady=5)
    while popOpen:
        popup.update()
    popup.destroy()


def searchByCode(code, questionList):
    # A simple linear search to find a code in the list. Could be implemented more efficiently using python's sorted().
    index = 0
    found = False
    while not found and index < len(questionList):
        if questionList[index].Code == code:
            found = True
            question = questionList[index]
        index += 1
    if not found:
        question = "Invalid"
    return question


buttonPressed = False


def submit(e=None):
    # A callback for the submit button.
    global buttonPressed
    buttonPressed = True


def EnterCode(possibleQuestions, window):
    global buttonPressed
    buttonPressed = False
    submitted = False
    clearWindow(window)
    tk.Label(window, text="Please enter a Question Code:").grid(row=0, column=0, padx=10, pady=5)
    inputCode = tk.StringVar(window)
    tk.Entry(window, textvariable=inputCode, width=29).grid(row=1, column=0, padx=10, pady=5)
    tk.Button(window, text="Go!", command=submit).grid(row=2, column=0, padx=30, pady=5)
    window.bind("<Return>", submit)  # Just a convenience thing, allow pressing Enter to trigger the submit button.
    while not submitted:
        window.update()
        if buttonPressed:
            question = searchByCode(inputCode.get(), possibleQuestions)
            if question == "Invalid":
                DisplayPopup()
                buttonPressed = False
            else:
                submitted = True
    window.unbind("<Return>")  # Don't want enter to trigger that function anymore, because the window is changing.
    return question
