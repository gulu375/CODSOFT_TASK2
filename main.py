from Board import Board
from AI_Mover import Minimax

board = Board('X')
ai = Minimax()
while(board.result == board.State.Pending):
    cell = int(input("Give position(User): "))
    while (not board.is_valid_move(board.coordinates(cell))):
        cell = int(input("Preoccupied or invalid cell. Give vaid position(User): "))
    board.user_mover(board.coordinates(cell))
    if(board.result != board.State.Pending):
        break
    board.ai_mover(ai.ai_mover(board))
