import sqlite3

class SQLiteDB:
    def __init__(self, db_name="game_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_stats (
                name TEXT PRIMARY KEY,
                token_position INTEGER,
                tokens_finished INTEGER,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def get_or_create_player(self, name):
        player = self.load_player_stats(name)
        if player:
            return player
        # Create new player
        player = {
            "name": name,
            "token_position": 0,
            "tokens_finished": 0,
            "wins": 0,
            "losses": 0,
        }
        self.save_player_stats(player)
        return player

    def save_player_stats(self, player):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO player_stats (name, token_position, tokens_finished, wins, losses)
            VALUES (?, ?, ?, ?, ?)
        """, (
            player.get("name"),
            player.get("token_position", 0),
            player.get("tokens_finished", 0),
            player.get("wins", 0),
            player.get("losses", 0),
        ))
        self.conn.commit()

    def load_player_stats(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, token_position, tokens_finished, wins, losses FROM player_stats WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return {
                "name": row[0],
                "token_position": row[1],
                "tokens_finished": row[2],
                "wins": row[3],
                "losses": row[4],
            }
        return None
