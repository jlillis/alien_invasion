import pygame
from settings import Settings

class Ship:
    """A class to manage the player ship."""

    def __init__(self, game):
        """Initialize the ship and set its starting position."""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Set its starting position (bottom center of screen)
        self.rect.midbottom = self.screen_rect.midbottom

        # Init position variables
        self.x = float(self.rect.x)

        # Init movment flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center ship on-screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)