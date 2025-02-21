import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (200, 50, 50)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
FPS = 60

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cowboy vs. Bandits")

# Load assets
cowboy_img = pygame.image.load("cowboy.png")
cowboy_img = pygame.transform.scale(cowboy_img, (80, 80))

bandit_img = pygame.image.load("bandit.png")
bandit_img = pygame.transform.scale(bandit_img, (50, 50))

background = pygame.image.load("saloon.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# Cowboy class
class Cowboy:
    def __init__(self):
        self.x = WIDTH // 2 - 40
        self.y = HEIGHT - 100
        self.speed = 5
        self.width = 80
        self.height = 80
        self.bullets = []

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

    def shoot(self):
        self.bullets.append([self.x + self.width // 2, self.y])
        shoot_sound.play()

    def draw(self):
        screen.blit(cowboy_img, (self.x, self.y))
        for bullet in self.bullets:
            pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], 5, 15))

# Bandit class
class Bandit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 2
        self.direction = random.choice(["left", "right"])

    def move(self):
        if self.direction == "left":
            self.x -= self.speed
            if self.x < 0:
                self.direction = "right"
                self.y += 30
        else:
            self.x += self.speed
            if self.x > WIDTH - self.width:
                self.direction = "left"
                self.y += 30
        
        if random.random() < 0.02:  # Randomly change direction
            self.direction = "left" if self.direction == "right" else "right"

    def draw(self):
        screen.blit(bandit_img, (self.x, self.y))

# Game variables
cowboy = Cowboy()
bandits = [Bandit(random.randint(0, WIDTH - 50), random.randint(20, 100)) for _ in range(5)]
score = 0
spawn_rate = 60
frame_count = 0
running = True

# Game loop
while running:
    pygame.time.delay(16)  # ~60 FPS
    screen.blit(background, (0, 0))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cowboy.move("left")
    if keys[pygame.K_RIGHT]:
        cowboy.move("right")
    if keys[pygame.K_SPACE]:
        cowboy.shoot()

    # Update bullets
    for bullet in cowboy.bullets[:]:
        bullet[1] -= 10
        if bullet[1] < 0:
            cowboy.bullets.remove(bullet)

    # Update bandits
    for bandit in bandits[:]:
        bandit.move()
        if bandit.y > HEIGHT - 100:  # Game over condition
            running = False
        
        for bullet in cowboy.bullets[:]:
            if bandit.x < bullet[0] < bandit.x + bandit.width and bandit.y < bullet[1] < bandit.y + bandit.height:
                hit_sound.play()
                bandits.remove(bandit)
                cowboy.bullets.remove(bullet)
                score += 50

    # Add new bandits
    frame_count += 1
    if frame_count >= spawn_rate:
        bandits.append(Bandit(random.randint(0, WIDTH - 50), 20))
        frame_count = 0
        spawn_rate = max(20, spawn_rate - 1)  # Increase difficulty

    # Draw everything
    cowboy.draw()
    for bandit in bandits:
        bandit.draw()
    
    # Score display
    font = pygame.font.SysFont("Comic Sans MS", 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
