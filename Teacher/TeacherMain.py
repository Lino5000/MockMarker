import tkinter as tk
from tkinter import messagebox
import os.path as path
from ChooseQuestion import ChooseQuestion
from DisplayQuestion import DisplayQuestion
from LoadQuestions import LoadQuestions


class TeacherMain:
    # The root class of the application, initialises the window and calls the other modules in a loop.
    def __init__(self):
        self.window = tk.Tk()  # Create the window
        self.window.grid()
        WIDTH = self.window.winfo_screenwidth()
        HEIGHT = self.window.winfo_screenheight()
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.resizable(False, False)

        currentPath = path.abspath("./Teacher")  # TODO: Update Path for build version
        # Small error handling thing added very late in the process, to account for missing file.
        try:
            self.questions = LoadQuestions(currentPath + "/Questions.txt")
        except FileNotFoundError:
            messagebox.showerror(
                'File not found',
                "The Questions.txt File could not be found. Please ensure the file is in the same folder as the " +
                "executable. "
            )
        else:
            try:
                self.window.after(0, self.loop)  # Start the custom loop
            except tk.TclError:
                # Can't be the window closing, something else has gone wrong.
                print("Exception before launch")
            self.window.mainloop()  # Start the tkinter library's window loop - handles inputs and display

    def loop(self):  # Has to be a separate function so it can be passed as a callback
        try:
            question = ChooseQuestion(self.questions, self.window)
            DisplayQuestion(question, self.window)
        except tk.TclError:
            # Most likely, the window has been closed, so just put something in the log and finish.
            print("Exception")
            return
        self.window.after(0, self.loop)  # Start the next cycle of the loop


if __name__ == "__main__":
    Main = TeacherMain()  # Creates new Instance of the Program and Runs it.
