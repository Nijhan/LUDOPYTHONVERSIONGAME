from ludo_game import players
from database import DB  # real DB

def main():
    print("🎲 Welcome to Ludo!")

    db = DB()  # real database

    # Register players
    players_list = players.register_players(db)

    # Choose colors
    players.choose_colors(players_list)

    print("\n✅ Players are ready to start!")
    for p in players_list:
        print(f"- {p.username} (Color: {p.color}) | Wins: {p.wins}, Losses: {p.losses}")

if __name__ == "__main__":
    main()