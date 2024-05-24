# Import to make requests from web
import urllib.request

# Imports for UI
import tkinter
from tkinter import *
from tkinter import Tk

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# Creates our tkinter UI and holds the main logic to allow text entry and processing
def create_UI():

    root = Tk()

    root.title("Website Status Checker")
    root.geometry("500x250")
    root.config(bg="#75a3a3")

    # Header label
    headerLabel = Label(root, text="Website Status Check!", bg="#476b6b", fg="white", anchor='w', padx=10, font=('Arial', 14, 'bold'))
    headerLabel.place(x=0, y=0, relwidth=1, height=50)

    # Is used to determine if the entered text is a valid URL or not. Will return true if the URL is valid and active.
    # Will return false if not an active URL
    def checkWebsite(url):

        try:

            # Gets the status of the website attached to the URL
            statusCode = urllib.request.urlopen(url).getcode()

            if (statusCode == 200):
                return True

            else:
                return False

        except Exception as e:
            print("Error: ", e)
            return False

    # Holds the text entered from the entry widget
    url = tkinter.StringVar()

    # Is used to change the statusLabel given the specific return value of the checkWebsite function
    # green for active, red for down, and yellow for not a valid url
    def checkStatusAndUpdate():

        web = (url.get())

        if web.strip() != "":
            if checkWebsite(web):
                statusLabel.config(text="Website is Available", fg="black", bg="green")
            else:
                statusLabel.config(text="Website is not Available", fg="black", bg="red")

        else:
            statusLabel.config(text="Please Enter a Valid URL", fg="black", bg="yellow")

    urlEntLabel = Label(root, text="Enter a valid URL here: ", bg="#75a3a3", fg="white", font=('Arial', 12, 'bold'))
    urlEntLabel.place(relx=0.02, rely=0.22, relwidth=0.4)

    urlEntry = Entry(root, textvariable=url)
    urlEntry.place(relx=0.43, rely=0.22, relwidth=0.5)

    submitBTN = Button(root, text="Check URL", command=checkStatusAndUpdate, bg="#476b6b", fg="white", font=('Arial', 12, 'bold'))
    submitBTN.place(relx=0.41, rely=0.7, relwidth=0.2)

    statusLabel = Label(root, text="", font=('Arial', 14, 'bold'), bg="#75a3a3")
    statusLabel.place(relx=0.26, rely=0.5, relwidth=0.5)

    root.mainloop()

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Calls the main logic function
if __name__ == '__main__':
    create_UI()
