import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 5
BULLET_SPEED = 7

# Enemy settings
ENEMY_SIZE = 40
ENEMY_SPEED = 2
ENEMY_DROP = 20
NUM_ENEMIES = 8
ENEMY_SPACING = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x += self.speed * self.direction

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

        # Create enemies
        for row in range(3):
            for col in range(NUM_ENEMIES):
                enemy = Enemy(col * (ENEMY_SIZE + ENEMY_SPACING) + 50,
                            row * (ENEMY_SIZE + 20) + 50)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

    def update(self):
        self.all_sprites.update()

        # Check if enemies need to change direction
        for enemy in self.enemies:
            if enemy.rect.right >= WINDOW_WIDTH or enemy.rect.left <= 0:
                for e in self.enemies:
                    e.direction *= -1
                    e.rect.y += ENEMY_DROP
                break

        # Check for collisions
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            self.score += 10

        # Check if enemies reached the bottom
        for enemy in self.enemies:
            if enemy.rect.bottom >= WINDOW_HEIGHT - 50:
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 