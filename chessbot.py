import chess


PIECE_VALUES = {
    chess.PAWN: 1,
    chess.BISHOP: 3,
    chess.KNIGHT: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


class ChessBot:
    def __init__(self, depth):
        self.depth = depth
        self.board = chess.Board()
        self.next_move = None

        # tracks the material advantage for white
        self.material_score = 0

    def load_position(self, fen_string, material_score):
        self.board = chess.Board(fen=fen_string)
        self.material_score = material_score

    def get_material_diff(self, move):
        # material diff is positive if it is white's turn, 
        # negative if black's turn
        sign = 1 if self.board.turn == chess.WHITE else -1
        
        if self.board.is_en_passant(move):
            return sign

        val = 0
        if piece := move.promotion:
            # note can capture and promote in the same move
            val += sign*(PIECE_VALUES[piece] - 1)

        if self.board.is_capture(move):
            piece = self.board.piece_type_at(move.to_square)
            val += sign*PIECE_VALUES[piece]
    
        return val

    def make_move_from_san(self, s):
        self.make_move(self.board.parse_san(s))

    def make_move(self, move):
        diff = self.get_material_diff(move)
        self.board.push(move)
        self.material_score += diff
        
    def undo_move(self):
        move = self.board.pop()
        diff = self.get_material_diff(move)
        self.material_score -= diff
        
    def heuristic(self):
        # returns the heuristic score for WHITE
        if not self.board.is_game_over():
            return self.material_score

        outcome = self.board.outcome()
        if not outcome.winner:
            return 0 # draw
        elif outcome.winner == chess.WHITE:
            return float("Inf")
        elif outcome.winner == chess.BLACK:
            return float("-Inf")

    def negamax(self, d, alpha, beta, color):
        if d == 0:
            return color*self.heuristic()

        best_move_val, value = float("-Inf"), float("-Inf")
        for move in self.board.legal_moves:
            self.make_move(move)
            value = max(value, -self.negamax(d-1, -beta, -alpha, -color))
            self.undo_move()

            if d == self.depth and value > best_move_val:
                self.next_move = move
                best_move_val = value

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    def compute_next_move(self):
        if self.board.turn == chess.WHITE:
            self.negamax(self.depth, float("-Inf"), float("Inf"), 1)
        else:
            self.negamax(self.depth, float("-Inf"), float("Inf"), -1)

        if self.next_move:
            return self.board.san(self.next_move)
        else:
            # can't find anything that doesn't lead to checkmate
            # just return any legal move
            return self.board.san(list(self.board.legal_moves)[0])


       

        



    