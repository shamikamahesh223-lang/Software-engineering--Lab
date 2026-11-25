SIZE = 8


def piece_owner(piece):
    return piece[0] if piece != "." else None


def is_king(piece):
    return piece.endswith("K")


def directions_for(piece, player):
    if is_king(piece):
        return ((-1, -1), (-1, 1), (1, -1), (1, 1))
    direction = -1 if player == "R" else 1
    return ((direction, -1), (direction, 1))


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if piece_owner(piece) != player or board[er][ec] != ".":
        return False
    return (er - sr, ec - sc) in directions_for(piece, player)


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if piece_owner(piece) != player or board[er][ec] != ".":
        return False
    dr, dc = er - sr, ec - sc
    if abs(dr) != 2 or abs(dc) != 2:
        return False
    allowed = {(2 * r, 2 * c) for r, c in directions_for(piece, player)}
    if (dr, dc) not in allowed:
        return False
    mr, mc = sr + dr // 2, sc + dc // 2
    return piece_owner(board[mr][mc]) not in (None, player)


def legal_moves(board, player, start=None, captures_only=False):
    moves = []
    positions = [start] if start is not None else [
        (r, c) for r in range(SIZE) for c in range(SIZE)
        if piece_owner(board[r][c]) == player
    ]
    for sr, sc in positions:
        piece = board[sr][sc]
        if piece_owner(piece) != player:
            continue
        for dr, dc in directions_for(piece, player):
            for distance in (2,) if captures_only else (1, 2):
                er, ec = sr + dr * distance, sc + dc * distance
                if not (0 <= er < SIZE and 0 <= ec < SIZE):
                    continue
                if distance == 2 and capture_move(board, player, (sr, sc), (er, ec)):
                    moves.append(((sr, sc), (er, ec)))
                elif distance == 1 and simple_move(board, player, (sr, sc), (er, ec)):
                    moves.append(((sr, sc), (er, ec)))
    return moves


def has_legal_moves(board, player):
    return bool(legal_moves(board, player))


def has_capture(board, player):
    return bool(legal_moves(board, player, captures_only=True))


def promote(board):
    promoted = []
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted.append("R")
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted.append("B")
    return promoted


def count_pieces(board, player):
    return sum(piece_owner(piece) == player for row in board for piece in row)
