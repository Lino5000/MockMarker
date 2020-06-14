class Question:
    def __init__(self, code):
        # Default Values, will mostly be overwritten.
        self.Code = code  # A question can't be created without a code.
        self.Desc = None
        self.Img = None

    def __str__(self):
        # Defines how to print an instance, just used for debugging.
        return self.Code + ', "' + self.Desc + '", ' + self.Img


def LoadQuestions(filename):
    with open(filename, "r") as fileData:
        lines = fileData.readlines()
        questions = []
        qIndex = -1
        for index in range(len(lines)):
            words = lines[index].split(' ')
            if words[0] == "Quest:":
                qIndex += 1
                questions.append(Question(words[1].strip('\n')))
            elif words[0] == "Desc:":
                questions[qIndex].Desc = words[1]
                for wIndex in range(2, len(words)):
                    questions[qIndex].Desc += ' ' + words[wIndex].strip('\n')
            elif words[0] == "Img:":
                questions[qIndex].Img = words[1].strip('\n')
            else:
                pass
    return questions
