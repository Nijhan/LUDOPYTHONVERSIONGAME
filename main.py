from game_logic import GameLogic

# Simple Player class
class Player:
    def __init__(self, name):
        self.name = name

def main():
    # create 2 players
    players = [Player("Najma"), Player("AI")]

    # start game
    game = GameLogic(players)

    winner = None
    while not winner:
        player = game.get_current_player()
        
        # roll dice
        roll = game.roll_dice()

        # move a token
        game.move_token(player, roll)

        # show board state
        game.display_board()

        # check for winner
        winner = game.check_winner(player)

        # switch turn
        game.next_turn()

if __name__ == "__main__":
    main()
