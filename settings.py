class Settings:
    """A class to store all settings."""

    def __init__(self):
        """Initialize game settings."""
        # Screen settings
        self.fullscreen = True
        self.screen_width = 1200 # Only used when fullscreen == False
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # Ship settings
        self.ship_speed = 1.25

        # Bullet settings
        self.bullets_allowed = 3
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)