from Board import Board


class Minimax:
    def minimax(self, board:Board, maximizing:bool, alpha, beta):
        match board.result:
            case Board.State.AI:
                return 10
            case Board.State.User:
                return -10
            case Board.State.Draw:
                return 0
            case Board.State.Pending:
                if maximizing:
                    best = float("-inf")            
                    for pos in board.available_moves:
                        board.tester_mover(pos, board.aisign)
                        score = self.minimax(board, False, alpha, beta)
                        board.undo_move(pos)
                        best = max(best, score)
                        alpha = max(best,alpha)
                        if alpha >= beta:
                            break
                    return best
                else:
                    best = float("inf")            
                    for pos in board.available_moves:
                        board.tester_mover(pos, board.usersign)
                        score = self.minimax(board, True, alpha, beta)
                        board.undo_move(pos)
                        best = min(best, score)
                        beta = min(best,beta)
                        if alpha >= beta:
                            break
                    return best

    def ai_mover(self, board:Board):
        best = float("-inf")
        move = None

        for pos in board.available_moves:
            board.tester_mover(pos, board.aisign)
            score = self.minimax(board, False, float("-inf"), float("inf"))
            board.undo_move(pos)
            if(score >= best):
                best = score
                move = pos

        return move