# utils/movement_utils.py

def move_token(position, steps, board_size=52):
    """
    Move a token along the board.
    - position = current position (-1 means token in yard)
    - steps = dice roll
    - board_size = number of spaces on the board (default 52 for Ludo)

    Returns new position.
    """
    if position == -1:
        return -1
    return (position + steps) % board_size
