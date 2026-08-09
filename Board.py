import os
import subprocess
from enum import Enum
import sys
import time

class Board:
    def __init__(self):
        '''
        Constructor:
            * Initializes necessary variables.
            * Refreshes the terminal.
            * Resets the board.
        '''
        self.margin = "        "                        # used for indentation on the left of the board to maintain symmetry
        self.dim = "\033[2m"                            # used to dim text in terminal
        self.norm = "\033[0m"                           # used to reset the text fromat in terminal
        self.red = "\033[91m"                           # used to red the text in terminal
        self.blue = "\033[94m"                          # used to blue the text in terminal
        self.bold = "\033[1m"                           # used to bold the text in terminal
        self.honeydew = "\033[38;5;150m"                # used to honeydew the text in terminal

    @staticmethod
    def coordinates(pos: int)->tuple:
        """
        2d coordinates of the cell number.

        Parameters:
            pos (int) : Single valued cell number.

        Returns:
            return (tuple) : Coordinates of the cell.
        """
        return (pos // 3, pos % 3)                      # converts cell[pos] to cell[i][j]

    def sign_setter(self, user_sign = "X"):
        """
        Set signs to user and AI.
        X goes first in the game.
        """
        self.usersign = user_sign                       # stores the sign(X or O) chosen by user
        self.aisign = chr(79 + 88 - ord(self.usersign)) # stores other sign to the ai

        

    def update_board(self):
        '''
        Updates the board with new format and variables.
        Generally used after every move.
        '''
        self.board = (
            f"{self.margin}  {self.hlit[0][0]}{self.cell[0][0]}{self.norm}  |  {self.hlit[0][1]}{self.cell[0][1]}{self.norm}  |  {self.hlit[0][2]}{self.cell[0][2]}{self.norm}  \n"
            f"{self.margin}-----------------\n"
            f"{self.margin}  {self.hlit[1][0]}{self.cell[1][0]}{self.norm}  |  {self.hlit[1][1]}{self.cell[1][1]}{self.norm}  |  {self.hlit[1][2]}{self.cell[1][2]}{self.norm}  \n"
            f"{self.margin}-----------------\n"
            f"{self.margin}  {self.hlit[2][0]}{self.cell[2][0]}{self.norm}  |  {self.hlit[2][1]}{self.cell[2][1]}{self.norm}  |  {self.hlit[2][2]}{self.cell[2][2]}{self.norm}  \n"
        )

    @staticmethod
    def slow_print(text, delay=0.0013):
        '''
        Animates the updating of the board.

        Parameters: 
            delay (float) : delay between printing each character
        '''
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush() 
            time.sleep(delay)   
        print() 

    def announcer(self):
        '''
        Announces the result of the game.
        '''
        announce = (f"{self.announcement_color}       -------------------\n"     #        -------------------
                    f"         {self.announcement_text}"                         #         Result of the Game
                    f"\n       -------------------{self.norm}\n")                #        -------------------
        normw_sequence = ["\033[2;37m","\033[0;37m", "\033[1;37m", "\033[0;37m"] # list of dimming and lighting sequences
        for _ in range(5):
            for style in normw_sequence:
                sys.stdout.write(f"\r{style}{announce}\033[0m")
                sys.stdout.flush()
                time.sleep(0.15) 
                sys.stdout.write('\033[3F')
        sys.stdout.write('\033[3E')
        print()

    def highlighter(self):
        '''
        Highlights the winning row/col/diagonal and dim all the others.
        '''
        self.reset_highlighter()                                            # dims every cell
        highlit = self.blue if self.result == self.State.User else self.red
        for pos in self.win_row:
            self.hlit[pos[0]][pos[1]] = self.bold+highlit                   # highlights only the winning row/col/diagonal
        for pos in self.available_moves:
            self.cell[pos[0]][pos[1]] = " "                                 # blancks the every unused cells

    def diaplayer(self, rapid = False, pos = ()):
        '''
        Displayes the board after every move. 
        Calls the announcer if the game is over.

        Parameters:
            rapid (bool) : Checks if animation will be applied. By default, false.
            pos (tuple) :  Passes position of the last move. Generally used by AI mover.
        '''
        self.refresh_terminal()                     # refreshes the terminal to erase the old board.
        if(self.result != self.State.Pending):
            self.highlighter()                      # calls the highlighter if the game is over.
        self.update_board()                         # updates the board before displaying
        print('\033[?25l')
        if rapid:                                   # if the move was of AI, it skips the animation and print instantly
            print(self.board,end="\n\n")
            print(self.red, self.bold,"       ","AI chooses:",self.norm,"\b\b",pos[0]*3+pos[1], end="\n")
            print("        -----------------",end='')
        else:                                       # if the move was of User, it prints the board with animation
            self.slow_print(self.board)
            print("\n\n")                                            
        if(self.result == self.State.Draw):                 #
            self.announcement_text = "OH! IT'S A DRAW"      #
            self.announcer()                                #
        elif(self.result == self.State.AI):                 #
            self.announcement_color = self.red              # Updates the announcement text and color according to the result, calls announcer.                                                            # This happens if and only if the game is over.
            self.announcement_text = "ALAS!! YOU LOST"      # Calls the announcer.
            self.announcer()                                #
        elif(self.result == self.State.User):               #
            self.announcement_color = self.blue             #
            self.announcement_text = "HURRAY! YOU WIN"      #
            self.announcer()                                #

        print('\033[?25h')                                  # invisibles the cursor in terminal before printing the board.

    def reset_highlighter(self):
        '''
        Dims every cell of the board.
        Generally used before highlighting the winning row/col/diagonal.
        '''
        self.hlit = [[self.dim,self.dim,self.dim],
                    [self.dim,self.dim,self.dim],
                    [self.dim,self.dim,self.dim]]

    def reset_game(self):
        '''
        Resets or sets the game to a new beginning.
        '''
        self.result = self.State.Pending                # keeps result of the game after every move
        self.win_row = {}                               # stores the winning row/col/diagonal 
        self.announcement_color = ""                    # stores the announcement color
        self.announcement_text = ""                     # stores the announcement text
        self.cell = [["0", "1", "2"],                   # stores the cell number to display the user
                    ["3", "4", "5"], 
                    ["6", "7", "8"]]
        self.hlit = [[self.dim,self.dim,self.dim],      # stores the format of cells
                    [self.dim,self.dim,self.dim],
                    [self.dim,self.dim,self.dim]]
        self.available_moves = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)} # stores and keeps track of available moves after every move
        self.update_board()                             # updates the board after resetting the game
        self.diaplayer()                                # displays the board after the resetting


    def tester_mover(self, pos: tuple, sign: str):
        '''
        Al uses this to temporarily make a move. 

        Parameters:
            pos (tuple) : Passes the chosen cell position by AI
            sign (str) : Passes the alloted sign to the AI
        '''
        if self.result != self.State.Pending:           # checks if the the game is not over
            return
        self.cell[pos[0]][pos[1]] = sign                # set sign to the cell
        self.available_moves.remove(pos)                # removes the cell from the available moves
        self.referee()                                  # calls the referee to check the result

    def ai_mover(self, pos: tuple):
        '''
        Ai uses this to execute it's confirmed move.

        Parameters:
            pos (tuple) : Passes the cell position chosen by the AI
        '''
        if self.result != self.State.Pending:           # checks if the the game is not over
            return
        self.cell[pos[0]][pos[1]] = self.aisign         # marks the cell
        self.available_moves.remove((pos[0] , pos[1]))  # removes the cell from available moves
        self.win_row = self.referee()                   # gets the winning row is the game is over
        self.hlit[pos[0]][pos[1]] = self.bold+self.red  # changes the format of the cell
        self.diaplayer(rapid=True, pos=pos)             # calls the displayer

    def user_mover(self, pos: tuple):
        '''
        Implements the move chosen by the user.

        Parameters:
            pos (tuple) : Passes the cell position chosen by the user.
        '''
        if self.result != self.State.Pending:           # checks if the the game is not over
            return
        self.cell[pos[0]][pos[1]] = self.usersign       # marks the cell
        self.available_moves.remove((pos[0], pos[1]))   # removes the cell from available moves
        self.win_row = self.referee()                   # gets the winning row is the game is over
        self.hlit[pos[0]][pos[1]] = self.bold+self.blue # changes the format of the cell
        self.diaplayer()                                # calls the displayer

    def referee(self) -> set[tuple]:
        '''
        * Checks if the game comes to a result.
        * Stores the result to the result variable.
        * Returns the winning row/col/diagonal.
        Returns:
            set[tuple] : The winning row/col/diagonal.
        '''
        if self.cell[0][0] == self.cell[0][1] == self.cell[0][2]:
            self.result = (self.State.AI if self.cell[0][0] == self.aisign else self.State.User)
            return {(0,0), (0,1), (0,2)} 
        elif self.cell[0][0] == self.cell[1][1] == self.cell[2][2]:
            self.result = (self.State.AI if self.cell[0][0] == self.aisign else self.State.User)
            return {(0,0), (1,1), (2,2)} 
        elif self.cell[0][0] == self.cell[1][0] == self.cell[2][0]: 
            self.result = (self.State.AI if self.cell[0][0] == self.aisign else self.State.User)
            return {(0,0), (1,0), (2,0)} 
        elif self.cell[1][0] == self.cell[1][1] == self.cell[1][2]:
            self.result = (self.State.AI if self.cell[1][0] == self.aisign else self.State.User)
            return {(1,0), (1,1), (1,2)} 
        elif self.cell[2][0] == self.cell[2][1] == self.cell[2][2]: 
            self.result = (self.State.AI if self.cell[2][0] == self.aisign else self.State.User) 
            return {(2,0), (2,1), (2,2)} 
        elif self.cell[0][1] == self.cell[1][1] == self.cell[2][1]:
            self.result = (self.State.AI if self.cell[0][1] == self.aisign else self.State.User) 
            return {(0,1), (1,1), (2,1)} 
        elif self.cell[0][2] == self.cell[1][2] == self.cell[2][2]:
            self.result = (self.State.AI if self.cell[0][2] == self.aisign else self.State.User)
            return {(0,2), (1,2), (2,2)} 
        elif self.cell[0][2] == self.cell[1][1] == self.cell[2][0]:
            self.result = (self.State.AI if self.cell[0][2] == self.aisign else self.State.User) 
            return {(0,2), (1,1), (2,0)} 
        else:
            self.result = (self.State.Draw if len(self.available_moves) == 0 else self.State.Pending)
            return {} 


    def undo_move(self, pos: tuple):
        '''
        Removes the move and retrives the previous state of the board.

        Parameters:
            pos (tuple) : Passes the position to the to undo
        '''
        self.available_moves.add(pos)                               # adds the position to the available moves
        self.cell[pos[0]][pos[1]] = str(pos[0]*3+pos[1])            # replace the marking of the cell with cell number
        self.result = self.State.Pending                            # keeps the result state pending

    def is_valid_move(self, pos: tuple) -> bool:
        '''
        Checks if the given position is available to play.

        Parameters:
            pos (tuple): Passes the position to check.
        
        Returns:
            bool : Returns true if available, else false otherwise.
        '''
        return pos in self.available_moves                          # checks if the position is in available moves

    def refresh_terminal(self):
        '''
        Prints banner of the game
        Erase the previous prints from the terminal.
        Generally used before printng new updated board.
        '''
        if os.name == "nt":                                         # checks if the os is Windows or macos
            subprocess.run(["cls"], shell=True)
        else:
            print("\033[H\033[2J", end="")
        print("==================================")                                              #  ==================================
        print(f"\033[1m----- {self.honeydew}CROSSES & NOUGHTS 3000{self.norm} -----\033[0m")     #  ----- CROSSES & NOUGHTS 3000 -----
        print("==================================")                                              #  ==================================

    class State(Enum):
        AI = 0
        User = 1 
        Draw = 2
        Pending = 3