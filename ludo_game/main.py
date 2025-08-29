# ludo_game/main.py

from utils import cli_styling as ui
from . import players
from .postgres_db import PostgresDB as RealDB

def main():
    ui.show_welcome()

    db = RealDB()
    players_list = players.register_players(db)
    players.choose_colors(players_list)
    ui.show_players(players_list)

    # Check if any player has an active game to resume
    resuming_game = False
    resuming_player = None
    resuming_game_id = None
    
    for p in players_list:
        if hasattr(p, 'active_game_data') and p.active_game_data:
            resuming_game = True
            resuming_player = p
            resuming_game_id = p.active_game_data['game_id']
            print(f"🎮 Resuming game {resuming_game_id} for {p.username}")
            break
    
    if resuming_game:
        # Use existing game and tokens
        game_id = resuming_game_id
        
        # Load tokens for all players from the existing game
        for p in players_list:
            if hasattr(p, 'active_game_data') and p.active_game_data:
                # This player has active game data, use their tokens
                game_data = p.active_game_data
                p.tokens = []
                for token in game_data['tokens']:
                    p.tokens.append({
                        "pos": int(token['position']),
                        "color": game_data['color'],
                        "id": token['id']
                    })
            else:
                # This player is joining an existing game, create new tokens for them
                game_player_id = db.create_game_player(game_id, p.id, p.color)
                token_ids = db.create_tokens(game_player_id, 2)
                p.tokens = [{"pos": 0, "color": p.color, "id": token_ids[i]} for i in range(2)]
    else:
        # Create new game
        game_id = db.create_game(len(players_list))
        
        # Create game_players and tokens for each player
        for p in players_list:
            game_player_id = db.create_game_player(game_id, p.id, p.color)
            token_ids = db.create_tokens(game_player_id, 2)
            p.tokens = [{"pos": 0, "color": p.color, "id": token_ids[i]} for i in range(2)]

    playing = True
    turn_index = 0
    track_length = 20

    while playing:
        current_player = players_list[turn_index]
        ui.announce_turn(current_player)
        input("Press ENTER to roll dice...")
        roll = ui.roll_dice_animation(current_player)

        moved = False
        for token in current_player.tokens:
            old_pos = token["pos"]
            if token["pos"] == 0 and roll == 6:
                token["pos"] = 1
                moved = True
            elif token["pos"] > 0:
                token["pos"] += roll
                if token["pos"] > track_length:
                    token["pos"] = track_length
                moved = True
            
            if moved:
                # Record move and update token in database
                db.record_move(game_id, current_player.id, roll, token["id"], token["pos"])
                db.update_token_position(token["id"], token["pos"])
                break

        ui.show_tokens(current_player, current_player.tokens)
        ui.show_live_board(players_list, track_length)

        for p in players_list:
            if all(isinstance(t["pos"], int) and t["pos"] >= track_length for t in p.tokens):
                ui.console.print(f"\n🏆 [bold green]{p.username} wins the game![/bold green]")
                
                # Finish game in database
                all_player_ids = [player.id for player in players_list]
                db.finish_game(game_id, p.id, all_player_ids)
                ui.console.print("[green]Game completed and saved to database![/green]")
                
                playing = False
                break

        turn_index = (turn_index + 1) % len(players_list)


if __name__ == "__main__":
    main()
