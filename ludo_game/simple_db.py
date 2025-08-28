class SimpleDB:
    """Simple in-memory database for testing"""
    def __init__(self):
        self.players = {}
        self.next_id = 1
    
    def get_or_create_player(self, username):
        """Get or create a player by username"""
        if username in self.players:
            return self.players[username]
        
        player_data = {
            "username": username,
            "id": self.next_id,
            "wins": 0,
            "losses": 0
        }
        self.players[username] = player_data
        self.next_id += 1
        return player_data