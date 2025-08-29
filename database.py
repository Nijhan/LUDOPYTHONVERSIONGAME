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
    # Tables are already created by Alembic migrations
    # This function is kept for backward compatibility but does nothing
    # since tables are managed by Alembic
    pass


def save_player_stats(conn, player):
    # This function is not used in the new schema
    # Player stats are managed through the game_players and moves tables
    pass


def load_player_stats(conn, username):
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, email, created_at FROM players WHERE username = %s",
        (username,),
    )
    row = cur.fetchone()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "created_at": row[3]
        }
    return None


class RealDB:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        """Connect directly to PostgreSQL with given credentials."""
        self.conn = connect_db(dbname, user, password, host, port)

    def get_or_create_player(self, username):
        player = load_player_stats(self.conn, username)
        if player:
            return player
        # If not found, create new player
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO players (username, email) VALUES (%s, %s) RETURNING id, username, email, created_at",
            (username, f"{username}@example.com")
        )
        row = cur.fetchone()
        self.conn.commit()
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "created_at": row[3]
        }

    def update_player_stats(self, player):
        # Player stats are updated through game-specific tables
        # This method is kept for compatibility but does nothing
        pass
