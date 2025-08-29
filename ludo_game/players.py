from ludo_game.utils.input_utils import (
    prompt_int,
    prompt_username,
    prompt_choice,
    prompt_yes_no,
)
from psycopg2.extras import RealDictCursor

# Available Ludo colors
PLAYER_COLORS = ["RED", "GREEN", "YELLOW", "BLUE"]

class Player:
    def __init__(self, username, color="", player_id=None, wins=0, losses=0):
        self.username = username
        self.color = color
        self.id = player_id
        self.wins = wins
        self.losses = losses

    def __str__(self):
        return f"Player({self.username}, {self.color}, Wins: {self.wins}, Losses: {self.losses})"


def register_players(db, min_players=2, max_players=4):
    """Register players via CLI and ensure unique usernames."""
    num_players = prompt_int("How many players?", min_players, max_players)
    players = []
    used_names = set()

    for i in range(1, num_players + 1):
        username = prompt_username(f"Enter username for Player {i}", used_names)
        used_names.add(username)

        # Check if player already exists
        with db.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM players WHERE username = %s", (username,))
            existing_player = cursor.fetchone()
            
            if existing_player:
                print(f"👋 Welcome back, {username}! You already have an account.")
                
                # Check if player has an active game to resume
                game_data = db.get_player_active_game_tokens(existing_player['id'])
                if game_data:
                    resume_game = prompt_yes_no("You have an active game. Would you like to resume it?")
                    if resume_game:
                        player = Player(
                            username=existing_player["username"],
                            player_id=existing_player["id"],
                            wins=existing_player.get("wins", 0),
                            losses=existing_player.get("losses", 0),
                        )
                        # Store game data for later use in main game loop
                        player.active_game_data = game_data
                        players.append(player)
                        continue
                    else:
                        print("Starting a new game...")
                
                # Use existing player without resuming game
                player = Player(
                    username=existing_player["username"],
                    player_id=existing_player["id"],
                    wins=existing_player.get("wins", 0),
                    losses=existing_player.get("losses", 0),
                )
                players.append(player)
            else:
                # Create new player
                row = db.get_or_create_player(username)
                player = Player(
                    username=row["username"],
                    player_id=row["id"],
                    wins=row.get("wins", 0),
                    losses=row.get("losses", 0),
                )
                players.append(player)

    return players


def choose_colors(players):
    """Assign colors to players, ensuring uniqueness."""
    available = PLAYER_COLORS[: len(players)]
    for player in players:
        choice = prompt_choice(f"{player.username}, choose your color", available)
        player.color = choice
        available.remove(choice)
