class Settings:
    """A class to store all settings."""

    def __init__(self):
        """Initialize game settings."""
        # Screen settings
        self.fullscreen = True
        self.screen_width = 1200 # Only used when fullscreen == False
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Bullet settings
        self.bullets_allowed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # Alien settings
        self.fleet_drop_speed = 10
        self.ship_limit = 3

        # Difficulty scaling
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        # Scoreboard settings
        self.text_color = (0, 0, 0)

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1 # 1 = right, -1 = left
        self.alien_points = 50
        self.score_scale = 1.5

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
