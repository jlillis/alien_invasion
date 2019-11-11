import json

class Statistics:
    """Track game statistics."""

    def __init__(self, game):
        """Initialize statistics."""
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False
        # Read high score
        try:
            with open("scores.json") as file:
                self.high_score = int(json.load(file))
        except:
            print("Failed to read high score from scores.json!")
            self.high_score = 0
    
        self.level = 1

    def reset_stats(self):
        """Reset statistics to default values."""
        self.ships_remaining = self.settings.ship_limit
        self.score = 0