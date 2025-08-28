import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

class PostgresDB:
    def __init__(self):
        self.connection = psycopg2.connect(
            host="aws-1-eu-north-1.pooler.supabase.com",
            database="postgres",
            user="postgres.uoouexfczqhdqjrvtsjn",
            password="zSDUjdsAZT4xmwEh",
            port=5432
        )
        self.connection.autocommit = True
        self.create_tables()
    
    def create_tables(self):
        """Create tables if they don't exist"""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(120),
                    wins INTEGER DEFAULT 0,
                    losses INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id SERIAL PRIMARY KEY,
                    winner_id INTEGER REFERENCES players(id),
                    player_count INTEGER,
                    status VARCHAR(20) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                    id SERIAL PRIMARY KEY,
                    game_id INTEGER REFERENCES games(id),
                    player_id INTEGER REFERENCES players(id),
                    token_number INTEGER,
                    position VARCHAR(10) DEFAULT 'Yard',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS moves (
                    id SERIAL PRIMARY KEY,
                    game_id INTEGER REFERENCES games(id),
                    player_id INTEGER REFERENCES players(id),
                    dice_roll INTEGER,
                    token_id INTEGER REFERENCES tokens(id),
                    from_position VARCHAR(10),
                    to_position VARCHAR(10),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def get_or_create_player(self, username):
        """Get or create player"""
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM players WHERE username = %s", (username,))
            player = cursor.fetchone()
            
            if player:
                return dict(player)
            
            cursor.execute(
                "INSERT INTO players (username, email) VALUES (%s, %s) RETURNING *",
                (username, f"{username}@example.com")
            )
            return dict(cursor.fetchone())
    
    def update_player_stats(self, player_id, won=False):
        """Update player win/loss stats"""
        with self.connection.cursor() as cursor:
            if won:
                cursor.execute("UPDATE players SET wins = wins + 1 WHERE id = %s", (player_id,))
            else:
                cursor.execute("UPDATE players SET losses = losses + 1 WHERE id = %s", (player_id,))
    
    def create_game(self, player_count):
        """Create new game and return game_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO games (status) VALUES ('active') RETURNING id"
            )
            return cursor.fetchone()[0]
    
    def create_tokens(self, game_player_id, num_tokens=4):
        """Create tokens for a player in a game"""
        token_ids = []
        with self.connection.cursor() as cursor:
            for i in range(num_tokens):
                cursor.execute(
                    "INSERT INTO tokens (game_player_id, position, is_home, is_finished) VALUES (%s, %s, %s, %s) RETURNING id",
                    (game_player_id, 0, True, False)
                )
                token_ids.append(cursor.fetchone()[0])
        return token_ids
    
    def record_move(self, game_id, player_id, dice_roll, token_id, new_position):
        """Record a move in the database"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO moves (game_id, player_id, token_id, dice_value, new_position) VALUES (%s, %s, %s, %s, %s)",
                (game_id, player_id, token_id, dice_roll, new_position)
            )
    
    def update_token_position(self, token_id, new_position):
        """Update token position in database"""
        with self.connection.cursor() as cursor:
            is_home = new_position == 0
            is_finished = new_position >= 20
            cursor.execute(
                "UPDATE tokens SET position = %s, is_home = %s, is_finished = %s WHERE id = %s",
                (new_position, is_home, is_finished, token_id)
            )
    
    def create_game_player(self, game_id, player_id, color):
        """Create game_player relationship"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO game_players (game_id, player_id, color) VALUES (%s, %s, %s) RETURNING id",
                (game_id, player_id, color)
            )
            return cursor.fetchone()[0]
    
    def finish_game(self, game_id, winner_id, all_player_ids):
        """Finish game and update all stats"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE games SET winner_id = %s, status = 'finished' WHERE id = %s",
                (winner_id, game_id)
            )
            
            # Update stats for all players
            for player_id in all_player_ids:
                self.update_player_stats(player_id, won=(player_id == winner_id))