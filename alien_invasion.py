import sys
import pygame
from time import sleep
from settings import Settings
from statistics import Statistics
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from fleet import Fleet
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
        self.fleet = Fleet(self)
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
                self.fleet.update()
            
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

        # Redraw fleet
        self.fleet.draw()

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
                self.scoreboard.save_high_score()
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
            self.scoreboard.save_high_score()
            sys.exit()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_event(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _start_game(self):
        """Start a new game."""
        # Reset game
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.bullets.empty()
        self.fleet = Fleet(self)
        self.ship.center_ship()

        # Hide cursor
        pygame.mouse.set_visible(False)

        # Start game
        self.stats.game_active = True

        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

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
            self.bullets, self.fleet.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        
        # Create a new fleet if all aliens are gone
        if not self.fleet.aliens:
            self.bullets.empty()
            self.fleet = Fleet(self)
            # Increment speed (difficulty)
            self.settings.increase_speed()
            # Increment level
            self.stats.level += 1
            self.scoreboard.prep_level()

    def ship_hit(self):
        """Respond to the player's ship being hit by an alien."""
        if self.stats.ships_remaining > 0:
            # Decrement number of ships remaining
            self.stats.ships_remaining -= 1
            self.scoreboard.prep_ships()

            # Clear all aliens and bullets
            #self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and ship
            self.fleet = Fleet(self)
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

if __name__ == '__main__':
    # Make a game instance and run it
    game = AlienInvasion()
    game.run_game()