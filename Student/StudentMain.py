import tkinter as tk
import os.path as path
from Student.EnterCode import EnterCode
from Student.DisplayQuestion import DisplayQuestion
from Student.LoadQuestions import LoadQuestions


class StudentMain:
    # The root class of the application, initialises the window and calls the other modules in a loop.
    def __init__(self):
        self.window = tk.Tk()  # Create the window
        self.window.grid()
        # TODO: Implement Support for different screen sizes.
        # WIDTH = self.window.winfo_screenwidth()
        # HEIGHT = self.window.winfo_screenheight()
        WIDTH = 1280
        HEIGHT = 800
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.resizable(False, False)

        currentPath = path.abspath(".")  # TODO: Update Path for build version
        self.questions = LoadQuestions(currentPath + "/Questions.txt")

        try:
            self.window.after(0, self.loop)  # Start the custom loop
        except tk.TclError:
            # Can't be the window closing, something else has gone wrong.
            print("Exception before launch")
        self.window.mainloop()  # Start the tkinter library's window loop - handles inputs and display

    def loop(self):
        try:
            question = EnterCode(self.questions, self.window)
            DisplayQuestion(question, self.window)
        except tk.TclError:
            # Most likely, the window has been closed, so just put something in the log and finish.
            print("Exception")
            pass
        self.window.after(0, self.loop)  # Start the next cycle of the loop


if __name__ == "__main__":
    Main = StudentMain()  # Creates new Instance of the Program and Runs it.
