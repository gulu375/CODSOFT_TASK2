from Board import Board
from AI_Mover import Minimax

board = Board()                                                                                 # initializes the board
board.reset_game()                                                                              # used to reset the board or initialize the board
board.sign_setter(input("X goes first. Choose your desired sign to play among(X and O): "))     # used to set sign for the user
print("\033[1A\033[2K\033[2A")
ai = Minimax()                                                                                  # initializes the minimax                                                                                 
while(board.result == board.State.Pending):                                                     # input taking loops untill the game is over
    if(board.usersign == "X"):                                                                  # if user chooses X, user gets first turn
        cell = int(input(f"      {board.blue+board.bold}Give position(User): {board.norm}"))    # ask for input as the cell position
        while (not board.is_valid_move(board.coordinates(cell))):                               # keep asking for input if input is invalid
            cell = int(input(f"{board.blue+board.bold}Preoccupied or invalid cell. Give vaid position(User): {board.norm}"))
        board.user_mover(board.coordinates(cell))
        if(board.result != board.State.Pending):                                                # breaks the loop(input) if game is over
            break
        board.ai_mover(ai.ai_mover(board))
    else :                                                                                      # if user chooses O, AI gets first turn
        board.ai_mover(ai.ai_mover(board))
        if(board.result != board.State.Pending):
            break
        cell = int(input(f"      {board.blue+board.bold}Give position(User): {board.norm}"))    # ask for input as the cell position
        while (not board.is_valid_move(board.coordinates(cell))):                               # keep asking for input if input is invalid
            cell = int(input(f"{board.blue+board.bold}Preoccupied or invalid cell. Give vaid position(User): {board.norm}"))
        board.user_mover(board.coordinates(cell))
