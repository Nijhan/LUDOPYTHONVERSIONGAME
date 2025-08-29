# TODO: Player Registration and Game Resumption Feature

## Steps to Complete:

1. [x] Add method to PostgresDB to fetch tokens and positions for a player in active game
2. [x] Modify register_players function to detect existing players and prompt for resume
3. [x] Update main game loop to support resuming from saved token positions
4. [ ] Test the registration flow for existing and new players
5. [ ] Test resuming game state from saved tokens

## Current Progress:
- Added get_player_active_game_tokens method to PostgresDB
- Modified register_players to detect existing players and prompt for resume
- Updated main game loop to support resuming from saved token positions
- Ready for testing
