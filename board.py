import pygame
class Board():

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        self.color = color

    def check_point_on_board(self, point):
        return 0 <= point.x_axis <= self.width and 0 <= point.y_axis <= self.height

    def draw(self):
        self.screen.fill(self.color)