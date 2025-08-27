from sqlalchemy.orm import sessionmaker
from alembic.app.db import engine, SessionLocal
from alembic.app.models import Player, Game, GamePlayer

class LudoDatabase:
    def __init__(self):
        self.session = SessionLocal()
    
    def create_player(self, name):
        player = Player(name=name)
        self.session.add(player)
        self.session.commit()
        return player
    
    def get_player(self, name):
        return self.session.query(Player).filter(Player.name == name).first()
    
    def create_game(self, player_names):
        game = Game()
        self.session.add(game)
        self.session.flush()
        
        colors = ["red", "blue", "green", "yellow"]
        for i, name in enumerate(player_names):
            player = self.get_player(name) or self.create_player(name)
            game_player = GamePlayer(
                game_id=game.id,
                player_id=player.id,
                color=colors[i],
                player_order=i
            )
            self.session.add(game_player)
        
        self.session.commit()
        return game
    
    def save_game_state(self, game_id, current_turn, token_positions):
        game = self.session.query(Game).get(game_id)
        game.current_player_turn = current_turn
        
        for player_order, positions in token_positions.items():
            game_player = self.session.query(GamePlayer).filter(
                GamePlayer.game_id == game_id,
                GamePlayer.player_order == player_order
            ).first()
            game_player.token_positions = positions
        
        self.session.commit()
    
    def finish_game(self, game_id, winner_player_order):
        game = self.session.query(Game).get(game_id)
        game.status = "finished"
        
        winner_game_player = self.session.query(GamePlayer).filter(
            GamePlayer.game_id == game_id,
            GamePlayer.player_order == winner_player_order
        ).first()
        
        game.winner_id = winner_game_player.player_id
        winner_game_player.is_finished = True
        
        # Update player stats
        winner = self.session.query(Player).get(winner_game_player.player_id)
        winner.games_won += 1
        
        # Update games_played for all players
        for gp in game.game_players:
            player = self.session.query(Player).get(gp.player_id)
            player.games_played += 1
        
        self.session.commit()
    
    def close(self):
        self.session.close()