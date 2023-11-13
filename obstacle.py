import random

from colorRect import ColorRect


class Obstacle(ColorRect):
    def __init__(self, screen, left, top, width, height, color):
        super().__init__(screen, left, top, width, height, color)

    @staticmethod
    def create_obstacle(screen, screen_width, player, land_top, color):
        size = random.randint(50, 100)
        # make sure this obstacle don't in the same column as the player initially.
        left = random.randint(player.left + player.w, screen_width - size)
        top = random.randint(0, land_top - size)
        return Obstacle(screen, left, top, size, size, color)

    def move(self):
        pass
