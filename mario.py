import pygame
import winsound
import math
import random
pygame.init()

TRIANGLE_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
OUTER_BLOCK_COLOR = (0, 255, 0)
OUTER_BLOCK_HEIGHT = 200
OUTER_BLOCK_WIDTH = 1000

screen = pygame.display.set_mode((640, 480), 0, 32)
screen_width = screen.get_width()
screen_height = screen.get_height()
player = pygame.image.load('resources/player_img.png')
player_rect = player.get_rect()
pygame.display.set_caption("Platformer")

x, y = (100, 300)
player_position = (100, 300)
player_size = (75, 62)
game_over = False
clock = pygame.time.Clock()

def point_in_triangle(px, py, p1, p2, p3):
    def sign(x1, y1, x2, y2, x3, y3):
        return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

    d1 = sign(px, py, p1[0], p1[1], p2[0], p2[1])
    d2 = sign(px, py, p2[0], p2[1], p3[0], p3[1])
    d3 = sign(px, py, p3[0], p3[1], p1[0], p1[1])

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def valid_point(x, y):
    if x >= player_position[0] and x <= player_position[0] + player_size[0] and y >= player_position[1] and y <= player_position[1] + player_size[1]:
        return False
    return True

def generate_random_triangle(edge_length):
    # Calculate height of the equilateral triangle
    height = math.sqrt(3) / 2 * edge_length

    # Generate random coordinates for the triangle
    while(True):
        x1 = random.randint(0, screen_width - edge_length)
        y1 = random.randint(0, screen_height - int(height))
        if (valid_point(x1, y1)):
            break

    while (True):
        x2 = x1 + edge_length
        y2 = y1
        if (valid_point(x2, y2)):
            break

    while (True):
        x3 = x1 + edge_length / 2
        y3 = y1 + height
        if (valid_point(x3, y3)):
            break


    return [(x1, y1), (x2, y2), (x3, y3)]


TRIANGLE_EDGE_LEN = 50
TRIANGLE_POINTS = generate_random_triangle(TRIANGLE_EDGE_LEN)
TRIANGLE_POINTS2 = generate_random_triangle(TRIANGLE_EDGE_LEN)  # Adjusted y-coordinates

def play_music():
    winsound.PlaySound("Fluffing a Duck.wav", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)


jumping = False
jump_start = 0
gravity = 0.2
jump_speed = 10
max_jump_height = 200
jump_count = 0


def start_movement():
    global x, y
    global pressed

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        x += 0.5 * dt
    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
        x -= 0.5 * dt


def restart_player():
    global x, y
    x, y = (100, 300)

# def move_triangle(, distance):
#     p1, p2, p3 =
#     p1[0] = x
#     random_num = random.randint(-distance, distance)
#     return [(p1[0] + random_num, p1[1] + random_num), (p2[0] + random_num, p2[1] + random_num), (p3[0] + random_num, p3[1] + random_num)]

def restrict_movement():
    global x, y
    if x < 0:
        x = 0


def jumping_check():
    global jumping
    global jump_count
    global y
    global jump_start
    global pressed

    if not jumping and pressed[pygame.K_SPACE]:
        jumping = True
        jump_start = y
        jump_count += 1

    if jumping:
        y -= jump_speed
        if y < 0:
            y = 0
            jumping = False
        elif jump_start - y > player.get_height() * 3:
            jumping = False


def apply_gravity():
    global y
    if not jumping and y < 300:
        y += gravity * dt


def create_triangles():
    triangle_rect = pygame.draw.polygon(screen, TRIANGLE_COLOR, TRIANGLE_POINTS)
    player_rect.topleft = (x, y)
    triangle_rect2 = pygame.draw.polygon(screen, TRIANGLE_COLOR, TRIANGLE_POINTS2)

    # Return the rectangles bounding the triangles
    return triangle_rect, triangle_rect2


def blit_triangles():
    pygame.draw.polygon(screen, TRIANGLE_COLOR, TRIANGLE_POINTS)
    pygame.draw.polygon(screen, TRIANGLE_COLOR, TRIANGLE_POINTS2)


def create_base():
    outer_block_rect = pygame.draw.rect(screen, OUTER_BLOCK_COLOR, (0, 362, OUTER_BLOCK_WIDTH, OUTER_BLOCK_HEIGHT))


def blit_player():
    screen.blit(player, (x, y))


def check_for_touching_triangle():
    if player_rect.colliderect(triangle_rect) or player_rect.colliderect(triangle_rect2):
        restart_player()
triangle_rect, triangle_rect2 = create_triangles()
while not game_over:
    global pressed
    dt = clock.tick(60)  # Cap the frame rate to 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if y < 0:
        y = 0

    play_music()

    start_movement()

    restrict_movement()

    jumping_check()

    apply_gravity()

    # Get the rectangles bounding the triangles

    blit_triangles()

    # Background RGB color
    screen.fill((124, 249, 236))

    # Draw the triangles
    blit_triangles()

    create_base()

    blit_player()

    check_for_touching_triangle()

    pygame.display.flip()

pygame.quit()
