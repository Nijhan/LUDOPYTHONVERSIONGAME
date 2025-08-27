import builtins
import pytest

from ludo_game import main
 # your main.py

def run_with_inputs(inputs, func, *args):
    """
    Helper to replace input() with predefined answers.
    """
    iterator = iter(inputs)

    def fake_input(_prompt=""):
        return next(iterator)

    real_input = builtins.input
    builtins.input = fake_input
    try:
        return func(*args)
    finally:
        builtins.input = real_input

#capsys is a built-in fixture that lets you capture anything printed to stdout (print) or stderr (errors) while a test is running.
def test_main_flow(capsys):
    """
    Simulate a full game setup with 2 players.
    """
    inputs = [
        "2",       # number of players
        "eva",     # player1 username
        "maina",   # player2 username
        "red",     # eva's color
        "green",   # maina's color
    ]

    run_with_inputs(inputs, main.main)

    # Capture stdout
    captured = capsys.readouterr()
    output = captured.out

    # Assertions
    assert "Welcome to Ludo" in output
    assert "eva" in output
    assert "maina" in output
    assert "RED" in output
    assert "GREEN" in output
    assert "✅ Players are ready to start!" in output
