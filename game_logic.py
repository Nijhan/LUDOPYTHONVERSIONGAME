import random

class Player:
    def _init_(self, name):
        self.name = name
        self.position = 0

    def move(self, steps):
        self.position += steps

class GameLogic:
    @staticmethod
    def roll_dice():
        return random.randint(1, 6)

    @staticmethod
    def move_token(start, steps):
        return start + steps

    @staticmethod
    def switch_turn(current_index, players):
        return (current_index + 1) % len(players)

    @staticmethod
    def check_winner(position, end_position=57):
        return position >= end_position

# Free functions for easier test access
def roll_dice():
    return GameLogic.roll_dice()

def move_token(start, steps):
    return GameLogic.move_token(start, steps)

def switch_turn(current_index, players):
    return GameLogic.switch_turn(current_index, players)

def check_winner(position, end_position=57):
    return GameLogic.check_winner(position, end_position)