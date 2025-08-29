from database import RealDB

class PostgresDB(RealDB):
    def __init__(self, dbname=None, user=None, password=None, host=None, port=5432):
        # Use default Supabase credentials if none provided
        if dbname is None:
            dbname = "postgres"
        if user is None:
            user = "postgres.uoouexfczqhdqjrvtsjn"
        if password is None:
            password = "zSDUjdsAZT4xmwEh"
        if host is None:
            host = "aws-1-eu-north-1.pooler.supabase.com"
        
        super().__init__(dbname, user, password, host, port)

    def create_game(self, player_count):
        """Create a new game and return the game ID"""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO games (status) VALUES ('in_progress') RETURNING id",
        )
        game_id = cur.fetchone()[0]
        self.conn.commit()
        return game_id

    def create_game_player(self, game_id, player_id, color):
        """Create a game_player entry and return the game_player_id"""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO game_players (game_id, player_id, color, is_winner) VALUES (%s, %s, %s, %s) RETURNING id",
            (game_id, player_id, color, False)
        )
        game_player_id = cur.fetchone()[0]
        self.conn.commit()
        return game_player_id

    def create_tokens(self, game_player_id, count=2):
        """Create tokens for a game player and return their IDs"""
        cur = self.conn.cursor()
        token_ids = []
        for _ in range(count):
            cur.execute(
                "INSERT INTO tokens (game_player_id, position, is_home, is_finished) VALUES (%s, %s, %s, %s) RETURNING id",
                (game_player_id, 0, True, False)
            )
            token_ids.append(cur.fetchone()[0])
        self.conn.commit()
        return token_ids

    def record_move(self, game_id, player_id, dice_value, token_id, new_position):
        """Record a move in the database"""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO moves (game_id, player_id, token_id, dice_value, new_position) VALUES (%s, %s, %s, %s, %s)",
            (game_id, player_id, token_id, dice_value, new_position)
        )
        self.conn.commit()

    def update_token_position(self, token_id, position):
        """Update a token's position"""
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE tokens SET position = %s, is_home = %s, is_finished = %s WHERE id = %s",
            (position, position == 0, position >= 20, token_id)
        )
        self.conn.commit()

    def finish_game(self, game_id, winner_id, all_player_ids):
        """Mark game as finished and update winner status"""
        cur = self.conn.cursor()
        
        # Update game status
        cur.execute(
            "UPDATE games SET status = 'finished' WHERE id = %s",
            (game_id,)
        )
        
        # Mark winner
        cur.execute(
            "UPDATE game_players SET is_winner = TRUE WHERE game_id = %s AND player_id = %s",
            (game_id, winner_id)
        )
        
        self.conn.commit()
