import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()

def show_welcome():
    """Display welcome message"""
    console.print(Panel.fit(
        "[bold yellow]🎲 Welcome to Ludo Game![/bold yellow]",
        subtitle="[italic]A classic board game brought to life[/italic]",
        border_style="green"
    ))

def show_players(players):
    """Display registered players"""
    table = Table(title="Registered Players")
    table.add_column("Username", style="cyan")
    table.add_column("Color", style="magenta")
    table.add_column("Wins", style="green")
    table.add_column("Losses", style="red")
    
    for player in players:
        table.add_row(
            player.username,
            player.color,
            str(player.wins),
            str(player.losses)
        )
    
    console.print(table)

def announce_turn(player):
    """Announce whose turn it is"""
    console.print(f"\n[bold]{player.username}'s turn![/bold] [italic]({player.color})[/italic]")

def roll_dice_animation(player):
    """Show dice roll animation and return result"""
    console.print(f"[cyan]{player.username} is rolling the dice...[/cyan]")
    
    # Simple animation
    for i in range(3):
        console.print(f"[yellow]🎲 Rolling... {random.randint(1, 6)}[/yellow]", end="\r")
        time.sleep(0.3)
    
    roll = random.randint(1, 6)
    console.print(f"[bold green]🎲 {player.username} rolled a {roll}![/bold green]")
    return roll

def show_tokens(player, tokens):
    """Display player's tokens"""
    console.print(f"[bold]{player.username}'s tokens:[/bold]")
    for i, token in enumerate(tokens, 1):
        console.print(f"  Token {i}: Position {token['pos']}")

def show_live_board(players, track_length=20):
    """Display a simple ASCII board showing token positions"""
    console.print("\n[bold]Live Board:[/bold]")
    console.print("─" * 50)
    
    for player in players:
        positions = [f"{token['pos']}/{track_length}" for token in player.tokens]
        console.print(f"{player.username} ({player.color}): {' | '.join(positions)}")
    
    console.print("─" * 50)

def console_print(*args, **kwargs):
    """Wrapper for console.print"""
    console.print(*args, **kwargs)
