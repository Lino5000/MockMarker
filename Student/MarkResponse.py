import math


class Marks:
    def __init__(self):
        self.Band = None
        self.PosList = []
        self.NegList = []
        self.PosScore = 0
        self.NegScore = 0

    def __str__(self):
        return str(self.Band) + "Pos: " + str(self.PosList) + str(self.PosScore) + \
               "Neg: " + str(self.NegList) + str(self.NegScore)


def isLetter(char):
    # Check whether a given character is a letter, using the ASCII values with ord().
    return ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z')


def IsIn(word, string):
    # Slightly modified linear search. Python has a much simpler and faster way of doing this: "word in string"
    index = 0
    found = False
    while not found and index <= (len(string) - len(word)):
        match = True
        wIndex = 0
        while match and wIndex < len(word):
            if word[wIndex].lower() != string[index + wIndex].lower():
                match = False
            wIndex += 1
        if match:
            if index + wIndex >= len(string) or not isLetter(string[index + wIndex]):
                # The match is at the end of a word (either end of string or no more letters in word)
                if not isLetter(string[index - 1]):
                    # The match is at the start of a word
                    found = True
                else:
                    index += 1
            else:
                index += 1
        else:
            index += 1
    return found


def MarkResponse(studentBand, studentPos, studentNeg, question):
    studentMark = Marks()

    bands = ['1-2', '3-4', '5-6']
    correctBand = bands[math.ceil(question.Band / 2) - 1]
    if studentBand == correctBand:
        studentMark.Band = True
    else:
        studentMark.Band = False

    for index in range(len(question.Pos)):
        if not IsIn(question.Pos[index], studentPos):
            studentMark.PosList.append(question.Pos[index])
    studentMark.PosScore = 1 - (len(studentMark.PosList) / len(question.Pos))

    for index in range(len(question.Neg)):
        if not IsIn(question.Neg[index], studentNeg):
            studentMark.NegList.append(question.Neg[index])
    studentMark.NegScore = 1 - (len(studentMark.NegList) / len(question.Neg))

    return studentMark
