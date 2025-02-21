import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Funky Cowboy Shootout")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
BROWN = (139, 69, 19)

# Player (Cowboy) settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = HEIGHT - PLAYER_HEIGHT - 10
player_speed = 5

# Bullet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
bullet_speed = 10
bullets = []
bullet_cooldown = 15  # Frames between shots
bullet_timer = 0

# Enemy (Bandit) settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
enemy_speed = 2
enemy_rows = 3
enemy_cols = 8
enemies = []
enemy_direction = 1  # 1 for right, -1 for left
enemy_drop_speed = 20  # How fast they drop down
enemy_move_timer = 0
enemy_move_interval = 30  # Frames between moves

# Funky ricochet chance (special bullet effect)
RICOCHET_CHANCE = 0.1  # 10% chance for a bullet to bounce

# Score and game state
score = 0
font = pygame.font.SysFont("Arial", 30)
game_over = False

# Clock for frame rate
clock = pygame.time.Clock()
FPS = 60

# Spawn enemies in a grid
def spawn_enemies():
    for row in range(enemy_rows):
        for col in range(enemy_cols):
            enemy_x = col * (ENEMY_WIDTH + 20) + 50
            enemy_y = row * (ENEMY_HEIGHT + 20) + 50
            enemies.append([enemy_x, enemy_y])

# Move enemies with funky wobble
def move_enemies():
    global enemy_direction, enemy_move_timer
    enemy_move_timer += 1
    if enemy_move_timer >= enemy_move_interval:
        enemy_move_timer = 0
        # Check if any enemy hits the edge
        for enemy in enemies:
            if enemy[0] <= 0 or enemy[0] + ENEMY_WIDTH >= WIDTH:
                enemy_direction *= -1
                for e in enemies:
                    e[1] += enemy_drop_speed  # Drop down
                break
        # Move horizontally with a little funky sway
        for enemy in enemies:
            enemy[0] += enemy_speed * enemy_direction * (1 + 0.2 * math.sin(enemy[1] * 0.1))

# Draw funky cowboy (hat and all!)
def draw_player(x, y):
    pygame.draw.rect(screen, BROWN, (x, y, PLAYER_WIDTH, PLAYER_HEIGHT))  # Body
    pygame.draw.polygon(screen, YELLOW, [(x + 10, y), (x + PLAYER_WIDTH - 10, y), (x + PLAYER_WIDTH // 2, y - 20)])  # Funky hat

# Draw bandit enemies (with a mustache twist!)
def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, ENEMY_WIDTH, ENEMY_HEIGHT))  # Body
    pygame.draw.line(screen, BLACK, (x + 10, y + 10), (x + ENEMY_WIDTH - 10, y + 10), 3)  # Mustache

# Draw bullet (stylized as a bullet with a trail)
def draw_bullet(x, y):
    pygame.draw.rect(screen, YELLOW, (x, y, BULLET_WIDTH, BULLET_HEIGHT))
    pygame.draw.line(screen, WHITE, (x + BULLET_WIDTH // 2, y + BULLET_HEIGHT), (x + BULLET_WIDTH // 2, y + BULLET_HEIGHT + 5), 2)

# Main game loop
spawn_enemies()
running = True
while running:
    screen.fill(BLACK)  # Desert night sky vibe

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False​​​​​​​​​​​​​​​​​​​​​​​​​