import random
from typing import List, Dict, Optional
from players import Player
from database import RealDB
from sqlite_db import SQLiteDB

class GameManager:
    def __init__(self, db):
        self.db = db
        self.players: List[Player] = []
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
        # Each player has 4 tokens, positions start at 0 (home)
        self.token_positions: Dict[str, List[int]] = {}
        
    def setup_game(self, players: List[Player]):
        """Initialize game state with players and their tokens"""
        self.players = players
        for player in players:
            self.token_positions[player.username] = [0, 0, 0, 0]  # 4 tokens per player
            
    def roll_dice(self) -> int:
        """Roll a 6-sided dice"""
        return random.randint(1, 6)
    
    def get_available_tokens(self, player: Player) -> List[int]:
        """Get indices of tokens that can be moved (not finished)"""
        positions = self.token_positions[player.username]
        return [i for i, pos in enumerate(positions) if pos < 57]  # 57 is final position
    
    def move_token(self, player: Player, token_index: int, steps: int) -> bool:
        """Move a token and return True if it reaches exactly the finish"""
        current_pos = self.token_positions[player.username][token_index]
        new_pos = current_pos + steps
        
        # Handle exact finish requirement - can only move if it lands exactly on 57 or less
        if new_pos > 57:
            return False  # Cannot move beyond finish
            
        self.token_positions[player.username][token_index] = new_pos
        
        # Check if token reached finish exactly
        if new_pos == 57:
            return True
        return False
    
    def check_winner(self, player: Player) -> bool:
        """Check if a player has won (all 4 tokens at finish)"""
        positions = self.token_positions[player.username]
        return all(pos == 57 for pos in positions)
    
    def next_turn(self, got_six: bool = False) -> Player:
        """Move to next player, unless current player rolled a 6"""
        if not got_six:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]
    
    def play_turn(self) -> bool:
        """Play one turn for the current player, return True if game continues"""
        if self.game_over:
            return False
            
        current_player = self.players[self.current_player_index]
        print(f"\n🎲 {current_player.username}'s turn!")
        
        # Roll dice
        dice_roll = self.roll_dice()
        print(f"🎯 Rolled: {dice_roll}")
        
        # Check if player can enter tokens
        available_tokens = self.get_available_tokens(current_player)
        
        if dice_roll == 6 and any(pos == 0 for pos in self.token_positions[current_player.username]):
            # Player rolled 6 and has tokens at home - must enter one
            print("🎉 You rolled a 6! You can enter a token to the board.")
            token_to_move = 0  # Enter first available token
            for i, pos in enumerate(self.token_positions[current_player.username]):
                if pos == 0:
                    token_to_move = i
                    break
            self.token_positions[current_player.username][token_to_move] = 1  # Start at position 1
            print(f"✅ Token {token_to_move + 1} entered the board!")
            self.next_turn(got_six=True)  # Extra turn for rolling 6
            return True
            
        elif available_tokens:
            # Player has tokens on board that can move
            print(f"Available tokens to move: {[i+1 for i in available_tokens]}")
            
            # For simplicity, move the first available token
            token_to_move = available_tokens[0]
            moved = self.move_token(current_player, token_to_move, dice_roll)
            
            if moved:
                print(f"✅ Moved token {token_to_move + 1} to position {self.token_positions[current_player.username][token_to_move]}")
                
                # Check if this move won the game
                if self.check_winner(current_player):
                    self.game_over = True
                    self.winner = current_player
                    print(f"🏆 {current_player.username} WINS THE GAME! 🏆")
                    return False
            else:
                print(f"❌ Cannot move token {token_to_move + 1} - would exceed finish")
                
            # Check if rolled 6 for extra turn
            if dice_roll == 6:
                print("🎉 Rolled a 6! You get an extra turn!")
                self.next_turn(got_six=True)
            else:
                self.next_turn()
                
            return True
        else:
            # No available moves
            print("❌ No tokens can be moved")
            self.next_turn()
            return True
    
    def display_board(self):
        """Display current board state"""
        print("\n📊 Current Board:")
        for player in self.players:
            positions = self.token_positions[player.username]
            token_str = ", ".join([f"T{i+1}:{pos}" for i, pos in enumerate(positions)])
            print(f"  {player.username} ({player.color}): {token_str}")
