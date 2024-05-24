import tkinter
import webbrowser
from tkinter import *
from tkinter import Tk

# Imports pyshorteners library to shorten URLs
import pyshorteners
# Imports the urlparse func to allow for our url to be checked to see if it is valid input
from urllib.parse import urlparse

import pyperclip


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


#Main UI logic. Also holds most of the general logic for the processing
def create_Main_UI():

    # Main callback function.
    # Used to check if URL is valid or invalid
    # Also used to update the newURLText widget to show the user the converted URL if possible.
    # Does so by calling the shortenURLTiny method
    def shorten_URL():

        # Gets the URL the user entered from the
        url = baseURL.get()

        apiToUse = APIChoice.get()

        try:

            # Parses the URL for validation checking
            scannedURL = urlparse(url)

            # If the entered URL is not valid, then it will raise an error that will change the text shown to the user
            if (scannedURL.scheme == '' or scannedURL.netloc == ''):
                raise ValueError("Invalid URL!!!")

            if (apiToUse == 'Tiny'):

                newURL = shortenURLTiny(url)

            elif (apiToUse == 'Da'):

                newURL = shortenURLDa(url)

            elif (apiToUse == 'Isgd'):

                newURL = shortenURLIsgd(url)

            elif (apiToUse == 'Post'):

                newURL = shortenURLPost(url)

            newURLText.delete(1.0, END)
            newURLText.insert(END, newURL)

            # Makes the text a hyperlink that leads to the URL
            newURLText.tag_add("hyperlink", "1.0", "end")
            newURLText.bind("<Button-1>", lambda event: open_url(newURL))

            plainTextURLFinal.config(text=newURL)
            copyURL(newURL)

        # Catches the exception for an invalid URL
        # Resets the newURL text and adds an error message to it
        except Exception as e:

            newURLText.delete(1.0, END)
            newURLText.insert(END, "ERROR: "+ str(e))

    # Used to open the web browser to the link that the new shortened URL points to
    def open_url(url):
        webbrowser.open(url)

    def copyURL(url):

        pyperclip.copy(url)


    # Creates window
    root = Tk()

    # Used to hold the value entered by the user
    baseURL = tkinter.StringVar()

    APIChoice = tkinter.StringVar()

    APIOptions = ['Da', 'Tiny', 'Isgd', 'Post']

    # Sets background of window to gray
    root.config(bg="gray")

    # Sets title and size for window
    root.title("URL Shortener - BASIC")
    root.geometry("750x400")

    # Title Label
    headerLabel = Label(root, text="Simple URL Shortener!", font=('Arial', 18), fg='black', bg='gray')
    headerLabel.place(relx=0.5, rely=0.05, anchor=CENTER)

    # Selector Label
    selectLabel = Label(root, text="Select the API you wish to use to convert the URL: ", font=('Arial', 14), fg='black', bg='gray')
    selectLabel.place(relx=0.5, rely=0.12, anchor=CENTER)

    selectAPI = OptionMenu(root, APIChoice, *APIOptions)
    selectAPI.place(relx=0.82, rely=0.12, anchor=CENTER)

    inputLabel = Label(root, text="Enter the URL you want to shorten here: ", font=('Arial', 14), fg='black', bg='gray')
    inputLabel.place(relx=0.4, rely=0.20, anchor=CENTER)

    # Gets info from the user and assigns it to baseURL
    baseURLEntry = Entry(root, textvariable=baseURL)
    baseURLEntry.place(relx=0.76, rely=0.20, anchor=CENTER, width=200)

    # Click to call shorten_URL function
    convertBTN = Button(root, text="Convert URL", command=shorten_URL, font=('Arial', 12), fg='black', bg='white')
    convertBTN.place(relx=0.5, rely=0.30, anchor=CENTER)

    plainTextURL = Label(root, text="Non-hyper-link URL: ", font=('Arial', 14), fg='black', bg='gray')
    plainTextURL.place(relx=0.5, rely=0.50, anchor=CENTER)

    plainTextURLFinal = Label(root, text="")
    plainTextURLFinal.place(relx=0.68, rely=0.50, anchor=CENTER)

    # Where the new URL or error message will appear
    newURLText = Text(root, wrap=WORD)
    newURLText.place(relx=0.5, rely=0.60, anchor=CENTER, width=300, height=50)

    root.mainloop()


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# Creates an instance of the pyshorteners library to control the way URLs are shortened
def shortenURLTiny(url):
    tinyURLShortener = pyshorteners.Shortener()

    print("Using Tiny API")

    newURL = tinyURLShortener.tinyurl.short(url)

    return newURL

def shortenURLIsgd(url):
    IsgdURLShortener = pyshorteners.Shortener()

    print("Using Isgd API")

    newURL = IsgdURLShortener.isgd.short(url)

    return newURL

def shortenURLPost(url):
    PostURLShortener = pyshorteners.Shortener()

    print("Using Post API")

    newURL = PostURLShortener.post.short(url)

    return newURL

def shortenURLDa(url):
    DasURLShortener = pyshorteners.Shortener()

    print("Using Da API")

    newURL = DasURLShortener.dagd.short(url)

    return newURL





# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# Main function. Creates UI on start
if __name__ == '__main__':
    create_Main_UI()