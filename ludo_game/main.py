from ludo_game import players
from ludo_game.utils import input_utils

# Temporary FakeDB until LB-10 (database) is finished
class FakeDB:
    def __init__(self):
        self.data = {}
        self.next_id = 1

    def get_or_create_player(self, username):
        if username not in self.data:
            self.data[username] = {
                "id": self.next_id,
                "username": username,
                "wins": 0,
                "losses": 0,
            }
            self.next_id += 1
        return self.data[username]


def main():
    print("🎲 Welcome to Ludo!")
    print("Let's register players...\n")

    # Use FakeDB for now
    db = FakeDB()

    # Step 1: Register players
    players_list = players.register_players(db)

    # Step 2: Choose colors
    players.choose_colors(players_list)

    # Step 3: Confirm setup
    print("\n✅ Players are ready to start!")
    for p in players_list:
        print(f"- {p.username} (Color: {p.color}) | Wins: {p.wins}, Losses: {p.losses}")


if __name__ == "__main__":
    main()
