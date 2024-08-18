########################################################################################################################
########################################################################################################################
# Project Creator: Dominic Clapper
# Date Created 8/11/2024
# Created for: Mini Portfolio Project to test Pillow Lib
# Purpose: I wanted to test out some of the functions that are available in the PIL lib inside a UI.
########################################################################################################################
########################################################################################################################


# Libraries Used
########################################################################################################################
########################################################################################################################
import tkinter
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from PIL import ImageDraw
from PIL import ImageFont
########################################################################################################################
########################################################################################################################


# Class to hold all of our major logic.
# Has a few base vars such as root for UI, and image, setPos, and watermark_img for the logic aspects
class WatermarkAdd:

    # Basic init function to initialize certain vars, as well as create the Base UI
    def __init__(self, root):
        self.root = root

        self.image = None
        self.watermark_img = None
        self.setPos = None

        self.root.geometry("500x500")
        self.root.title("Image-Watermark Maker")

        self.openedIMG = tkinter.Label(root)
        self.openedIMG.pack()

        self.openImgBTN = tkinter.Button(root, text="Open File", command=self.DisplayImg)
        self.openImgBTN.pack()

        self.AddWaterBTN = tkinter.Button(root, text="Add Watermark", command=self.AddWatermark)
        self.AddWaterBTN.pack()


    # All this function does is open a file open dialog and check to see if the opened file is valid
    def GetFile(self):
        filename = fd.askopenfilename(
            title='Open a File',
            initialdir='/',
        )

        if filename:
            self.image = Image.open(filename)


    # Is the callback function for the openImgBTN.
    # Gets the opened img file and displays it in the UI
    def DisplayImg(self):

        self.GetFile()

        # Sets a new size for the image
        self.size = (300, 300)

        # Resizes the image
        self.resizedImg = self.image.resize(self.size)

        mainImg = ImageTk.PhotoImage(self.resizedImg)

        # Changes the openedIMG label to make it the selected image
        self.openedIMG.config(image=mainImg)
        self.openedIMG.image = mainImg

    # Is the sub-function for the AddWatermark button
    # Is called when the user clicks the add Watermark button
    # Depending on the button the user clicks in this sub UI, it calls a specific callback function to change the setPos var
    def choosePos(self):

        # Creates a new toplevel UI on top of root
        self.watermarkLOCPanel = tkinter.Toplevel(self.root)
        self.watermarkLOCPanel.geometry("350x350")
        self.watermarkLOCPanel.title("Choose Watermark Locations")

        # May come back to this later. Nothing for now
        self.LOCPanelImg = tkinter.Label(self.watermarkLOCPanel)
        self.LOCPanelImg.place(relx=0.5, rely=0.5)

        # Top Left pos button
        self.topLeftBTN = tkinter.Button(self.watermarkLOCPanel, text="Place top Left", command=self.placeTopLeft)
        self.topLeftBTN.place(relx=0.1, rely=0.1)

        # Top Right pos button
        self.topRightBTN = tkinter.Button(self.watermarkLOCPanel, text="Place top Right", command=self.placeTopRight)
        self.topRightBTN.place(relx=0.7, rely=0.1)

        # Bot Left pos button
        self.botLeftBTN = tkinter.Button(self.watermarkLOCPanel, text="Place bot Left", command=self.placeBotLeft)
        self.botLeftBTN.place(relx=0.1, rely=0.9)

        # Bot Right pos button
        self.botRightBTN = tkinter.Button(self.watermarkLOCPanel, text="Place bot Right", command=self.placeBotRight)
        self.botRightBTN.place(relx=0.7, rely=0.9)

        # Waits until the window closes to continue execution
        self.watermarkLOCPanel.wait_window()

    # Callback function that will change the setPos to top Left
    # Closes the top level window after selected
    def placeTopLeft(self):
        self.setPos = "top_left"
        self.watermarkLOCPanel.destroy()

    # Callback function that will change the setPos to top Right
    # Closes the top level window after selected
    def placeTopRight(self):
        self.setPos = "top_right"
        self.watermarkLOCPanel.destroy()

    # Callback function that will change the setPos to bot Left
    # Closes the top level window after selected
    def placeBotLeft(self):
        self.setPos = "bot_left"
        self.watermarkLOCPanel.destroy()

    # Callback function that will change the setPos to bot Right
    # Closes the top level window after selected
    def placeBotRight(self):
        self.setPos = "bot_right"
        self.watermarkLOCPanel.destroy()

    # Main logic function to add the watermark to the selected/opened image
    def AddWatermark(self):
        # If the image is valid, then the user is prompted to pick a location for the watermark via the choosePos function
        if self.image is not None:

            self.choosePos()

            # If setPos is None, then an error box will pop up.
            if self.setPos is None:
                tkinter.messagebox.showwarning("Warning", "No watermark position selected.")
                return

            # Starting textPos, just holder for now
            textPos = (0, 0)

            # Watermark text color
            textColor = (255, 255, 255, 128)

            img_width, img_height = self.image.size


            # Conditional logic branch that changes the position of the watermark based on what the user selected in the choosePos UI
            # Goes based off of the setPos var value
            if self.setPos == "top_left":

                textPos = (10, 10)

            elif self.setPos == "top_right":

                textPos = (img_width-200, 10)

            elif self.setPos == "bot_left":

                textPos = (10, img_height-50)

            elif self.setPos == "bot_right":

                textPos = (img_width - 200, img_height - 50)

            # Watermark text that will appear when the code runs
            # Change this text string to whatever you want
            watermark_text = "DomoSlime"

            # Creates a copy of the opened image
            self.watermark_img = self.image.copy()

            draw = ImageDraw.Draw(self.watermark_img)

            font = ImageFont.truetype("arial.ttf", 24)

            # Uses the draw object above to draw the watermark text on top of the copied version of the selected image
            draw.text(textPos, watermark_text, font=font, fill=textColor)

            if self.watermark_img.mode != 'RGB':
                self.watermark_img = self.watermark_img.convert('RGB')

            # Saves the image after edits are made
            self.watermark_img.save("watermarked_img.jpg")


########################################################################################################################
########################################################################################################################

# Just used to call the main logic by creating the tkinter UI
if __name__ == '__main__':
    root = tkinter.Tk()

    app = WatermarkAdd(root)

    root.mainloop()

