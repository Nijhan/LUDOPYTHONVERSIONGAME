from database import LudoDatabase

class PlayerManager:
    def __init__(self):
        self.db = LudoDatabase()
    
    def register_player(self, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Player name must be at least 2 characters")
        
        existing = self.db.get_player(name.strip())
        if existing:
            return existing
        
        return self.db.create_player(name.strip())
    
    def get_player_stats(self, name):
        player = self.db.get_player(name)
        if not player:
            return None
        
        return {
            "name": player.name,
            "games_played": player.games_played,
            "games_won": player.games_won,
            "win_rate": player.games_won / player.games_played if player.games_played > 0 else 0
        }
    
    def validate_players(self, player_names):
        if len(player_names) < 2 or len(player_names) > 4:
            raise ValueError("Game requires 2-4 players")
        
        if len(set(player_names)) != len(player_names):
            raise ValueError("Player names must be unique")
        
        return True