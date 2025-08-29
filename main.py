import os
from urllib.parse import urlparse
from players import *
from sqlite_db import SQLiteDB  # SQLite DB alternative
from database import RealDB  # PostgreSQL DB alternative

def main():
    print("🎲 Welcome to Ludo!")

    # Get database URL from environment or use default
    database_url = os.getenv("DATABASE_URL", "")
    
    if not database_url:
        # Default to SQLite for easier local development
        print("⚠️  DATABASE_URL not set. Using SQLite database for local development.")
        db = SQLiteDB("ludo_game.db")
    elif database_url.startswith("sqlite"):
        # Use SQLiteDB
        db = SQLiteDB(database_url.split("///")[-1])
    else:
        # Parse the database URL
        parsed_url = urlparse(database_url)
        
        # Extract connection parameters
        dbname = parsed_url.path[1:]  # Remove leading slash
        user = parsed_url.username
        password = parsed_url.password
        host = parsed_url.hostname
        port = parsed_url.port or 5432

        db = RealDB(dbname, user, password, host, port)  # real database

    # Register players
    players_list = register_players(db)

    # Choose colors
    choose_colors(players_list)

    print("\n✅ Players are ready to start!")
    for p in players_list:
        print(f"- {p.username} (Color: {p.color}) | Wins: {p.wins}, Losses: {p.losses}")

if __name__ == "__main__":
    main()