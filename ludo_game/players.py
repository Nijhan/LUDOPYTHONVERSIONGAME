# ludo_game/players.py
from utils.input_utils import get_valid_input
from utils.cli_styling import console
from .postgres_db import PostgresDB
import random

class Player:
    def __init__(self, username, player_id, color="", wins=0, losses=0):
        self.username = username
        self.id = player_id
        self.color = color
        self.wins = wins
        self.losses = losses
        self.tokens = []
        self.active_game_data = None

def register_players(db):
    """Register players for the game"""
    players_list = []
    
    console.print("\n[bold cyan]Player Registration[/bold cyan]")
    num_players = get_valid_input(
        "How many players? (2-4): ",
        lambda x: x.isdigit() and 2 <= int(x) <= 4,
        "Please enter a number between 2 and 4"
    )
    
    num_players = int(num_players)
    available_colors = ["RED", "GREEN", "BLUE", "YELLOW"]
    random.shuffle(available_colors)
    
    for i in range(num_players):
        while True:
            username = input(f"Enter username for Player {i+1}: ").strip()
            if not username:
                console.print("[red]Username cannot be empty![/red]")
                continue
                
            # Check if player exists in database
            player_data = db.get_or_create_player(username)
            
            # Check if player has active game
            active_game = db.get_player_active_game_tokens(player_data['id'])
            
            player = Player(
                username=player_data['username'],
                player_id=player_data['id'],
                wins=player_data.get('wins', 0),
                losses=player_data.get('losses', 0)
            )
            
            if active_game:
                console.print(f"[yellow]Found active game for {username}![/yellow]")
                resume = input("Resume this game? (y/n): ").lower().strip()
                if resume == 'y':
                    player.active_game_data = active_game
                    players_list.append(player)
                    console.print(f"[green]Resuming game for {username}[/green]")
                    break
                else:
                    console.print(f"[yellow]Starting new game for {username}[/yellow]")
                    players_list.append(player)
                    break
            else:
                players_list.append(player)
                break
    
    return players_list

def choose_colors(players_list):
    """Let players choose their colors"""
    available_colors = ["RED", "GREEN", "BLUE", "YELLOW"]
    color_map = {"RED": "red", "GREEN": "green", "BLUE": "blue", "YELLOW": "yellow"}
    
    console.print("\n[bold cyan]Choose Your Colors[/bold cyan]")
    console.print("Available colors: " + ", ".join(
        f"[{color_map[color]}]{color}[/{color_map[color]}]" for color in available_colors
    ))
    
    for player in players_list:
        if player.active_game_data:
            # Player is resuming a game, use their existing color
            player.color = player.active_game_data['color']
            console.print(f"{player.username} keeps their [{color_map[player.color]}]{player.color}[/{color_map[player.color]}] color")
            continue
            
        while True:
            color_choice = input(f"{player.username}, choose your color: ").upper().strip()
            if color_choice in available_colors:
                player.color = color_choice
                available_colors.remove(color_choice)
                console.print(f"{player.username} chose [{color_map[color_choice]}]{color_choice}[/{color_map[color_choice]}]")
                break
            else:
                console.print(f"[red]Invalid color! Choose from: {', '.join(available_colors)}[/red]")
