from Board import Board
from AI_Mover import Minimax

board = Board(input("\nX goes first. Choose your sign among(X and O): "))
ai = Minimax()
while(board.result == board.State.Pending):
    if(board.usersign == "X"): 
        cell = int(input(f"      {board.blue+board.bold}Give position(User): {board.norm}"))
        while (not board.is_valid_move(board.coordinates(cell))):
            cell = int(input(f"{board.blue+board.bold}Preoccupied or invalid cell. Give vaid position(User): {board.norm}"))
        board.user_mover(board.coordinates(cell))
        if(board.result != board.State.Pending):
            break
        board.ai_mover(ai.ai_mover(board))
    else :
        board.ai_mover(ai.ai_mover(board))
        if(board.result != board.State.Pending):
            break
        cell = int(input(f"      {board.blue+board.bold}Give position(User): {board.norm}"))
        while (not board.is_valid_move(board.coordinates(cell))):
            cell = int(input(f"{board.blue+board.bold}Preoccupied or invalid cell. Give vaid position(User): {board.norm}"))
        board.user_mover(board.coordinates(cell))
