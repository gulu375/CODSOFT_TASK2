from Board import Board


class Minimax:
    def minimax(self, board:Board, maximizing:bool, alpha:float, beta:float) -> int:
        '''
        Recursively evaluates possible game states using the Minimax algorithm
        with Alpha-Beta pruning to determine the optimal move for the AI.

        Parameters:
            board (Board) : Passes the board object.
            maximizing (bool) : Passes the purpose. Either maximize or minimaize the score.
            alpha (float) : Passes the best score the maximizing player can guarantee so far
            beta (float) : Passes the best score the minimizing player can guarantee so far
        
        Returns:
            int: Returns best possible score in current state
        '''
        match board.result:
            case Board.State.AI:
                return 10                                                   # returns 10 if ai wins
            case Board.State.User:
                return -10                                                  # returns -10 if user wins
            case Board.State.Draw:
                return 0                                                    # returns 0 is its a draw
            case Board.State.Pending:
                if maximizing:                                              # checks if have maximize the score
                    best = float("-inf")                                    # initally keeps best score to negetive infinity            
                    for pos in board.available_moves:                       # iterates for every available moves
                        board.tester_mover(pos, board.aisign)               # temporarily plays the move
                        score = self.minimax(board, False, alpha, beta)     # explores further possibilities after the move and gets best possible score
                        board.undo_move(pos)                                # undo the move
                        best = max(best, score)                             # keeps track of best score in current loop
                        alpha = max(best,alpha)                             # keeps track of best score so far for maximizing 
                        if alpha >= beta:                                   # checks if best score so far better is better than user
                            break
                    return best                                             # returns the best score
                else:                                                       # checks if have minimize the score
                    best = float("inf")                                     # initally keeps best score to positive infinity
                    for pos in board.available_moves:                       # iterates for every available moves
                        board.tester_mover(pos, board.usersign)             # temporarily plays the move
                        score = self.minimax(board, True, alpha, beta)      # explores further possibilities after the move and gets best possible score
                        board.undo_move(pos)                                # undo the move
                        best = min(best, score)                             # keeps track of least score in current loop
                        beta = min(best,beta)                               # keeps track of least score so far for minimizing 
                        if alpha >= beta:
                            break
                    return best                                             # returns the best least score

    def ai_mover(self, board:Board)-> tuple:
        '''
        Determines the optimal move for the AI by evaluating all available moves
        using the Minimax algorithm with Alpha-Beta pruning, then returns the
        position with the highest score.

        Parameters:
            board (Board) : Passes the board object.
        
        Returns:
            tuple : Returns the best possible move in current state
        '''
        best = float("-inf")                                                # initally keeps best score to negetive infinity  
        move = None                                                         # keeps the move to none

        for pos in board.available_moves:                                   # iterates for every available moves
            board.tester_mover(pos, board.aisign)                           # temporarily plays the move
            score = self.minimax(board, False, float("-inf"), float("inf")) # explores further possibilities after the move and gets best possible score
            board.undo_move(pos)                                            # undo the move
            if(score >= best):                                              # checks if current score is the best. If it is, then updates the best and collect the move
                best = score
                move = pos

        return move                                                         # returns the best possible move in current state