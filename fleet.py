import pygame
from alien import Alien

class Fleet():
    """A class to manage alien fleets."""

    def __init__(self, game):
        self.game = game
        self.aliens = pygame.sprite.Group()

        # Create a single alien and use it's width calculate the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(game)
        alien_width, alien_height = alien.rect.size
        space_x = game.settings.screen_width - (2 * alien_width)
        num_aliens_x = space_x // (2 * alien_width)

        # Calculate number of rows that fit on screen
        ship_height = game.player_ship.rect.height
        space_y = game.settings.screen_height - (3 * alien_height) - ship_height
        num_rows = space_y // (2 * alien_height)

        # Create the aliens
        for row_id in range(num_rows):
            for alien_id in range(num_aliens_x):
                self._create_alien(alien_id, row_id)

    def update(self):
        """Update the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Check for alien-ship collisions
        if pygame.sprite.spritecollideany(self.game.player_ship, self.aliens):
            self.game.kill_player()

        # Check for aliens hitting bottom of screen.
        self._check_aliens_bottom()
    
    def draw(self):
        """Draws the fleet."""
        # Draw all aliens in the fleet
        self.aliens.draw(self.game.screen)

    def _create_alien(self, alien_id, row_id):
        """Create an alien and place it in the row."""
        alien = Alien(self.game)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_id
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_id
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Check if the fleet has reached the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the fleet one row and change direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.game.settings.fleet_drop_speed
        
        self.game.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.game.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.game.kill_player()
                break