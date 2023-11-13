import pygame
import winsound

from board import Board
from colorRect import ColorRect
from obstacle import Obstacle
from player import Player
# from triangle import Triangle


class Game:

    def __init__(self):
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 480
        self.LAND_HEIGHT = 100
        self.TRIANGLE_EDGE_LENGTH = 100
        self.board = Board(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, (124, 249, 236))
        screen = self.board.screen
        land_color = pygame.Color(0, 255, 0)
        land_top = self.SCREEN_HEIGHT - self.LAND_HEIGHT
        self.land = ColorRect(screen, 0, land_top, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, land_color)

        self.player = Player(screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, land_top)

        obstacle_color = pygame.Color(255, 0, 0)
        # self.obstacles = [Triangle.generate_random_triangle(screen,
        #                                                     obstacle_color,
        #                                                     self.TRIANGLE_EDGE_LENGTH,
        #                                                     self.player.top_left,
        #                                                     self.player.size,
        #                                                     self.SCREEN_WIDTH,
        #                                                     self.SCREEN_HEIGHT,
        #                                                     self.land.top) for i in range(3)]

        self.obstacles = [Obstacle.create_obstacle(screen, self.SCREEN_WIDTH, self.player, land_top, obstacle_color) for i in range(4)]
    def play_music(self):
        winsound.PlaySound("Fluffing a Duck.wav", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)

    def run(self):
        clock = pygame.time.Clock()

        self.play_music()
        while not self.game_over():

            self.player.move_horizontally(self.obstacles)
            self.player.jumping_check(self.obstacles)

            self.player.apply_gravity(self.obstacles)

            # Get the rectangles bounding the triangles

            # Background RGB color
            self.board.draw()

            for obstacle in self.obstacles:
                obstacle.draw()

            self.land.draw()

            self.player.draw()

            self.player.check_for_touching_obstacle(self.obstacles)

            pygame.display.flip()

    def game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

