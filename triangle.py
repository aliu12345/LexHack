
import math
import random

import pygame

from point import Point


class Triangle:
    def __init__(self, screen, color,  p1:Point, p2:Point, p3:Point):
        self.screen = screen
        self.color = color
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def point_in_triangle(self, px, py):
        def sign(x1, y1, x2, y2, x3, y3):
            return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

        d1 = sign(px, py, self.p1.x_axis, self.p1.y_axis, self.p2.x_axis, self.p2.y_axis)
        d2 = sign(px, py, self.p2.x_axis, self.p2.y_axis, self.p3.x_axis, self.p3.y_axis)
        d3 = sign(px, py, self.p3.x_axis, self.p3.y_axis, self.p1.x_axis, self.p1.y_axis)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    @staticmethod
    def collide(x, y, player_position, player_size):
        if player_position.x_axis <= x <= player_position.x_axis + player_size[0] and \
                player_position.y_axis <= y <= player_position.y_axis + player_size[1]:
            return True
        return False

    def on_screen(self, screen_width, screen_height):
        if self.p1.x_axis < 0 or \
                self.p1.x_axis > screen_width or \
                self.p1.y_axis < 0 or \
                self.p1.y_axis > screen_height or \
                self.p2.x_axis < 0 or \
                self.p2.x_axis > screen_width or \
                self.p2.y_axis < 0 or \
                self.p2.y_axis > screen_height or \
                self.p3.x_axis < 0 or \
                self.p3.x_axis > screen_width or \
                self.p3.y_axis < 0 or \
                self.p3.y_axis > screen_height:
            return False
        return True

    @staticmethod
    def generate_random_triangle(screen, color, edge_length, player_position, player_size, screen_width, screen_height,
                                 land_top):
        # Calculate height of the equilateral triangle
        while (True):
            height = math.sqrt(3) / 2 * edge_length
            # Generate random coordinates for the triangle
            x1 = random.randint(0, screen_width - edge_length)
            y1 = random.randint(0, screen_height - int(height))
            if Triangle.collide(x1, y1, player_position, player_size):
                continue
            if y1 > land_top:
                continue
            x2 = x1 + edge_length
            y2 = y1
            if Triangle.collide(x2, y2, player_position, player_size):
                continue
            x3 = x1 + edge_length / 2
            y3 = y1 - height
            if Triangle.collide(x3, y3, player_position, player_size):
                continue
            triangle = Triangle(screen, color, Point(x1, y1), Point(x2, y2), Point(x3, y3))
            if triangle.on_screen(screen_width, screen_height):
                return triangle


    def move_triangle(self, player_position, player_size, screen_width, screen_height, base):
        # Calculate height of the equilateral triangle
        move_x = random.randint(-5, 5)
        move_y = random.randint(-5, 5)
        while(True):
            # Generate random coordinates for the triangle
            x1 = self.p1.x_axis + move_x
            y1 = self.p1.y_axis + move_y
            if Triangle.collide(x1, y1, player_position, player_size):
                continue
            if y1 > base:
                continue
            x2 = self.p2.x_axis + move_x
            y2 = self.p2.y_axis + move_y
            if Triangle.collide(x2, y2, player_position, player_size):
                continue
            x3 = self.p3.x_axis + move_x
            y3 = self.p3.y_axis + move_y
            if Triangle.collide(x3, y3, player_position, player_size):
                continue
            triangle = Triangle(self.screen, self.color, Point(x1, y1), Point(x2, y2), Point(x3, y3))
            if triangle.on_screen(screen_width, screen_height):
                self.p1, self.p2, self.p3 = triangle.p1, triangle.p2, triangle.p3
                break

    def to_tuple_sequence(self):
        return [self.p1.to_tuple(), self.p2.to_tuple(), self.p3.to_tuple()]

    def draw(self):
        pygame.draw.polygon(self.screen, self.color, self.to_tuple_sequence())

