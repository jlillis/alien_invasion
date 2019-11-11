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
        """ Update the ship's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def draw(self, screen):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        #self.bullets.draw(screen)
        for bullet in self.bullets:
            bullet.draw()

    def center_ship(self):
        """Center ship on-screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self.game))

    def update_bullets(self, game):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for bullet collisions
        self._check_bullet_collisions(game)

    def _check_bullet_collisions(self, game):
        """Check for bullet collisions."""
        # Check for bullets that have collided with aliens
        collisions = pygame.sprite.groupcollide(
            self.bullets, game.fleet.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                game.stats.score += self.settings.alien_points * len(aliens)
            game.scoreboard.prep_score()
            game.scoreboard.check_high_score()
        
        # Create a new fleet if all aliens are gone
        if not game.fleet.aliens:
            self.bullets.empty()
            game.fleet = Fleet(self)
            # Increment speed (difficulty)
            game.settings.increase_speed()
            # Increment level
            game.stats.level += 1
            game.scoreboard.prep_level()