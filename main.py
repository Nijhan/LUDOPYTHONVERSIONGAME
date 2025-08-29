from game_logic import GameLogic, Player

def main():
    # Two players
    players = [Player("Najma"), Player("Adrian")]

    # Initialize game
    game = GameLogic(players)

    winner = None
    print("🎲 Ludo Demo 🎲 Track ends at 20 for quick play. Each player has 2 tokens.")
    while not winner:
        player = game.get_current_player()
        input(f"\n{player.name}'s turn → press ENTER to roll dice")
        roll = game.roll_dice()
        print(f"{player.name} rolled: {roll}")

        game.move_token(player, roll)
        game.display_board()

        winner = game.check_winner(player)
        game.next_turn()

if __name__ == "__main__":
    main()