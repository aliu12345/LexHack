import pygame


class ColorRect(pygame.Rect):

    def __init__(self, screen, left, top, width, height, color):
        super().__init__(left, top, width, height)
        self.screen = screen
        self.color = color

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self)
