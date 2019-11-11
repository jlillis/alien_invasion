class Statistics:
    """Track game statistics."""

    def __init__(self, game):
        """Initialize statistics."""
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Reset statistics to default values."""
        self.ships_remaining = self.settings.ship_limit
        self.score = 0