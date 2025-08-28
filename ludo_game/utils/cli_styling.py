# utils/cli_styling.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
import random
import time

console = Console()

# -----------------------------
# Welcome & Players
# -----------------------------
def show_welcome():
    console.print(
        Panel.fit(
            "🎲 [bold magenta]Welcome to Ludo![/bold magenta] 🎲\nLet's register players...",
            border_style="green",
            title="[yellow]LUDO GAME[/yellow]"
        )
    )

def show_players(players_list):
    table = Table(title="✅ Players Ready")
    table.add_column("Username", style="cyan", justify="center")
    table.add_column("Color", style="bold", justify="center")
    table.add_column("Wins", justify="center")
    table.add_column("Losses", justify="center")

    color_map = {"RED": "red", "GREEN": "green", "BLUE": "blue", "YELLOW": "yellow"}

    for p in players_list:
        table.add_row(
            p.username,
            f"[{color_map.get(p.color, 'white')}]{p.color}[/{color_map.get(p.color, 'white')}]",
            str(p.wins),
            str(p.losses)
        )

    console.print(table)

# -----------------------------
# Dice & Turns
# -----------------------------
def announce_turn(player):
    console.print(f"\n[bold cyan]{player.username}[/bold cyan]'s turn → press ENTER to roll dice 🎲")

def roll_dice_animation(player, sides=6, rolls=10, delay=0.1):
    with Live("", refresh_per_second=10, console=console) as live:
        for _ in range(rolls):
            fake_roll = random.randint(1, sides)
            text = Text.assemble(
                ("🎲 ", "yellow"),
                (f"{player.username} rolled: ", "cyan"),
                (f"{fake_roll}", "bold green")
            )
            live.update(text)
            time.sleep(delay)
        final_roll = random.randint(1, sides)
        text = Text.assemble(
            ("🎲 ", "yellow"),
            (f"{player.username} rolled: ", "cyan"),
            (f"{final_roll}", "bold green")
        )
        live.update(text)
        time.sleep(0.2)
    return final_roll

# -----------------------------
# Token & Board
# -----------------------------
def show_tokens(player, tokens):
    color_map = {"RED": "red", "GREEN": "green", "BLUE": "blue", "YELLOW": "yellow"}
    tokens_status = ", ".join(
        f"[{color_map.get(t['color'], 'white')}]{t['pos']}[/{color_map.get(t['color'], 'white')}]"
        for t in tokens
    )
    console.print(f"{player.username}: {tokens_status}")

def render_full_board(players_list, track_length=20):
    color_map = {"RED": "red", "GREEN": "green", "BLUE": "blue", "YELLOW": "yellow"}
    yard_lines = []
    for p in players_list:
        yard_tokens = " ".join(f"[{color_map.get(t['color'], 'white')}]{p.username[0]}[/{color_map.get(t['color'], 'white')}]"
                               for t in p.tokens if t["pos"] == "Yard")
        yard_lines.append(f"{p.username} Yard: {yard_tokens or 'Empty'}")

    track_str = ""
    for pos in range(1, track_length + 1):
        cell_tokens = []
        for p in players_list:
            for t in p.tokens:
                if t["pos"] == pos:
                    cell_tokens.append(f"[{color_map.get(t['color'], 'white')}]{p.username[0]}[/{color_map.get(t['color'], 'white')}]")
        track_str += "".join(cell_tokens).ljust(4) if cell_tokens else f"{pos}".ljust(4)

    board_str = "\n".join(yard_lines) + "\n\nTrack:\n" + track_str
    return board_str

def show_live_board(players_list, track_length=20, delay=0.5):
    with Live(render_full_board(players_list, track_length), refresh_per_second=4, console=console) as live:
        time.sleep(delay)
        live.update(render_full_board(players_list, track_length))