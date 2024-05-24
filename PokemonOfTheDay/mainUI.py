# Imports for UI
import io
import tkinter
from tkinter import *
from tkinter import Tk

# Imports PIL Image and ImageTK to allow for pokemon image to be displayed in UI
from PIL import Image, ImageTk

# Used to gen random number to select random pokemon each day
import random

# Used to get info from the API
import requests
import json

# Used to manage time in CACHE file
import time

# File that holds the current timestamp, which is checked against a 24 hour timer
CACHE_FILE = "timestamp.txt"

# File that holds the current pokemon id/pokedex number. Used to still output the pokemon and its data even when the app is on cooldown
POKEMON_FILE = "savedPokemon.txt"
SECONDS_IN_DAY = 24 * 60 * 60

# Gets the pokedex number from the Pokemon Cache File
def getPokemonIndexFromFile():

    # If the file opens successfully, then it will read in the pokedex number and store return it
    try:
        with open(POKEMON_FILE, "r") as file:
            index = int(file.read().strip())
            return index
    # If the file does not open successfully, then an error is caught
    except FileNotFoundError:
        return None

# Saves the pokedex number to the Pokemon Cache File
def savePokemonIndexToFile(index):
    with open(POKEMON_FILE, "w") as file:
        file.write(str(index))


# Gets the last timestamp that is stored in the CACHE file. Is then used to compare with the current timestamp
def getLastTimestamp():
    # If the file opens successfully, then it will read the stored timestamp
    try:
        with open(CACHE_FILE, "r") as file:
            timestamp = int(file.read().strip())
            return timestamp

    # If the file does not open successfully, then an error is caught
    except FileNotFoundError:
        # Create the file and initialize with a default timestamp (0)
        with open(CACHE_FILE, "w") as file:
            file.write("0")
        return 0

# Updates the timestamp stored in the file
def updateTimestamp(timestamp):
    with open(CACHE_FILE, "w") as file:
        file.write(str(timestamp))

# Checks to see if the API is good to be pulled from based on the timer logic
def canPullFromAPI():

    lastTimeStamp = getLastTimestamp()

    # If there is no timestamp, then it returns true to gen a new pokemon
    if lastTimeStamp is None:
        return True

    currentTimeStamp = int(time.time())

    timeDiff = currentTimeStamp - lastTimeStamp

    return timeDiff >= SECONDS_IN_DAY

def createUI():

    root = Tk()
    root.title("Daily Pokemon!")
    root.geometry("400x500")

    root.config(bg="#ffccff")

    headerLabel = Label(root, text="Daily Pokemon Generator", bg="#666699", fg="white", anchor=CENTER, font=('Arial', 18, 'bold'))
    headerLabel.place(x=0, y=0, relwidth=1, height=80)

    cached_index = getPokemonIndexFromFile()

    # Used to change the randPokemonNum var so that it can determine whether a new pokemon should be found or if the stored pokemon should be found in the URL
    if cached_index is None or canPullFromAPI():
        randPokemonNum = random.randrange(0, 1153)
        savePokemonIndexToFile(randPokemonNum)
        updateTimestamp(int(time.time()))
    else:
        randPokemonNum = cached_index

    # URL for PokeAPI and it gets a specific pokemon based upon the data in the Pokemon Cache file
    url = f"https://pokeapi.co/api/v2/pokemon/{randPokemonNum}"

    # Gets info from the URL
    response = requests.get(url)

    # If the request response is valid, then create the rest of the UI
    if response.status_code == 200:

        data = response.json()

        pName = data['name'].capitalize()
        pDexNum = data['id']
        pTypes = [type_data['type']['name'].capitalize() for type_data in data['types']]

        pSpriteURL = data['sprites']['front_default']

        pSpriteResponse = requests.get(pSpriteURL)
        pSpriteData = Image.open(io.BytesIO(pSpriteResponse.content))
        pSprite = ImageTk.PhotoImage(pSpriteData)

        pNameLabel = Label(root, text="Pokemon Name: " + str(pName), bg="#ffccff", font=('Arial', 14, 'bold'))
        pNameLabel.place(relx=0.5, rely=0.25, anchor=CENTER)

        pDexNumberLabel = Label(root, text="Pokedex Number: " + str(pDexNum), bg="#ffccff", font=('Arial', 14, 'bold'))
        pDexNumberLabel.place(relx=0.5, rely=0.35, anchor=CENTER)

        pTypesLabel = Label(root, text="Pokemon Type(s): " + ", ".join(pTypes), bg="#ffccff", font=('Arial', 14, 'bold'))
        pTypesLabel.place(relx=0.5, rely=0.45, anchor=CENTER)

        pSpriteFrame = Frame(root, bg="#ffccff", highlightbackground="black", highlightthickness=2)
        pSpriteFrame.place(relx=0.5, rely=0.75, anchor=CENTER)

        pSpriteLabel = Label(pSpriteFrame, image=pSprite, bg="#ffccff")
        pSpriteLabel.image = pSprite
        pSpriteLabel.pack()

        # Prints the JSON data that is got from the API
        json_formatted_str = json.dumps(data, indent=2)
        print(json_formatted_str)

    else:
        print("Error:", response.status_code, response.reason)

    root.mainloop()

# Starts execution of the code by creating the UI and logic
if __name__ == '__main__':
    createUI()

