import sqlite3

def connect_db(db_name="game_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_stats (
            name TEXT PRIMARY KEY,
            token_position INTEGER,
            tokens_finished INTEGER
        )
    """)
    conn.commit()
    return conn

def save_player_stats(conn, player):
    if isinstance(player, tuple):
        name, token_position, tokens_finished = player
    else:
        name = getattr(player, "name", None)
        token_position = getattr(player, "token_position", None)
        tokens_finished = getattr(player, "tokens_finished", None)

    if name is None or token_position is None or tokens_finished is None:
        raise ValueError("Missing player attributes")

    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO player_stats (name, token_position, tokens_finished)
        VALUES (?, ?, ?)
    """, (name, token_position, tokens_finished))
    conn.commit()

def load_player_stats(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT name, token_position, tokens_finished FROM player_stats WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        return {
            "name": row[0],
            "token_position": row[1],
            "tokens_finished": row[2]
        }
    return None