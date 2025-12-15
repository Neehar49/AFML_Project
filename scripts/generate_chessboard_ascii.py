"""Generate an ASCII chess board with starting positions using 11x11 tiles."""
from pathlib import Path

TILES = {
    "EMPTY_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
    ],
    "EMPTY_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
    ],
    "W_KING_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        ".....+.....",
        "....███....",
        "...█████...",
        "....███....",
        "...█████...",
        "...█████...",
        "..███████..",
    ],
    "W_KING_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "     +     ",
        "    ███    ",
        "   █████   ",
        "    ███    ",
        "   █████   ",
        "   █████   ",
        "  ███████  ",
    ],
    "W_QUEEN_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "....<*>....",
        "....███....",
        "...█████...",
        "....███....",
        "...█████...",
        "...█████...",
        "..███████..",
    ],
    "W_QUEEN_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "    <*>    ",
        "    ███    ",
        "   █████   ",
        "    ███    ",
        "   █████   ",
        "   █████   ",
        "  ███████  ",
    ],
    "W_BISHOP_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "....███....",
        "...█/███...",
        "...█████...",
        "....███....",
        "....███....",
        "...█████...",
        "..███████..",
    ],
    "W_BISHOP_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "    ███    ",
        "   █/███   ",
        "   █████   ",
        "    ███    ",
        "    ███    ",
        "   █████   ",
        "  ███████  ",
    ],
    "W_KNIGHT_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        ".....N.....",
        "...██/█....",
        "..██████...",
        "..██.......",
        "..████.....",
        "..██████...",
        "..███████..",
    ],
    "W_KNIGHT_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "     N     ",
        "   ██/█    ",
        "  ██████   ",
        "  ██       ",
        "  ████     ",
        "  ██████   ",
        "  ███████  ",
    ],
    "W_ROOK_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...█ █ █...",
        "...█████...",
        "....███....",
        "....███....",
        "...█████...",
        "..███████..",
    ],
    "W_ROOK_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "   █ █ █   ",
        "   █████   ",
        "    ███    ",
        "    ███    ",
        "   █████   ",
        "  ███████  ",
    ],
    "W_PAWN_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "....███....",
        "...███|█...",
        "...███|█...",
        "....███....",
        "...█████...",
        "..███████..",
    ],
    "W_PAWN_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "    ███    ",
        "   ███|█   ",
        "   ███|█   ",
        "    ███    ",
        "   █████   ",
        "  ███████  ",
    ],
    "B_KING_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        ".....+.....",
        "....┃┃┃....",
        "...┃┃┃┃┃...",
        "....┃┃┃....",
        "...┃┃┃┃┃...",
        "...┃┃┃┃┃...",
        "..┃┃┃┃┃┃┃..",
    ],
    "B_KING_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "     +     ",
        "    ┃┃┃    ",
        "   ┃┃┃┃┃   ",
        "    ┃┃┃    ",
        "   ┃┃┃┃┃   ",
        "   ┃┃┃┃┃   ",
        "  ┃┃┃┃┃┃┃  ",
    ],
    "B_QUEEN_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "....<*>....",
        "....┃┃┃....",
        "...┃┃┃┃┃...",
        "....┃┃┃....",
        "...┃┃┃┃┃...",
        "...┃┃┃┃┃...",
        "..┃┃┃┃┃┃┃..",
    ],
    "B_QUEEN_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "    <*>    ",
        "    ┃┃┃    ",
        "   ┃┃┃┃┃   ",
        "    ┃┃┃    ",
        "   ┃┃┃┃┃   ",
        "   ┃┃┃┃┃   ",
        "  ┃┃┃┃┃┃┃  ",
    ],
    "B_BISHOP_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "....┃┃┃....",
        "...┃/┃┃┃...",
        "...┃┃┃┃┃...",
        "....┃┃┃....",
        "....┃┃┃....",
        "...┃┃┃┃┃...",
        "..┃┃┃┃┃┃┃..",
    ],
    "B_BISHOP_BLACK": [
        "           ",
        "           ",
        "           ",        
        "           ",
        "    ┃┃┃    ",
        "   ┃/┃┃┃   ",
        "   ┃┃┃┃┃   ",
        "    ┃┃┃    ",
        "    ┃┃┃    ",
        "   ┃┃┃┃┃   ",
        "  ┃┃┃┃┃┃┃  ",
    ],
    "B_KNIGHT_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        ".....N.....",
        "...┃┃/┃....",
        "..┃┃┃┃┃┃...",
        "..┃┃.......",
        "..┃┃┃┃.....",
        "..┃┃┃┃┃┃...",
        "..┃┃┃┃┃┃┃..",
    ],
    "B_KNIGHT_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "     N     ",
        "   ┃┃/┃    ",
        "  ┃┃┃┃┃┃   ",
        "  ┃┃       ",
        "  ┃┃┃┃     ",
        "  ┃┃┃┃┃┃   ",
        "  ┃┃┃┃┃┃┃  ",
    ],
    "B_ROOK_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "...┃ ┃ ┃...",
        "...┃┃┃┃┃...",
        "....┃┃┃....",
        "....┃┃┃....",
        "...┃┃┃┃┃...",
        "..┃┃┃┃┃┃┃..",
    ],
    "B_ROOK_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "   ┃ ┃ ┃   ",
        "   ┃┃┃┃┃   ",
        "    ┃┃┃    ",
        "    ┃┃┃    ",
        "   ┃┃┃┃┃   ",
        "  ┃┃┃┃┃┃┃  ",
    ],
    "B_PAWN_WHITE": [
        "...........",
        "...........",
        "...........",
        "...........",
        "...........",
        "....┃┃┃....",
        "...┃┃┃|┃...",
        "...┃┃┃|┃...",
        "....┃┃┃....",
        "...┃┃┃┃┃...",
        "..┃┃┃┃┃┃┃..",
    ],
    "B_PAWN_BLACK": [
        "           ",
        "           ",
        "           ",
        "           ",
        "           ",
        "    ┃┃┃    ",
        "   ┃┃┃|┃   ",
        "   ┃┃┃|┃   ",
        "    ┃┃┃    ",
        "   ┃┃┃┃┃   ",
        "  ┃┃┃┃┃┃┃  ",
    ],
}

FILES = {
    ("b", "king"): ("B_KING_WHITE", "B_KING_BLACK"),
    ("b", "queen"): ("B_QUEEN_WHITE", "B_QUEEN_BLACK"),
    ("b", "rook"): ("B_ROOK_WHITE", "B_ROOK_BLACK"),
    ("b", "bishop"): ("B_BISHOP_WHITE", "B_BISHOP_BLACK"),
    ("b", "knight"): ("B_KNIGHT_WHITE", "B_KNIGHT_BLACK"),
    ("b", "pawn"): ("B_PAWN_WHITE", "B_PAWN_BLACK"),
    ("w", "king"): ("W_KING_WHITE", "W_KING_BLACK"),
    ("w", "queen"): ("W_QUEEN_WHITE", "W_QUEEN_BLACK"),
    ("w", "rook"): ("W_ROOK_WHITE", "W_ROOK_BLACK"),
    ("w", "bishop"): ("W_BISHOP_WHITE", "W_BISHOP_BLACK"),
    ("w", "knight"): ("W_KNIGHT_WHITE", "W_KNIGHT_BLACK"),
    ("w", "pawn"): ("W_PAWN_WHITE", "W_PAWN_BLACK"),
}


def square_color(file_index: int, rank_index: int) -> str:
    """Return 'white' or 'black' for the square background.

    Files and ranks are zero-indexed from the white player's perspective,
    with file_index 0 corresponding to column 'a' and rank_index 0 to rank 1.
    """
    return "white" if (file_index + rank_index) % 2 == 0 else "black"


def starting_board():
    rank8 = ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"]
    rank7 = ["b_pawn"] * 8
    empty = [None] * 8
    rank2 = ["w_pawn"] * 8
    rank1 = ["w_rook", "w_knight", "w_bishop", "w_queen", "w_king", "w_bishop", "w_knight", "w_rook"]
    return [rank8, rank7, empty, empty, empty, empty, rank2, rank1]


def tile_for(square_piece, file_idx, rank_idx):
    color = square_color(file_idx, rank_idx)
    if square_piece is None:
        key = "EMPTY_WHITE" if color == "white" else "EMPTY_BLACK"
        return TILES[key]

    player, piece = square_piece.split("_", 1)
    tile_keys = FILES[(player[0], piece)]
    key = tile_keys[0] if color == "white" else tile_keys[1]
    return TILES[key]


def render_board(board):
    top = "++" + "=" * 88 + "++"
    rail = "++" + "-" * 88 + "++"
    lines = [top, rail]

    for rank_idx, rank in enumerate(board):
        tile_rows = ["" for _ in range(11)]
        board_rank_index = 7 - rank_idx  # convert to white's perspective (rank 1 index 0)
        for file_idx, square_piece in enumerate(rank):
            tile = tile_for(square_piece, file_idx, board_rank_index)
            for i, tile_line in enumerate(tile):
                tile_rows[i] += tile_line
        lines.extend(["||" + row + "||" for row in tile_rows])
    lines.extend([rail, top])
    return "\n".join(lines)


def main():
    board = starting_board()
    ascii_board = render_board(board)
    out_path = Path("data/chess_board_start.txt")
    out_path.write_text(ascii_board)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
