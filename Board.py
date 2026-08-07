import os
import subprocess
from enum import Enum
import sys
import time


class Board:
    def __init__(self, user_sign: str):
        self.margin = "       "
        self.result = self.State.Pending
        self.glo = "\033[0m"
        self.red = "\033[91m"
        self.blue = "\033[94m"
        self.usersign = user_sign
        self.aisign = chr(79 + 88 - ord(user_sign))
        self.refresh_terminal()
        self.reset_board()

    @staticmethod
    def coordinates(pos: int)->tuple:
        return (pos // 3, pos % 3)

    def set(self):
        self.board = (
            f"{self.margin}  {self.hlit[0][0]}{self.cell[0][0]}{self.glo}  |  {self.hlit[0][1]}{self.cell[0][1]}{self.glo}  |  {self.hlit[0][2]}{self.cell[0][2]}{self.glo}  \n"
            f"{self.margin}-----------------\n"
            f"{self.margin}  {self.hlit[1][0]}{self.cell[1][0]}{self.glo}  |  {self.hlit[1][1]}{self.cell[1][1]}{self.glo}  |  {self.hlit[1][2]}{self.cell[1][2]}{self.glo}  \n"
            f"{self.margin}-----------------\n"
            f"{self.margin}  {self.hlit[2][0]}{self.cell[2][0]}{self.glo}  |  {self.hlit[2][1]}{self.cell[2][1]}{self.glo}  |  {self.hlit[2][2]}{self.cell[2][2]}{self.glo}  \n"
        )

    def slow_print(self, text, delay=0.0013):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush() 
            time.sleep(delay)   
        print() 

    def announcer(self):
        announce = (f"{self.ann_hol[0]}---------------------------------\n"
                    f"        {self.ann_hol[1]}        "
                    f"\n---------------------------------{self.glo}\n")
        glow_sequence = ["\033[2;37m","\033[0;37m", "\033[1;37m", "\033[0;37m"]
        for _ in range(5):
            for style in glow_sequence:
                sys.stdout.write(f"\r{style}{announce}\033[0m")
                sys.stdout.flush()
                time.sleep(0.15) 
                sys.stdout.write('\033[3F')
        sys.stdout.write('\033[3E')
        print()

    def printer(self):
        self.refresh_terminal()
        self.set()
        print('\033[?25l')
        self.slow_print(self.board)
        if(self.result == self.State.Draw):
            self.ann_hol[1] = "  IT IS A DRAW"
            self.announcer()
        elif(self.result == self.State.AI):
            self.ann_hol[0] = self.red
            self.ann_hol[1] = "ALAS! YOU LOST"
            self.announcer()
        elif(self.result == self.State.User):
            self.ann_hol[0] = self.blue
            self.ann_hol[1] = "HURRAY! YOU WIN"
            self.announcer()
        print('\033[?25h')


    def reset_board(self):
        self.refresh_terminal()
        self.result = self.State.Pending
        self.ann_hol = ["",""]
        self.cell = [["0", "1", "2"], 
                    ["3", "4", "5"], 
                    ["6", "7", "8"]]
        self.hlit = [["\033[38;2;100;100;100m","\033[38;2;100;100;100m","\033[38;2;100;100;100m"],
                    ["\033[38;2;100;100;100m","\033[38;2;100;100;100m","\033[38;2;100;100;100m"],
                    ["\033[38;2;100;100;100m","\033[38;2;100;100;100m","\033[38;2;100;100;100m"]]
        self.available_moves = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
        self.set()
        self.printer()


    def tester_mover(self, pos: tuple, sign: str):
        if self.result != self.State.Pending:
            return
        (i, j) = pos
        self.cell[i][j] = "\033[1m"+sign
        self.available_moves.remove((i , j))

    def ai_mover(self, pos: tuple):
        if self.result != self.State.Pending:
            return
        (i, j) = pos
        self.cell[i][j] = self.aisign
        self.available_moves.remove((i , j))
        self.referee()
        self.hlit[i][j] = "\033[91m"
        self.printer()

    def user_mover(self, pos: tuple):
        if self.result != self.State.Pending:
            return
        (i, j) = pos
        self.cell[i][j] = self.usersign
        self.available_moves.remove((i , j))
        self.referee()
        self.hlit[i][j] = "\033[94m"
        self.printer()

    def referee(self):
        if self.cell[0][0] == self.cell[0][1] == self.cell[0][2]:
            self.result = (self.State.AI if self.cell[0][0] == self.aisign else self.State.User) 
        elif self.cell[0][0] == self.cell[1][1] == self.cell[2][2]: #
            self.result = (self.State.AI if self.cell[0][0] == self.aisign else self.State.User) 
        elif self.cell[0][0] == self.cell[1][0] == self.cell[2][0]: #
            self.result = (self.State.AI if self.cell[0][0] == self.aisign else self.State.User)
        elif self.cell[1][0] == self.cell[1][1] == self.cell[1][2]: #
            self.result = (self.State.AI if self.cell[1][0] == self.aisign else self.State.User)
        elif self.cell[2][0] == self.cell[2][1] == self.cell[2][2]: #
            self.result = (self.State.AI if self.cell[2][0] == self.aisign else self.State.User) 
        elif self.cell[0][1] == self.cell[1][1] == self.cell[2][1]: #
            self.result = (self.State.AI if self.cell[0][1] == self.aisign else self.State.User) 
        elif self.cell[0][2] == self.cell[1][2] == self.cell[2][2]: #
            self.result = (self.State.AI if self.cell[0][2] == self.aisign else self.State.User)
        elif self.cell[0][2] == self.cell[1][1] == self.cell[2][0]:
            self.result = (self.State.AI if self.cell[0][2] == self.aisign else self.State.User) 
        else:
            self.result = (self.State.Draw if len(self.available_moves) == 0 else self.State.Pending)

    def undo_move(self, pos: tuple):
        self.available_moves.add(pos)
        self.cell[pos[0]][pos[1]] = str(pos[0]*3+pos[1])

    def is_valid_move(self, pos: tuple) -> bool:
        return pos in self.available_moves

    def refresh_terminal(self):
        if os.name == "nt":
            subprocess.run(["cls"], shell=True)
        else:
            print("\033[H\033[2J", end="")
        print("=================================")
        print("      CROSSES & NOUGHTS 3000     ")
        print("=================================")

    class State(Enum):
        AI = 0
        User = 1 
        Draw = 2
        Pending = 3