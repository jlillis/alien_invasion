import sys
import pygame
from time import sleep
from settings import Settings
from statistics import Statistics
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        
        # Initialize stats
        self.stats = Statistics(self)

        # Initialize game elements
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        self.scoreboard = Scoreboard(self)

        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _update_screen(self):
        """Redraw the game elements and screen."""

        # Redraw the background
        self.screen.fill(self.settings.bg_color)

        # Redraw the ship
        self.ship.blitme()

        # Redraw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Redraw aliens
        self.aliens.draw(self.screen)

        # Redraw scoreboard
        self.scoreboard.show_score()

        # Redraw play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()
          
    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():
            # Exit when the game window is closed
            if event.type == pygame.QUIT:
                sys.exit()
            # Respond to mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            # Respond to key events
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
    
    def _check_keydown_event(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_event(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game
            self.stats.reset_stats()
            self.settings.initialize_dynamic_settings()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()

            # Hide cursor
            pygame.mouse.set_visible(False)

            # Start game
            self.stats.game_active = True

            self.scoreboard.prep_score()
            self.scoreboard.prep_level()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

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
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        
        # Create a new fleet if all aliens are gone
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            # Increment speed (difficulty)
            self.settings.increase_speed()
            # Increment level
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Create an alien and find number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        space_x = self.settings.screen_width - (2 * alien_width)
        num_aliens_x = space_x // (2 * alien_width)

        # Determine number of rows that fit on screen
        ship_height = self.ship.rect.height
        space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        num_rows = space_y // (2 * alien_height)

        # Create the fleet of aliens
        for row_id in range(num_rows):
            for alien_id in range(num_aliens_x):
                self._create_alien(alien_id, row_id)
    
    def _create_alien(self, alien_id, row_id):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_id
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_id
        self.aliens.add(alien)

    def _update_aliens(self):
        """Update all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Check for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens hitting bottom of screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Check if the fleet has reached the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the fleet one row and change direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the player's ship being hit by an alien."""
        if self.stats.ships_remaining > 0:
            # Decrement number of ships remaining
            self.stats.ships_remaining -= 1

            # Clear all aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make a game instance and run it
    game = AlienInvasion()
    game.run_game()