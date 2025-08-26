# game_logic.py
from utils.dice_utils import roll_dice
from utils.movement_utils import move_token

PLAYERS = ["Red", "Green", "Yellow", "Blue"]
TOKENS_PER_PLAYER = 4

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.tokens = [-1] * TOKENS_PER_PLAYER  # -1 = yard

    def __str__(self):
        return f"{self.name} ({self.color})"

def play_game():
    print("🎲 Welcome to Ludo (Game Logic) 🎲")

    # Setup players
    num_players = 2
    players = [Player("P1", "Red"), Player("P2", "Green")]

    current = 0
    while True:
        player = players[current]
        input(f"\n{player}'s turn → press ENTER to roll dice")
        dice = roll_dice()
        print(f"{player} rolled {dice}")

        # always move first token for now
        idx = 0
        old = player.tokens[idx]
        if old == -1 and dice == 6:
            player.tokens[idx] = 0
            print(f"Token entered the board!")
        elif old != -1:
            player.tokens[idx] = move_token(old, dice)
            print(f"Token moved from {old} to {player.tokens[idx]}")
        else:
            print("Need a 6 to leave yard.")

        # Extra turn on 6
        if dice != 6:
            current = (current + 1) % len(players)

if __name__ == "__main__":
    play_game()
