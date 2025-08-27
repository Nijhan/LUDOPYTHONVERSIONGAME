from utils.dice_utils import roll_dice as roll_dice_util
from utils.movement_utils import move_token as move_token_util

TOKENS_PER_PLAYER = 2
FINAL_POSITION = 20  # Short track for demo

class Player:
    def __init__(self, name):
        self.name = name
        self.tokens = [-1] * TOKENS_PER_PLAYER  # All tokens start in Yard

    def has_won(self):
        return all(pos >= FINAL_POSITION for pos in self.tokens)

class GameLogic:
    def __init__(self, players):
        self.players = players
        self.current_index = 0

    def get_current_player(self):
        return self.players[self.current_index]

    def roll_dice(self):
        return roll_dice_util()

    def move_token(self, player, roll):
        for i, pos in enumerate(player.tokens):
            if pos == -1 and roll == 6:
                player.tokens[i] = 0
                print(f"{player.name}'s token {i+1} entered the board!")
                return
            elif pos != -1:
                player.tokens[i] = move_token_util(pos, roll)
                print(f"{player.name}'s token {i+1} moved to {player.tokens[i]}")
                return
        print(f"{player.name} could not move any token.")

    def display_board(self):
        for player in self.players:
            status = ", ".join(str(t) if t != -1 else "Yard" for t in player.tokens)
            print(f"{player.name}: {status}")

    def check_winner(self, player):
        if player.has_won():
            print(f"\n🎉 {player.name} has won the game! 🎉")
            return player
        return None

    def next_turn(self):
        self.current_index = (self.current_index + 1) % len(self.players)
