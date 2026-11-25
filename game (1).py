from board import initial_board, move_piece, remove_piece, SIZE
from rules import capture_move, simple_move, legal_moves, has_capture, has_legal_moves, promote, count_pieces


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def opponent(self):
        return "B" if self.player == "R" else "R"

    def apply_capture(self, start, end):
        sr, sc = start
        er, ec = end
        mr, mc = (sr + er) // 2, (sc + ec) // 2
        move_piece(self.board, start, end)
        remove_piece(self.board, (mr, mc))

    def process_move(self, start, end):
        forced = has_capture(self.board, self.player)
        if forced and not capture_move(self.board, self.player, start, end):
            return False, "A capture is available; you must capture."
        if capture_move(self.board, self.player, start, end):
            self.apply_capture(start, end)
            promoted = promote(self.board)
            return True, ("capture", bool(promoted))
        if simple_move(self.board, self.player, start, end) and not forced:
            move_piece(self.board, start, end)
            promoted = promote(self.board)
            return True, ("move", bool(promoted))
        return False, "Invalid move."

    def run(self):
        print("Checkers — move: sr sc er ec (q to quit)")
        while True:
            if count_pieces(self.board, self.player) == 0 or not has_legal_moves(self.board, self.player):
                self.print_board()
                print(f"Game over — {self.opponent()} wins.")
                return
            self.print_board()
            raw = input(f"{self.player}> ").strip().lower().split()
            if raw == ["q"]:
                print("Game quit.")
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue
            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue
            accepted, result = self.process_move((sr, sc), (er, ec))
            if not accepted:
                print(result)
                continue
            action, promoted = result
            message = "Captured an opponent piece." if action == "capture" else "Moved successfully."
            if promoted:
                message += " Promoted to king."
            print(message)
            winner = self.opponent() if count_pieces(self.board, self.opponent()) == 0 or not has_legal_moves(self.board, self.opponent()) else None
            if winner:
                self.print_board()
                print(f"Game over — {winner} wins.")
                return
            if action == "capture" and not promoted:
                landing = (er, ec)
                if any(m_start == landing for m_start, _ in legal_moves(self.board, self.player, captures_only=True)):
                    print("Another capture is available — continue your turn.")
                    continue
            self.player = self.opponent()
