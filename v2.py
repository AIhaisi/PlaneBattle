import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸和帧率
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Ninja")
clock = pygame.time.Clock()

# 加载图片
background = pygame.image.load("background.png")
fruit_images = [pygame.image.load(f"fruit{i}.png") for i in range(1, 5)]
cut_fruit_images = [
    (pygame.image.load(f"fruit{i}_1.png"), pygame.image.load(f"fruit{i}_2.png"))
    for i in range(1, 5)
]

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 字体
font = pygame.font.Font(None, 36)

# 游戏状态
game_over = False
game_start = False
score = 0

class Fruit:
    def __init__(self, image, cut_images):
        self.image = image
        self.cut_images = cut_images
        self.reset()

    def reset(self):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = SCREEN_HEIGHT + random.randint(50, 100)
        self.speed = random.randint(-10, -5)
        self.gravity = 0.5
        self.angle = random.randint(-20, 20)
        self.rot_speed = random.randint(-5, 5)
        self.cut = False
        self.cut_positions = None

    def update(self):
        self.y += self.speed
        self.speed += self.gravity
        self.angle += self.rot_speed

        if self.y > SCREEN_HEIGHT:
            self.reset()

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect.topleft)

    def check_collision(self, mouse_pos):
        if not self.cut:
            rect = self.image.get_rect(center=(self.x, self.y))
            if rect.collidepoint(mouse_pos):
                self.cut = True
                self.cut_positions = (self.x, self.y)
                return True
        return False

    def draw_cut(self):
        if self.cut_positions:
            x, y = self.cut_positions
            for i, cut_image in enumerate(self.cut_images):
                cut_rect = cut_image.get_rect(center=(x, y))
                offset = 20 if i == 0 else -20
                cut_rect.x += offset
                screen.blit(cut_image, cut_rect.topleft)

# 创建水果实例
fruits = [Fruit(fruit_images[i], cut_fruit_images[i]) for i in range(len(fruit_images))]

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# 主循环
while True:
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not game_start:
                game_start = True
                game_over = False
                score = 0
                for fruit in fruits:
                    fruit.reset()
            else:
                for fruit in fruits:
                    if fruit.check_collision(mouse_pos):
                        score += 1

    if game_start:
        for fruit in fruits:
            fruit.update()
            if fruit.cut:
                fruit.draw_cut()
            else:
                fruit.draw()

        draw_text(f"Score: {score}", font, WHITE, screen, SCREEN_WIDTH // 2, 30)

        if game_over:
            draw_text("Game Over", font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text("Click to Restart", font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
            game_start = False
    else:
        draw_text("Fruit Ninja", font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        draw_text("Click to Start", font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.display.flip()
    clock.tick(60)
