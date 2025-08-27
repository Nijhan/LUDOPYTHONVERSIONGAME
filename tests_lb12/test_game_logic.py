import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from game_logic import roll_dice, move_token, switch_turn, check_winner

