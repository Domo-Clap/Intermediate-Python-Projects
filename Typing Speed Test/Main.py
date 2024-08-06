########################################################################################################################
# Project Creator: Dominic Clapper
# Date Created: 7/28/2024
# Created for: Mini Portfolio project
# Purpose: Just to practice a little bit of scripting and UI building
########################################################################################################################


# Libraries Used
########################################################################################################################
from tkinter import *
from tkinter import ttk

import time
import random
########################################################################################################################


# List that has all of the sentences that can appear when the user starts the typing test
sentenceList = ["Now is the time for all good men to come to the aid of their country.",
                "Exceeding expectations requires both dedication and hard work.",
                "The professor explained the intricate details of quantum physics with clarity.",
                "Despite the heavy rain, the children played joyfully in the park.",
                "Under the starry sky, the campfire crackled and the night felt magical.",
                "Innovative ideas often emerge from the most unexpected places and times."]

# Main function that holds the UI building plus the main logic
# Creates UI, and has logic that provides sentence to type and starts/ends timer when needed.
def create_UI():

    # Function used to start the timer, as well as select a random sentence for the user to type
    def startTest():

        global startTime, targetSentence, numWords

        # Gets the random sentence to type
        targetSentence = getRandomSentence()

        # Figures out how many words are in the sentence
        numWords = len(targetSentence.split())

        sentenceToType.config(text=targetSentence)

        # Enables typing in the text box
        enterBox.config(state='normal')

        enterBox.delete(1.0, END)

        # Disables the start button from being clicked
        startBTN.config(state='disabled')
        # Gets the current time. Used later
        startTime = time.time()

    # Function used to check and see if the text in the text box equal the sentence string
    def checkTyping():
        global startTime, numWords

        # Retrieves the text in the text box
        userText = enterBox.get(1.0, END).strip()

        # If the user text equals the sentence text, then an end time is found. The elapsed time and WPS are then calculated.
        if userText == targetSentence:
            endTime = time.time()
            elapsedTime = endTime - startTime

            WPS = round((numWords / elapsedTime), 3)

            mainResultLabel.config(text=f"The time it took you to type the sentence was: {elapsedTime}.")
            WPSLabel.config(text=f"Your words per second is: {WPS}.")

            # Re-enables the start button
            startBTN.config(state="normal")

        # If the user text is not correct, will say keep trying
        else:
            mainResultLabel.config(text="Keep Trying!")

    # Function that gets and returns a random sentence from the list
    def getRandomSentence():
        return random.choice(sentenceList)

    # Defines tkinter window
    root = Tk()

    # Basic window size and title
    root.geometry("500x500")
    root.title("Typing Speed Test")

    headerLabel = Label(root, text="Typing Speed Test", font=("Courier", 25, "bold"))
    headerLabel.pack()

    subHeaderLabel = Label(root, text="See how fast you can type!", font=("Courier", 18, "bold"))
    subHeaderLabel.pack()

    # Updates when the user hits the button
    sentenceToType = Label(root, text="")
    sentenceToType.pack()

    # Where user will enter text
    enterBox = Text(root, height=8, width=30, state='disabled')
    enterBox.pack()

    enterBox.bind("<KeyRelease>", lambda e: checkTyping())

    # Calls the startTest function which will choose a random sentence and start the timer
    startBTN = Button(root, text="Start Test", command=startTest)
    startBTN.pack()

    mainResultLabel = Label(root, text="", font=("Courier", 11, "bold"))
    mainResultLabel.pack()

    WPSLabel = Label(root, text="", font=("Courier", 11, "bold"))
    WPSLabel.pack()

    root.mainloop()


# Used to call the create_UI function which pretty much is the entire program
if __name__ == '__main__':
    create_UI()
