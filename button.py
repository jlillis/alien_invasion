import pygame.font

class Button:
    """A class that implements simple UI buttons."""

    def __init__(self, game, text):
        """Initialize buttom attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        self._prep_text(text)

    def _prep_text(self, text):
        """Turn the text into a rendered image centered on the button."""
        self.text_image = self.font.render(text, True, self.text_color, self.button_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center
        
    def draw_button(self):
        """Render the button on-screen."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)