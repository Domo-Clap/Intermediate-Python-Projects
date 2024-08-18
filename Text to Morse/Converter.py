########################################################################################################################
# Project Creator: Dominic Clapper
# Date Created: 7/27/2024
# Created for: Mini Portfolio project
# Purpose: Just to practice a little bit of scripting and UI building
########################################################################################################################


# Libraries Used
########################################################################################################################
from tkinter import *
from tkinter import ttk
########################################################################################################################


# Main Logic function
# Contains UI code too
########################################################################################################################
def createUI():

    # Dictionary used to map letters/numbers to morse code
    morseDict = {"A": ".- ", "B": "-... ", "C": "-.-. ", "D": "-.D. ", "E": ". ", "F": ". . - . ",
                 "G": "--. ",
                 "H": ".... ", "I": ". . ", "J": ". - - - ", "K": "- . - ", "L": ". - . . ", "M": "- - ",
                 "N": "-. ",
                 "O": "--- ", "P": ". - - . ", "Q": "- - . - ", "R": ". - . ", "S": ". . . ", "T": "-  ",
                 "U": "..- ",
                 "V": "...- ", "W": ". - - ", "X": "- . . - ", "Y": "- . - - ", "Z": "- - . . ", "1": ". - - - - ",
                 "2": "..--- ", "3": ". . . - - ", "4": ". . . . - ", "5": ". . . . . ", "6": "- . . . . ",
                 "7": "--... ", "8": "- - - . . ", "9": "- - - - . ", "0": "- - - - - ", ".": ". - . - . - ",
                 ",": "--..-- ", "?": "..--.. "}

    # Callback function for the convert button
    # Takes the value from the text entry box and loops through each char of the string to get the morse conversion
    def convertString():
        inputStr = enterText.get()
        outputStr = []

        for inputChar in inputStr:
            if inputChar.upper() in morseDict.keys():
                print(inputChar.upper(), " = ", morseDict[inputChar.upper()])

                outputStr.append(morseDict[inputChar.upper()])

        finalMorse = "".join(outputStr)

        print(finalMorse)

        # Changes the blank morseOutput label to the converted morse text
        morseOutput.config(text=finalMorse)

    root = Tk()
    root.title("Morse Code Converter")
    root.config(bg="#f7f5dd")
    root.geometry("500x500")

    stringEntryVar = StringVar()

    headerLabel = Label(root, text="Morse Code Connverter", bg="#f7f5dd", font=("Courier", 25, "bold"))
    headerLabel.pack()

    enterLabel = Label(root, text="Enter your message here:", bg="#f7f5dd", font=("Courier", 16, "bold"))
    enterLabel.pack()

    enterText = Entry(root, textvariable=stringEntryVar)
    enterText.pack()

    convertBTN = Button(root, text="Convert Text", command=convertString)
    convertBTN.pack()

    morseOutput = Label(root, text="", bg="#f7f5dd")
    morseOutput.pack()

    # Builds UI and displays it
    root.mainloop()

########################################################################################################################

# Just used to call the main logic function
if __name__ == '__main__':
    createUI()
