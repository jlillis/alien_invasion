import json
import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    "A class to manage scoring information."

    def __init__(self, game):
        """Initialize the scoreboard."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.score = 0
        self.high_score = self._load_high_score()

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self._prep_score()
        self._prep_high_score()
        self.prep_level()
        self.prep_ships()

    def draw(self):
        """Draw score the the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def reset(self):
        """Resets the scoreboard."""
        self.score = 0
        self._prep_score()
        self._prep_high_score()
        self.prep_level()
        self.prep_ships()

    def set_score(self, score):
        """Updates the player's score."""
        # Update the score display
        self.score = score
        self._prep_score()

        # Update the high score if required
        if self.score > self.high_score:
            self.high_score = score
            self._prep_high_score()

    def prep_level(self):
        """Turn the level in to rendered image."""
        level_str = str(self.game.level)
        self.level_image = self.font.render(level_str, True, self.text_color,
                                            self.settings.bg_color)

        # Position level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """ Show how many ships are left."""
        self.ships = Group()
        for ship_id in range(self.game.ships_remaining):
            ship = Ship(self.game)
            ship.rect.x = 10 + ship_id * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def save_high_score(self):
        """Saves the high score to disk."""
        try:
            with open("scores.json", 'w') as file:
                json.dump(self.high_score, file)
        except:
            print("Failed to write high score to scores.json!")

    def _load_high_score(self):
        """Returns the high score from disc, or 0 if not found."""
        try:
            with open("scores.json") as file:
                return int(json.load(file))
        except:
            print("Failed to read high score from scores.json!")
            return 0

    def _prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.score, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def _prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.high_score, -1)
        score_str = "{:,}".format(high_score)
        score_str = str(self.high_score)
        self.high_score_image = self.font.render(score_str, True, self.text_color,
                                                 self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
