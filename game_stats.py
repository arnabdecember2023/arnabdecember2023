import os
import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statisctics."""
        self.settings = ai_game.settings
        # High score should never reset.
        self.high_score = 0
        self.reset_stats()
        
        # Start Alien Invasion in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score() -> int:
        filename= 'high_score.json'
        if filename in os.lsitdir():
            with open(filename, 'r') as f:
                json.dump(high_score, f)
                val = f.read()
                if val == '':
                    high_score = 0
                else:
                    high_score = int(val)
        else:
            high_score = 0
        return high_score
    
    def set_score(high_score) -> None:
        with open('high_score.json', 'w') as file:
            file.write(str(high_score))