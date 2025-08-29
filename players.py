from utils.input_utils import (
    prompt_int,
    prompt_username,
    prompt_choice,
)

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

        # DB lookup (create if not exists)
        row = db.get_or_create_player(username)

        # Handle different return types from database classes
        if hasattr(row, 'name'):  # RealDB returns Player object
            player = Player(
                username=row.name,
                player_id=getattr(row, 'id', None),
                wins=getattr(row, 'wins', 0),
                losses=getattr(row, 'losses', 0),
            )
        else:  # SQLiteDB returns dictionary
            player = Player(
                username=row["name"],
                player_id=row.get("id", None),
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