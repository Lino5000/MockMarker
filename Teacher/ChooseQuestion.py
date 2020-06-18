import tkinter as tk
from tkinter import ttk


def clearWindow(window):
    for widget in window.winfo_children():  # Get all the elements in the window and destroy them
        widget.destroy()


def submit():
    # A callback function so that the submit button can change the submitted variable.
    global submitted
    submitted = True


submitted = False


def ChooseQuestion(questions, window):
    global submitted
    WIDTH = window.winfo_screenwidth()
    HEIGHT = window.winfo_screenheight()
    clearWindow(window)
    titleLabel = tk.Label(window, text="Choose a Question:")  # Make the Label
    titleLabel.grid(column=0, row=0, padx=15, pady=5)  # Place the label on the screen

    questionList = ttk.Treeview(window, height=(int(HEIGHT / 22)))  # Make the TreeView list
    xPadding = 10
    questionList.column("#0", width=(WIDTH - 2 * xPadding - 5))
    questionList.heading("#0", text="Question", anchor=tk.W)  # Set the heading of the list
    for index in range(len(questions)):
        if questions[index].Desc is not None:
            item = questions[index].Desc
        else:
            item = questions[index].Code
        questionList.insert("", "end", text=item)  # Add an item to the list with the correct text
    questionList.grid(column=0, row=1, padx=xPadding)  # Place the list on the screen

    submitted = False
    submitButton = tk.Button(window, text="Show Question", command=submit)
    submitButton.grid(row=5, column=0, pady=15)

    while not submitted:
        window.update()  # Tell tkinter to repeatedly update the screen. Handles display and input.

    selectedIndex = questionList.index(questionList.focus())
    return questions[selectedIndex]
