import pygame

from point import Point

'''a player with a image in rectangle shape'''


class Player(pygame.Rect):

    def __init__(self, screen, screen_width, screen_height, land_top):
        self.jump_start = 0
        self.jump_count = 0
        self.jump_speed = 10
        self.screen = screen

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.land_top = land_top
        self.jumping = False
        self.image = pygame.image.load('resources/player_img.png')
        self.rect = self.image.get_rect()
        self.initial_left = 100
        self.initial_top = land_top - self.rect[3]
        super().__init__(self.initial_left, self.initial_top, self.rect[2], self.rect[3])

        self.top_left = Point(self.initial_left, self.initial_top)
        self.size = (self.rect[2], self.rect[3])
        self.dt = pygame.time.Clock().tick(800)
        self.gravity = 0.2 * self.dt
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def restart_player(self):
        self.update(self.initial_left, self.initial_top, self.w, self.h)

    def apply_gravity(self, obstacles):
        if not self.jumping:
            new_top = self.y + 0.5 * self.clock.tick(60)  # self.gravity

            new_feet = new_top + self.height
            if new_feet <= self.land_top:
                if not self.is_touching_obstacle([self.left, new_top, self.w, self.h], obstacles):
                    self.update(self.left, new_top, self.w, self.h)

    def move_horizontally(self, obstacles):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            left = self.x + 0.5 * self.clock.tick(60)
            if left >= self.screen_width - self.w:
                left = self.screen_width - self.w
            if not self.is_touching_obstacle([left, self.top, self.w, self.h], obstacles):
                self.update(left, self.top, self.w, self.h)
            return
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            left = self.x - 0.5 * self.clock.tick(60)
            if left <= 0:
                left = 0
            if not self.is_touching_obstacle([left, self.top, self.w, self.h], obstacles):
                self.update(left, self.top, self.w, self.h)
            return

    def jumping_check(self, obstacles):
        pressed = pygame.key.get_pressed()
        if not self.jumping and pressed[pygame.K_SPACE]:
            self.jumping = True
            self.jump_start = self.y
            self.jump_count += 1

        if self.jumping:
            top = self.y - 0.5 * self.clock.tick(60) # self.jump_speed
            if top < 0:
                top = 0
                self.jumping = False

            if self.jump_start - top > self.h * 3:
                self.jumping = False

            if not self.is_touching_obstacle([self.left, top, self.w, self.h], obstacles):
                self.update(self.left, top, self.w, self.h)

    @staticmethod
    def is_touching_obstacle(vector, obstacles):
        for obstacle in obstacles:
            if obstacle.colliderect(vector):
                return True
        return False

    def check_for_touching_obstacle(self, obstacles):
        for obstacle in obstacles:
            if self.colliderect(obstacle):
                self.restart_player()
                return
