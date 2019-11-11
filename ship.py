import pygame
from pygame.sprite import Sprite
from settings import Settings
from bullet import Bullet
from fleet import Fleet

class Ship(Sprite):
    """A class to manage the player ship."""

    def __init__(self, game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.game = game
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

        # Init bullet group
        self.bullets = pygame.sprite.Group()

        # Init movment flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position and fired bullets."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x
        self._update_bullets()

    def draw(self, screen):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        #self.bullets.draw(screen)
        for bullet in self.bullets:
            bullet.draw()

    def reset(self):
        """Resets the ship to it's default state."""
        # Center the ship
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        # Clear all bullets
        self.bullets = pygame.sprite.Group()

    def fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self.game))

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for bullet collisions
        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        """Check for bullet collisions."""
        # Check for bullets that have collided with aliens
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.game.fleet.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.game.stats.score += self.settings.alien_points * len(aliens)
            self.game.scoreboard.prep_score()
            self.game.scoreboard.check_high_score()
        
        # Create a new fleet if all aliens are gone
        if not self.game.fleet.aliens:
            self.bullets.empty()
            self.game.fleet = Fleet(self)
            # Increment speed (difficulty)
            self.game.settings.increase_speed()
            # Increment level
            self.game.stats.level += 1
            self.game.scoreboard.prep_level()