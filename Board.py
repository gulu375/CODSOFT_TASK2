import os
import subprocess
from enum import Enum


class Board:
    def __init__(self, user_sign: str):
        self.margin = "       "
        self.cell = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.available_moves = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
        self.board = (
            f"{self.margin}  {self.cell[0][0]}  |  {self.cell[0][1]}  |  {self.cell[0][2]}  \n"
            f"{self.margin}-----------------\n"
            f"{self.margin}  {self.cell[1][0]}  |  {self.cell[1][1]}  |  {self.cell[1][2]}  \n"
            f"{self.margin}-----------------\n"
            f"{self.margin}  {self.cell[2][0]}  |  {self.cell[2][1]}  |  {self.cell[2][2]}  \n"
        )
        self.usersign = user_sign
        self.aisign = chr(79 + 88 - ord(user_sign))
        self.refresh_terminal()
        self.reset()

    @staticmethod
    def coordinates(pos: int)->tuple:
        return (pos % 10, pos // 10)

    def set(self):
        self.board = (
            f"{self.margin}  {self.cell[0][0]}  |  {self.cell[0][1]}  |  {self.cell[0][2]}  \n"
            f"{self.margin}-----------------\n"
            f"{self.margin}  {self.cell[1][0]}  |  {self.cell[1][1]}  |  {self.cell[1][2]}  \n"
            f"{self.margin}-----------------\n"
            f"{self.margin}  {self.cell[2][0]}  |  {self.cell[2][1]}  |  {self.cell[2][2]}  \n"
        )

    def reset(self):
        self.refresh_terminal()
        print(self.board)

    def load(self) -> bool:
        self.refresh_terminal()
        if len(self.available_moves) % 2 != 0 and len(self.available_moves) >= 5:
            res = self.check_result()
            if res == self.State.Pending:
                self.set()
                print(self.board)
                return False
            elif res == self.State.AI:
                print("Alas! You Lost.")
                return True
            elif res == self.State.User:
                print("Hurray! You Won.")
                return True
            else:
                print("It is a Draw.")
                return True
        else:
            self.set()
            print(self.board)
            return False

    def tester_mover(self, pos: tuple, sign: str):
        (i, j) = pos
        self.cell[i][j] = sign
        self.available_moves.remove((i , j))

    def ai_mover(self, pos: tuple) -> bool:
        (i, j) = pos
        self.cell[i][j] = self.aisign
        self.available_moves.remove((i , j))
        return self.load()

    def user_mover(self, pos: tuple) -> bool:
        (i, j) = pos
        self.cell[i][j] = self.usersign
        self.available_moves.remove((i , j))
        return self.load()

    def check_result(self) -> int:
        if self.cell[0][0] == self.cell[0][1] == self.cell[0][2] != " ":
            return self.State.AI if self.cell[0][0] == self.aisign else self.State.User 
        elif self.cell[0][0] == self.cell[1][1] == self.cell[2][2] != " ":
            return self.State.AI if self.cell[0][0] == self.aisign else self.State.User 
        elif self.cell[0][0] == self.cell[1][0] == self.cell[2][0] != " ":
            return self.State.AI if self.cell[0][0] == self.aisign else self.State.User 
        elif self.cell[1][0] == self.cell[1][1] == self.cell[1][2] != " ":
            return self.State.AI if self.cell[1][0] == self.aisign else self.State.User 
        elif self.cell[2][0] == self.cell[2][1] == self.cell[2][2] != " ":
            return self.State.AI if self.cell[2][0] == self.aisign else self.State.User 
        elif self.cell[0][1] == self.cell[1][1] == self.cell[2][1] != " ":
            return self.State.AI if self.cell[0][1] == self.aisign else self.State.User 
        elif self.cell[0][2] == self.cell[1][2] == self.cell[2][2] != " ":
            return self.State.AI if self.cell[0][2] == self.aisign else self.State.User 
        elif self.cell[0][2] == self.cell[1][1] == self.cell[2][0] != " ":
            return self.State.AI if self.cell[0][2] == self.aisign else self.State.User 
        else:
            return self.State.Draw if len(self.available_moves) == 0 else self.State.Pending

    def undo_move(self, pos: tuple):
        self.available_moves.add(pos)
        self.cell[pos[0]][pos[1]] = " "

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


