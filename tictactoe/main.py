########################################################################################################################
########################################################################################################################
# Project Creator: Dominic Clapper
# Date Created 8/11/2024
# Created for: Mini Portfolio Project to practice general python logic
# Purpose: Just getting some practice with running loops and if logic. Also some practice involving accessing dictionaries and editing them
########################################################################################################################
########################################################################################################################


# Function simply used to be called at the start of each game
# Displays basic game info
def display_start_game_text():
    print("###########################################################################################################")
    print("###########################################################################################################")
    print("# This is a very simple game of tic tac toe where you will be playing against a CPU.                      #")
    print("# The goal of the game is to fill three spaces in a row with your specific shape (X or O).                #")
    print("# You can win by getting 3 of your shape in a row, diagonally or in a line.                               #")
    print("###########################################################################################################")
    print("###########################################################################################################")

    print()

    print("This is what the intial game board looks like")
    print()

    print("   |   |   ")
    print("-----------")
    print("   |   |   ")
    print("-----------")
    print("   |   |   ")

    print()
    print()


# Checks to see if someone has won the game, or if the game ended in a draw
# There is a list of win condition positions to check and then we have a for loop that runs through these win conditions
# In this loop, we check to see if the values are all the same in any of the win conditions
# Then we return the value that won, so X or O
def check_win_status():
    win_conditions = [
        ['topLeft', 'topMid', 'topRight'],
        ['midLeft', 'midMid', 'midRight'],
        ['botLeft', 'botMid', 'botRight'],
        ['topLeft', 'midLeft', 'botLeft'],
        ['topMid', 'midMid', 'botMid'],
        ['topRight', 'midRight', 'botRight'],
        ['topLeft', 'midMid', 'botRight'],
        ['topRight', 'midMid', 'botLeft']
    ]

    for win_cond in win_conditions:
        values = [gameBoardDict[pos] for pos in win_cond]

        if values[0] != "" and values[0] == values[1] == values[2]:
            return values[0]

    return None


# All this function does is get the input from the user and validate it to make sure it is a correct string
# Gets called every loop twice
def get_user_choice():
    choice = None

    while choice is None:

        print()
        print()
        print("These are your possible row/col space options:")
        print()
        print()
        print("##############################################")
        print("topLeft, topMid, topRight")
        print("midLeft, midMid, midRight")
        print("botLeft, botMid, botRight")
        print("##############################################")
        print()
        print()

        choice = input("What row/col space do you want to select: ")

        if choice.lower() not in ['topleft', 'topmid', 'topright', 'midleft', 'midmid', 'midright', 'botleft', 'botmid',
                                  'botright']:
            print()
            print("Not a valid choice. Please enter something valid")
            print()
            choice = None

    return choice

# Just used to display the current game board given the current values in the gameBoardDict
# Gets called every loop twice
def display_curr_board():
    print(f" {gameBoardDict["topLeft"]} | {gameBoardDict["topMid"]} |{gameBoardDict["topRight"]}")
    print("--------")
    print(f" {gameBoardDict["midLeft"]} | {gameBoardDict["midMid"]} |{gameBoardDict["midRight"]}")
    print("--------")
    print(f" {gameBoardDict["botLeft"]} | {gameBoardDict["botMid"]} |{gameBoardDict["botRight"]}")


# Main function with update loop and gameboard dict used for defining the board and values
if __name__ == '__main__':

    # Starts out with blank values for each key, which are then assigned
    gameBoardDict = {"topLeft": "", "topMid": "", "topRight": "",
                     "midLeft": "", "midMid": "", "midRight": "",
                     "botLeft": "", "botMid": "", "botRight": ""}

    # Used to run the update loop
    winStatus = None
    # determines the turn of the users
    player1Turn = True

    # Displays the initial game info text
    display_start_game_text()

    # Update loop, runs both players turns and gets input from both. Also checks to make sure the input from the user
    # is not overwriting the other users.
    # Loop breaks when the call to check_win_status returns a value that is not None
    while not winStatus:

        if player1Turn:

            display_curr_board()

            print()
            print()

            player1Choice = get_user_choice()

            if gameBoardDict[player1Choice] == "":
                gameBoardDict[player1Choice] = "X"

                player1Turn = False

            else:
                print("That spot already has a shape in it!")
                print("Cannot place your shape there. Choose a different spot!")

        else:
            display_curr_board()

            print()
            print()

            player2Choice = get_user_choice()

            if gameBoardDict[player2Choice] == "":
                gameBoardDict[player2Choice] = "O"

                player1Turn = True

            else:
                print("That spot already has a shape in it!")
                print("Cannot place your shape there. Choose a different spot!")

        winStatus = check_win_status()

    if winStatus == "Draw":
        print("The game is a draw!")
    else:
        print(f"Player {winStatus} wins!")
