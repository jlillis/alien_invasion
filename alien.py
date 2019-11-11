import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, game):
        """Initialize the alien."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load the alien image and get its rect
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Set its starting position (top left of screen)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Update the alien's position."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return True if the alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
