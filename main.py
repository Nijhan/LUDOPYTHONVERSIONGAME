from game_logic import Player
from game_manager import GameManager
from sqlite_db import SQLiteDB

def main():
    # Two players
    players = [Player("Najma"), Player("Adrian")]

    # Initialize game with SQLite database
    db = SQLiteDB()
    game = GameManager(db)
    game.setup_game(players)

    print("🎲 Ludo Demo 🎲 Track ends at 57 for standard play. Each player has 4 tokens.")
    
    # Game loop
    while game.play_turn():
        game.display_board()
        input("\nPress ENTER to continue to next turn...")

if __name__ == "__main__":
    main()
