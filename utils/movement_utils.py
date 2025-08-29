def move_token(position, roll, track_length=20):
    """Move token based on current position and dice roll"""
    # If token is in Yard (-1) and rolled 6, enter the board
    if position == "Yard" and roll == 6:
        return 1
    
    # If token is on track, move forward
    if isinstance(position, int):
        new_pos = position + roll
        # Don't go beyond track length
        if new_pos > track_length:
            return track_length
        return new_pos
    
    # Token stays in yard if not rolled 6
    return position

def can_move_token(position, roll):
    """Check if token can move with given roll"""
    if position == "Yard":
        return roll == 6
    return isinstance(position, int)