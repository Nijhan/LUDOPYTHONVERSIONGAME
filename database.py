import psycopg2


def connect_db(dbname, user, password, host="localhost", port=5432):
    """Helper function to connect to PostgreSQL and ensure tables exist."""
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
    )
    create_tables(conn)
    return conn


def create_tables(conn):
    with conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE,
                token_position INTEGER DEFAULT 0,
                tokens_finished INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
            """
        )
        conn.commit()


def save_player_stats(conn, player):
    with conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO players (name, token_position, tokens_finished, wins, losses)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
                token_position = EXCLUDED.token_position,
                tokens_finished = EXCLUDED.tokens_finished,
                wins = EXCLUDED.wins,
                losses = EXCLUDED.losses
            """,
            (
                getattr(player, "name", None),
                getattr(player, "token_position", 0),
                getattr(player, "tokens_finished", 0),
                getattr(player, "wins", 0),
                getattr(player, "losses", 0),
            ),
        )
        conn.commit()


def load_player_stats(conn, name):
    cur = conn.cursor()
    cur.execute(
        "SELECT name, token_position, tokens_finished, wins, losses FROM players WHERE name = %s",
        (name,),
    )
    row = cur.fetchone()
    if row:
        return type("Player", (), {
            "name": row[0],
            "token_position": row[1],
            "tokens_finished": row[2],
            "wins": row[3],
            "losses": row[4],
        })()
    return None


class RealDB:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        """Connect directly to PostgreSQL with given credentials."""
        self.conn = connect_db(dbname, user, password, host, port)

    def get_or_create_player(self, name):
        player = load_player_stats(self.conn, name)
        if player:
            return player
        # If not found, create new
        player = type("Player", (), {
            "name": name,
            "token_position": 0,
            "tokens_finished": 0,
            "wins": 0,
            "losses": 0,
        })()
        save_player_stats(self.conn, player)
        return player

    def update_player_stats(self, player):
        save_player_stats(self.conn, player)