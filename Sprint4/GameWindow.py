from GameLogic import *
import random

#Inherits from GameLogic.
class GameWindow:
    """
    Class that creates window and displays the state of the game in the GUI.

    Inherits all of the variables and methods from GameLogic. Creates the window and frames that
    will contain UI widgets, then creates labels, buttons, and entry boxes and places them in 
    the frames. The playing grid canvas takes up the middle space, options for each player rest 
    on the sides of the grid, and the bottom holds the buttons for controlling the game and 
    entry boxes for inputting x and y values.

    Important Attributes:
        currentGame: an instance of either SimpleGame or ComplexGame that keeps track of the rules
        and state of the current game.
        xEntry and yEntry: entry boxes that receive coordinates from the user.
        redSButton and redOButton: buttons that control whether Red will enter an S or an O.
        blueSButton and blueObutton: buttons that do the same thing for Blue.
        addCharButton: adds a letter to GameLogic.letterArray and gridCanvas IF inputs from xEntry
        and yEntry are a valid, unoccupied space.
        simpleButton and complexButton: radiobuttons that control whether the next game will be a 
        simple or complex game.
        gridSizeEntry: entry box that determines the dimensions of the next game created by newGameButton.
        newGameButton: restarts game by creating new SimpleGame or ComplexGame, then resetting 
        gridCanvas with the appropriate height and width.
        gridCanvas: a canvas that displays a grid and shows the player the status of the current game.
        Visible attributes include the game's size, the S and O placements, and any SOS patterns that
        have been formed with colored lines.

        gridLetter(self): method connected to addCharButton. Finds appropriate letter and coordinates,
        then places letter in GameLogic.letterArray and gridCanvas OR displays error message in
        announceLabel. Also checks for created SOS patterns and if game is over.
        newGameCommand(self): method connected to newGameButton. Creates new GameLogic derivative
        based on nextGameType and gridSizeEntry.
    """

    def __init__(self):
        #Initializes first game, a simple game with grid size of 8.
        self.currentGame = SimpleGame(8, False, False)

        #Window setup.
        self.window = tk.Tk()
        self.window.title("SOS Game")
        self.window.geometry("600x400")

        #Sets up frames within window.
        self.headerFrame = tk.Frame(self.window)
        self.redFrame = tk.Frame(self.window)
        self.blueFrame = tk.Frame(self.window)
        self.gridFrame = tk.Frame(self.window)
        self.scoreFrame = tk.Frame(self.window)
        self.charEntryFrame = tk.Frame(self.window)

        #Labels that will be edited during the game.
        self.redScoreLabel = tk.Label(self.scoreFrame, width = 3, text = "0")
        self.blueScoreLabel = tk.Label(self.scoreFrame, width = 3, text = "0")
        self.turnLabel = tk.Label(self.scoreFrame, text = "Red's turn")
        self.announceLabel = tk.Label(self.scoreFrame)

        #String variables and radio buttons that control what letter each player will insert.
        self.redSV = tk.StringVar(self.window, "S")
        self.blueSV = tk.StringVar(self.window, "S")
        self.redSButton = tk.Radiobutton(self.redFrame, pady = 3, text = "S", variable = self.redSV, value = "S")
        self.redOButton = tk.Radiobutton(self.redFrame, pady = 3, text = "O", variable = self.redSV, value = "O")
        self.blueSButton = tk.Radiobutton(self.blueFrame, pady = 3, text = "S", variable = self.blueSV, value = "S")
        self.blueOButton = tk.Radiobutton(self.blueFrame, pady = 3, text = "O", variable = self.blueSV, value = "O")

        #Boolean variable and radio buttons that will control the next game's ruleset.
        self.nextGameType = tk.BooleanVar(self.window, True)
        self.simpleButton = tk.Radiobutton(self.charEntryFrame, text = "Simple Game", variable = self.nextGameType, value = True)
        self.complexButton = tk.Radiobutton(self.charEntryFrame, text = "Complex Game", variable = self.nextGameType, value = False)

        #String variables and entry boxes that obtain coordinates for entered letter or the size of
        #the grid for the next game.
        self.currentX = tk.StringVar(self.window)
        self.currentY = tk.StringVar(self.window)
        self.nextGridSizeVar = tk.StringVar(self.window, value = "8")
        self.xEntry = tk.Entry(self.charEntryFrame, width = 10, textvariable = self.currentX)
        self.yEntry = tk.Entry(self.charEntryFrame, width = 10, textvariable = self.currentY)
        self.gridSizeEntry = tk.Entry(self.charEntryFrame, width = 5, textvariable = self.nextGridSizeVar)

        #Checkboxes that control whether a player is controlled by a human or computer (not implemented).
        self.nextRedPlayer = tk.BooleanVar(self.window, False)
        self.nextBluePlayer = tk.BooleanVar(self.window, False)
        self.redComputerBox = tk.Checkbutton(self.redFrame, text = "Computer", variable = self.nextRedPlayer)
        self.blueComputerBox = tk.Checkbutton(self.blueFrame, text = "Computer", variable = self.nextBluePlayer)

        #Buttons that add S or O to board and starts new game.
        self.addCharButton = tk.Button(self.charEntryFrame, text = "Add character", command = self.gridLetter)
        self.newGameButton = tk.Button(self.charEntryFrame, text = "New Game", command = self.newGameCommand)

        #Label placements.
        tk.Label(self.headerFrame, text = "SOS Game").pack(fill = 'x')
        tk.Label(self.headerFrame, text = "By Stephen Holman").pack(fill = 'x')

        tk.Label(self.redFrame, text = "Red Player", pady = 15).pack()
        self.redSButton.pack()
        self.redOButton.pack()
        self.redComputerBox.pack(pady = 10)

        tk.Label(self.blueFrame, text = "Blue Player", pady = 15).pack()
        self.blueSButton.pack()
        self.blueOButton.pack()
        self.blueComputerBox.pack(pady = 10)

        tk.Label(self.scoreFrame, text = "Red Score: ").pack(side = 'left')
        self.redScoreLabel.pack(side = 'left')
        self.blueScoreLabel.pack(side = 'right')
        tk.Label(self.scoreFrame, text = "Blue Score: ").pack(side = 'right')
        self.announceLabel.pack()
        self.turnLabel.pack()

        tk.Label(self.charEntryFrame, text = "X value:").grid(row = 0, column = 0)
        self.xEntry.grid(row = 0, column = 1)
        tk.Label(self.charEntryFrame, text = "Y value:").grid(row = 0, column = 2)
        self.yEntry.grid(row = 0, column = 3)
        self.addCharButton.grid(row = 1, column = 0, columnspan = 4, pady = 10)
        tk.Label(self.charEntryFrame, text = "Game Type:").grid(row = 2, column = 0)
        self.simpleButton.grid(row = 2, column = 1)
        self.complexButton.grid(row = 2, column = 2)
        self.newGameButton.grid(row = 2, column = 3)
        tk.Label(self.charEntryFrame, text = "New Game Grid Size: (From 5 to 10)").grid(row = 3, column = 0, columnspan = 3)
        self.gridSizeEntry.grid(row = 3, column = 3)

        #Playing grid canvas creation and placements. Default size is 8.
        self.gridCanvas = tk.Canvas(self.window, height = 160, width = 160)
        for y in range(0, 8):
            for x in range(0, 8):
                self.gridCanvas.create_rectangle(y*20, x*20, (y*20) + 20, (x*20) + 20, outline = "#000", fill = "#fff")
                x += 20
            y += 20

        #Places frames and gridCanvas within window.
        self.headerFrame.grid(row = 0, column = 1)
        self.redFrame.grid(row = 1, column = 0)
        self.gridCanvas.grid(row = 1, column = 1, sticky = "")
        self.blueFrame.grid(row = 1, column = 2)
        self.scoreFrame.grid(row = 2, column = 1)
        self.charEntryFrame.grid(row = 3, column = 1)

    #Method for adding letter to the grid in the GUI and finding new SOS patterns.
    def gridLetter(self):
        try:   
            selectedX = int(self.currentX.get()) - 1
            selectedY = int(self.currentY.get()) - 1
        #If the coordinates are not valid integers, edits announcement to reflect this and skips the
        #rest of the code in else section.
        except (TypeError, ValueError):
            self.currentGame.currentAnnounce = "Invalid entry"
        else:
            #Decides which letter to enter based on whose turn it is.
            selectedLetter = ""
            selectedColor = ""
            currentPlayer = True
            if (self.currentGame.currentTurn):
                selectedLetter = self.redSV.get()
                selectedColor = "#f00"
                currentPlayer = True
            else:
                selectedLetter = self.blueSV.get()
                selectedColor = "#00f"
                currentPlayer = False
            success = self.currentGame.placeLetter(selectedX, selectedY, selectedLetter)
            #Only places letter in labelGrid if GameLogic.placeLetter was successful.
            if (success):
                self.gridCanvas.create_text(selectedX*20 + 10, selectedY*20 + 10, text = selectedLetter)
                #Tests if SOS was formed in any direction if new letter was an S.
                if selectedLetter == "S":
                    for searchX in [-1,0,1]:
                        for searchY in [-1,0,1]:
                            scored = self.currentGame.findPatternForS(currentPlayer, selectedX + (2*searchX), selectedY + (2*searchY), selectedX + searchX, selectedY + searchY)
                            if (scored):
                                self.gridCanvas.create_line((selectedX * 20) + (searchX * 40) + 10, (selectedY * 20) + (searchY * 40) + 10, (selectedX * 20) + 10,(selectedY * 20) + 10, fill = selectedColor, width = 2)
                #Tests if SOS was formed in any direction if new letter was an O.
                elif selectedLetter == "O":
                    for searchX in [-1,0,1]:
                        scored = self.currentGame.findPatternForO(currentPlayer, selectedX + searchX, selectedY + 1, selectedX - searchX, selectedY - 1)
                        if (scored):
                            self.gridCanvas.create_line((selectedX * 20) + (searchX * 20) + 10, (selectedY * 20) + 30, (selectedX * 20) - (searchX * 20) + 10,(selectedY * 20) - 10, fill = selectedColor, width = 2)
                    scored = self.currentGame.findPatternForO(currentPlayer, selectedX + 1, selectedY, selectedX - 1, selectedY)
                    if (scored):
                        self.gridCanvas.create_line((selectedX * 20) - 10, (selectedY * 20) + 10, (selectedX * 20) + 30, (selectedY * 20) + 10, fill = selectedColor, width = 2)
                #Tests if the game is over using method distinct to SimpleGame or ComplexGame.
                self.currentGame.gameOver()
        finally:
            #Updates announcement and current turn.
            self.announceLabel.config(text = self.currentGame.currentAnnounce)
            self.redScoreLabel.config(text = self.currentGame.redScore)
            self.blueScoreLabel.config(text = self.currentGame.blueScore)
            self.turnLabel.config(text = self.currentGame.getTurnString())

    #Method for restarting game and resetting gridCanvas.
    def newGameCommand(self):
        try:
            nextGameSize = int(self.nextGridSizeVar.get())
        #If the nextGameSize is not a valid integer, announces failure and does not start new game.
        except (TypeError, ValueError):
            self.currentGame.currentAnnounce = "Invalid entry for grid size"
        else:
            if (nextGameSize >= 5 and nextGameSize <= 10):
                #Deletes currentGame and creates new one with ruleset and grid size from inputs.
                del self.currentGame
                if (self.nextGameType.get()):
                    self.currentGame = SimpleGame(nextGameSize, self.nextRedPlayer, self.nextBluePlayer)
                else:
                    self.currentGame = ComplexGame(nextGameSize, self.nextRedPlayer, self.nextBluePlayer)
                self.redScoreLabel.config(text = "0")
                self.blueScoreLabel.config(text = "0")
                #Resets gridCanvas.
                self.gridCanvas.delete("all")
                self.gridCanvas.config(width = nextGameSize * 20, height = nextGameSize * 20)
                for y in range(0, nextGameSize):
                    for x in range(0, nextGameSize):
                        self.gridCanvas.create_rectangle(y*20, x*20, (y*20) + 20, (x*20) + 20, outline = "#000", fill = "#fff")
                        x += 20
                    y += 20
            #If nextGameSize is outside of acceptable range, does not create new game.
            else:
                self.currentGame.currentAnnounce = "Grid size outside acceptable range"
        finally:
            self.announceLabel.config(text = self.currentGame.currentAnnounce)
            self.turnLabel.config(text = self.currentGame.getTurnString())