import tkinter as tk
import os.path as path
from Teacher.ChooseQuestion import ChooseQuestion
from Teacher.DisplayQuestion import DisplayQuestion
from Teacher.LoadQuestions import LoadQuestions


class TeacherMain:
    def __init__(self):
        self.window = tk.Tk()  # Create the window

        currentPath = path.abspath(path.curdir) + "/Teacher/"  # TODO: Update Path for build version
        self.questions = LoadQuestions(currentPath + "Questions.txt")
        print(self.questions[0])

        try:
            self.window.after(0, self.loop)  # Start the custom loop
        except tk.TclError:
            # Most likely, the window has been closed, though unusually fast
            pass
        self.window.mainloop()  # Start the library's window loop - handles inputs and display

    def loop(self):  # Has to be a separate function so it can be passed as a callback
        try:
            question = ChooseQuestion(self.questions, self.window)
            DisplayQuestion(question, self.window)
        except tk.TclError:
            # Most likely, the window has been closed, so just finish.
            pass
        self.window.after(0, self.loop)  # Start the next cycle of the loop


if __name__ == "__main__":
    Main = TeacherMain()  # Creates new Instance of the Program and Runs it.
