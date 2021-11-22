import tkinter as tk

class GameLogic:
    """
    Class full of variables and methods that control the game's status.

    Contains variables like the player's scores, whose turn it is, whether the game is over,
    and the current grid.  The methods edit the variables to match the players' inputs,
    report successful SOS patterns, and keep track of player scores.  Game over conditions will
    be handled by the children classes.

    Attributes:
        redScore and blueScore: ints that keep track of how many times a player has scored
        currentTurn: bool that is True when it is Red's turn and False when it is Blue's turn.
        currentGameSize: int that will keep track of how big the current array is.
        redPlayer and bluePlayer: bools that determine whether the players are controlled by
        humans or the computer.
        letterArray: a square (default 8x8) array that keeps track of the letters inputed by the players.
        gameRunning: bool that prevents players from making moves after the game's end conditions are met
        (until a new game is started)

        placeLetter(self, xVal, yVal, letter): places the given letter at coordinates (yVal, xVal)
        within the letterArray.
        findPatternForS(self, currPlayer, SX, SY, OX, OY) and findPatternForO(self, currPlayer, X1, Y1, X2, Y2):
        Whenever an S or O respectively is placed on the grid, these methods will be called to find any SOS
        patterns formed around the new entry.
        changeRedLetter(letter) and changeBlueLetter(letter): changes the selected letter 
        for a player that will be placed in the letterArray with placeLetter method.
        getTurnString(self): returns a string that tells whether it is Red's or Blue's turn based
        on currentTurn.
    """

    #Initiates GameLogic with variables controlling game and an array of strings.
    def __init__(self, newSize, redStatus, blueStatus):
        self.redScore = 0
        self.blueScore = 0
        #When currentTurn is true, it is red's turn; otherwise, it is blue's turn.
        self.currentTurn = True
        self.currentAnnounce = ""
        self.gameRunning = True

        self.currentGameSize = newSize
        #When these variables are true, there is a human player; otherwise, 
        #it is a computer. FIXME: NOT IMPLEMENTED.
        self.redComputer = redStatus
        self.blueComputer = blueStatus

        #Initializes 2D array that contains letters.
        self.letterArray = []
        for y in range(0,self.currentGameSize):
            tempArray = []
            for x in range(0,self.currentGameSize):
                tempArray.append(" ")
            self.letterArray.append(tempArray)

    #Places letter within letterArray IF the inputs are valid.
    def placeLetter(self, xVal, yVal, letter):
        #If the game is already over, the letter is not placed.
        if (self.gameRunning == False):
            self.currentAnnounce = "Game is over."
            return False
        #If the input values would not fit on the grid, the letter is not placed.
        elif (xVal < 0 or xVal >= len(self.letterArray) or yVal < 0 or yVal >= len(self.letterArray[0])):
            self.currentAnnounce = "Invalid grid position"
            return False
        #If the space in the array is occupied, the letter is not placed.
        elif (self.letterArray[yVal][xVal] != " "):
            self.currentAnnounce = "Entered position is occupied"
            return False
        #If this is a valid position, places the letter in the correct space
        #in the array and returns True.
        else:
            self.letterArray[yVal][xVal] = letter
            self.currentTurn = not self.currentTurn
            self.currentAnnounce = "Letter successfully placed"
            return True
        
    #Using related entries in letterArray, finds out if there is an SOS pattern.
    #If there is, increases a player's score and returns True.
    def findPatternForS(self, currPlayer, SX, SY, OX, OY):
        #Prevents rollover within array, e.g. self.letterArray[-1][-1] is invalid.
        valid = (SX >= 0 and SY >= 0 and SX < len(self.letterArray) and SY < len(self.letterArray))
        try:
            #If letter forms SOS pattern, increases respective score and returns True.
            #This indicates that a line should be drawn on the GUI.
            if (self.letterArray[SY][SX] == "S" and self.letterArray[OY][OX] == "O" and valid == True):
                if (currPlayer):
                    self.redScore += 1
                else:
                    self.blueScore += 1
                return True
            else:
                return False
        except (IndexError):
            #If one of the inputs is out of bounds for letterArray, returns False.
            return False

    #Similar function to findPatternForS.
    def findPatternForO(self, currPlayer, X1, Y1, X2, Y2):
        valid = (X1 >= 0 and X1 < len(self.letterArray) and Y1 >= 0 and Y1 < len(self.letterArray) and X2 >= 0 and X2 < len(self.letterArray) and Y2 >= 0 and Y2 < len(self.letterArray))
        try:
            if (self.letterArray[Y1][X1] == "S" and self.letterArray[Y2][X2] == "S" and valid):
                if (currPlayer):
                    self.redScore += 1
                else:
                    self.blueScore += 1
                return True
            else:
                return False
        except (IndexError):
            return False
    
    #Two methods that change letter for each player.
    def changeRedLetter(letter):
        redLetter = letter

    def changeBlueLetter(letter):
        blueLetter = letter

    #Method that returns string based on which player's turn it is.
    def getTurnString(self):
        if (self.currentTurn):
            return "Red's turn"
        else:
            return "Blue's turn"

    
class SimpleGame(GameLogic):
    """
    Variant of GameLogic that ends when a single SOS pattern is formed.

    Inherits from GameLogic and adds game over conditions. If either player scores, they are
    declared winner and the game stops. Else, the game ends if the grid is full with no SOS patterns
    formed. Once gameRunning is set to False, no more moves are possible.

    Attributes:
        gameOver(self): After every move, checks if there are any SOS patterns formed and if the 
        grid is full.  If so, gameRunning is set to False and the players cannot move.  To return 
        gameRunning to True, the player(s) must create a new game.
    """

    def __init__(self, newSize, redStatus, blueStatus):
        GameLogic.__init__(self, newSize, redStatus, blueStatus)
        self.currentAnnounce = "New Simple Game!"

    def gameOver(self):
        #If either player scored, game is over and victor is declared with currentAnnounce.
        if (self.redScore > 0):
            self.gameRunning = False
            self.currentAnnounce = "Red wins!"
        elif (self.blueScore > 0):
            self.gameRunning = False
            self.currentAnnounce = "Blue wins!"
        #If the grid is full and neither player scored, game is over and there is a draw.
        else:
            gridFull = True
            for x in range(0, len(self.letterArray)):
                for y in range(0, len(self.letterArray[0])):
                    if (self.letterArray[y][x] == " "):
                        gridFull = False
            if (gridFull):
                self.gameRunning = False
                self.currentAnnounce = "Game is a draw."
            else:
                self.gameRunning = True

class ComplexGame(GameLogic):
    """
    Variant of GameLogic that tracks each player's scores and ends only when the grid is full.

    Inherits from GameLogic and adds game over conditions. If the game's grid is full, the player
    with the higher score is declared the winner; if they are equal, the game is a draw.
    Once gameRunning is set to False, no more moves are possible.

    Attributes:
        gameOver(self): After every move, checks if the grid is full.  If so, gameRunning is
        set to False and a winner is declared.  To return gameRunning to True, the player(s) 
        must create a new game.
    """

    def __init__(self, newSize, redStatus, blueStatus):
        GameLogic.__init__(self, newSize, redStatus, blueStatus)
        self.currentAnnounce = "New Complex Game!"
    
    def gameOver(self):
        #Checks if grid is full (no entries are equal to " ").
        gridFull = True
        for x in range(0, len(self.letterArray)):
            for y in range(0, len(self.letterArray[0])):
                if (self.letterArray[y][x] == " "):
                    gridFull = False
        if (gridFull):
            self.gameRunning = False
            #Determines winner based on each player's score. The higher score wins.
            if (self.redScore > self.blueScore):
                self.currentAnnounce = "Red wins!"
            elif (self.blueScore > self.redScore):
                self.currentAnnounce = "Blue wins!"
            else:
                self.currentAnnounce = "Game is a draw."
        else:
            self.gameRunning = True