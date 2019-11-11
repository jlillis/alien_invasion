import sys
import pygame
from time import sleep
from settings import Settings
from statistics import Statistics
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from fleet import Fleet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game."""
        # Initialize game display
        pygame.init()
        self.settings = Settings()
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Initialize stats
        self.stats = Statistics(self)
        self.active = False

        # Initialize game elements
        self.player_ship = Ship(self)
        self.fleet = Fleet(self)
        self.play_button = Button(self, "Play")
        self.scoreboard = Scoreboard(self)

    def run(self):
        """Start the main game loop."""
        while True:
            # Check for keyboard/mouse events
            self._check_events()

            # Update player ship and alien fleet, if game is active
            if self.active:
                self.player_ship.update()
                self.fleet.update()
            
            # Draw the game
            self._draw()

    def _draw(self):
        """Draw the game screen and all elements."""

        # Redraw the background
        self.screen.fill(self.settings.bg_color)

        # Redraw the player ship
        self.player_ship.draw(self.screen)

        # Redraw the alien fleet
        self.fleet.draw()

        # Redraw the scoreboard
        self.scoreboard.draw()

        # Redraw play button if game is inactive
        if not self.active:
            self.play_button.draw()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _start_game(self):
        """Start a new game."""
        # Reset game
        self.stats.reset()
        self.settings.initialize_dynamic_settings()
        self.fleet = Fleet(self)
        self.player_ship.reset()

        # Hide cursor
        pygame.mouse.set_visible(False)

        # Start game
        self.active = True

        # Prep the scoreboard
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()

    def kill_player(self):
        """Handle player death."""
        if self.stats.ships_remaining > 0:
            # Decrement number of ships remaining
            self.stats.ships_remaining -= 1
            self.scoreboard.prep_ships()

            # Create new fleet and ship
            self.fleet = Fleet(self)
            self.player_ship.reset()

            # Pause
            sleep(0.5)
        else:
            self.active = False
            pygame.mouse.set_visible(True)

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
            self.player_ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.player_ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.player_ship.fire_bullet()
        elif event.key == pygame.K_q:
            self.scoreboard.save_high_score()
            sys.exit()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_event(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.player_ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player_ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

if __name__ == '__main__':
    # Make a game instance and run it
    game = AlienInvasion()
    game.run()