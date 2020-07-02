import tkinter as tk


class Question:
    # A record that stores a single question's information.
    def __init__(self, code):
        # Default Values, will mostly be overwritten.
        self.Code = code  # A question can't be created without a code.
        self.Band = 0
        self.Pos = []
        self.Neg = []

    def __str__(self):
        # Defines how to print an instance, just used for debugging.
        return str(self.Code) + ', ' + str(self.Band) + ', ' + str(self.Pos) + ', ' + str(self.Neg)


def isCompleteQuestion(question):
    complete = False
    if question.Band > 0:
        if len(question.Pos) > 0:
            if len(question.Neg) > 0:
                complete = True
    return complete


def DisplayPopup(codeList):
    popup = tk.Tk()
    closeButton = tk.Button(popup, text="Ok", command=popup.destroy)
    tk.Label(popup, text="The following questions were not loaded:").grid(row=0, column=0, pady=10, padx=10)
    for index in range(len(codeList)):
        tk.Label(popup, text=codeList[index]).grid(row=index + 1, column=0, pady=2, padx=20)
    closeButton.grid(row=len(codeList) + 1, column=0, pady=10, padx=50)
    popup.mainloop()


def LoadQuestions(filename):
    with open(filename, 'r') as fileData:
        lines = fileData.readlines()
        questions = []  # Need a default value here so python won't be angry
        unloaded = []
        uIndex = 1
        qIndex = -1
        for index in range(len(lines)):
            words = lines[index].strip('\n').split(' ')
            if words[0] == "Quest:":
                if qIndex == -1:
                    qIndex += 1
                elif isCompleteQuestion(questions[qIndex]):
                    # Need these as two different checks, otherwise python will raise a runtime error trying to
                    # access the nonexistent item in questions.
                    qIndex += 1
                else:
                    unloaded.append(questions[qIndex].Code)
                    uIndex += 1
                    questions[qIndex].Band = 0
                    questions[qIndex].Pos = []
                    questions[qIndex].Neg = []
                questions.append(Question(words[1]))
            elif words[0] == "Band:":
                try:
                    questions[qIndex].Band = int(words[1])
                except ValueError:
                    return "Error at line" + str(index)
            elif words[0] == "Pos:":
                temp = ""
                for wordIndex in range(1, len(words)):
                    temp += ' ' + words[wordIndex]
                # Split at ',' and remove trailing spaces.
                for item in temp.split(','):
                    questions[qIndex].Pos.append(item.strip(' '))
            elif words[0] == "Neg:":
                temp = ""
                for wordIndex in range(1, len(words)):
                    temp += ' ' + words[wordIndex]
                # Split at ',' and remove trailing spaces.
                for item in temp.split(','):
                    questions[qIndex].Neg.append(item.strip(' '))
            else:
                pass  # Just to make it explicit that nothing should be done.
        if not isCompleteQuestion(questions[qIndex]):
            unloaded.append(questions[qIndex].Code)
            del questions[qIndex]
        if len(unloaded) > 0:
            DisplayPopup(unloaded)
        return questions
