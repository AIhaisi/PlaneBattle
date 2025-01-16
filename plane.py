import pygame
import random

# 初始化 Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 512, 728
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("战机游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 加载资源
background = pygame.image.load("background.jpg")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
enemy_hit_img = pygame.image.load("enemy_hit.png")
explode_imgs = [pygame.image.load(f"explode{i}.png") for i in range(1, 12)]

# 加载中文字体
font_path = "SimHei.ttf"
font = pygame.font.Font(font_path, 36)
large_font = pygame.font.Font(font_path, 74)


# 定义玩家类
class Player:
    def __init__(self):
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8
        self.health = 100
        self.hit = False

        # 调整判定框
        self.rect.width = self.rect.width - 20  # 调整宽度
        self.rect.height = self.rect.height - 20  # 调整高度
        self.rect.x = self.rect.x + 10  # 调整左边界位置
        self.rect.y = self.rect.y + 10  # 调整上边界位置

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

    def draw(self):
        if self.hit:
            pygame.draw.rect(screen, RED, self.rect, 3)
            self.hit = False
        screen.blit(self.image, self.rect.topleft)

    def draw_health_bar(self):
        health_bar_width = 100
        health_bar_height = 10
        health_ratio = self.health / 100
        health_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 15, health_bar_width * health_ratio, health_bar_height)
        pygame.draw.rect(screen, GREEN, health_bar_rect)
        pygame.draw.rect(screen, WHITE, (self.rect.x, self.rect.y - 15, health_bar_width, health_bar_height), 2)


# 定义子弹类
class Bullet:
    def __init__(self, x, y, speed, color):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = speed
        self.color = color
        self.to_be_removed = False

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


# 定义敌方战机类
class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -100)
        self.speed = random.randint(2, 5)
        self.health = 2
        self.hit = False
        self.hit_once = False
        self.exploded = False
        self.explode_index = 0
        self.explode_images = random.sample(explode_imgs, len(explode_imgs))

    def update(self):
        if not self.exploded:
            self.rect.y += self.speed
            if self.rect.top > SCREEN_HEIGHT:
                self.reset()
        else:
            self.explode_index += 1

    def reset(self):
        self.rect.y = random.randint(-150, -100)
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.speed = random.randint(2, 5)
        self.hit = False
        self.hit_once = False
        self.exploded = False
        self.explode_index = 0
        self.explode_images = random.sample(explode_imgs, len(explode_imgs))
        self.health = 2

    def draw(self):
        if self.hit and not self.exploded:
            screen.blit(enemy_hit_img, self.rect.topleft)
            self.hit = False
        elif not self.exploded:
            screen.blit(self.image, self.rect.topleft)
        else:
            if self.explode_index < len(self.explode_images):
                screen.blit(self.explode_images[self.explode_index], self.rect.topleft)
            else:
                self.reset()

    def fire(self):
        return Bullet(self.rect.centerx - 2, self.rect.bottom, 5, RED)

    def hit_by_bullet(self):
        self.health -= 1
        self.hit = True
        if self.health <= 0:
            self.exploded = True
            return True  # 返回True表示敌机被击毁
        return False


# 显示开始界面
def show_start_screen():
    screen.fill(BLACK)
    text = large_font.render("战机游戏", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    text = font.render("按任意键开始", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False


# 显示游戏说明界面
def show_instructions_screen():
    screen.fill(BLACK)
    lines = [
        "游戏说明：",
        "1. 使用方向键移动",
        "2. 按空格键发射子弹",
        "3. 击毁敌机得分",
        "4. 不要放跑敌机",
        "5. 击败敌机回血",
        "6. 分数到达1000分通过",
        "",
        "按任意键继续"
    ]

    y = 50
    for line in lines:
        text = font.render(line, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
        y += 40

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False


# 显示结束界面
def show_end_screen(score):
    screen.fill(BLACK)
    text = large_font.render("游戏结束", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    score_text = font.render(f"得分: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    restart_text = font.render("重新开始", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    pygame.draw.rect(screen, WHITE, restart_rect, 2)
    screen.blit(restart_text, restart_rect.topleft)

    quit_text = font.render("退出游戏", True, WHITE)
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    pygame.draw.rect(screen, WHITE, quit_rect, 2)
    screen.blit(quit_text, quit_rect.topleft)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    game()
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

    return False


# 主循环
def game():
    player = Player()
    bullets = []
    enemy_bullets = []
    enemies = [Enemy() for _ in range(2,10)]     #一次刷新的敌机数量
    clock = pygame.time.Clock()
    enemy_timer = 0     #敌机刷新间隔，每秒60帧，每帧-1
    score = 0
    running = True
    last_shot = pygame.time.get_ticks()
    shot_delay = 100  # 每次射击的间隔时间，单位为毫秒

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - last_shot > shot_delay:
                bullets.append(Bullet(player.rect.centerx - 2, player.rect.top, -7, WHITE))
                last_shot = now

        if keys[pygame.K_LEFT]:
            player.move(-player.speed, 0)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed, 0)
        if keys[pygame.K_UP]:
            player.move(0, -player.speed)
        if keys[pygame.K_DOWN]:
            player.move(0, player.speed)

        for bullet in bullets:
            bullet.update()
            bullet.draw()
            if bullet.rect.bottom < 0:
                bullet.to_be_removed = True
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect) and not enemy.exploded:
                    bullet.to_be_removed = True
                    if enemy.hit_by_bullet():
                        score += 10  # 击毁敌机得分
                        player.health += 5
                        player.health = min(100, player.health)
                    break

        for enemy in enemies:
            if enemy.rect.bottom > SCREEN_HEIGHT:
                show_end_screen(score)
                running = False
                break

            if enemy.rect.bottom > 0 and random.random() < 0.01:
                enemy_bullets.append(enemy.fire())
            enemy.update()
            enemy.draw()

        for bullet in enemy_bullets:
            bullet.update()
            bullet.draw()
            if bullet.rect.top > SCREEN_HEIGHT:
                bullet.to_be_removed = True
            elif bullet.rect.colliderect(player.rect):
                bullet.to_be_removed = True
                player.health -= 5
                player.hit = True
                if player.health <= 0 or score >= 1000:
                    show_end_screen(score)

        # 移除需要删除的子弹
        bullets = [bullet for bullet in bullets if not bullet.to_be_removed]
        enemy_bullets = [bullet for bullet in enemy_bullets if not bullet.to_be_removed]

        if enemy_timer <= 0:
            enemies.append(Enemy())
            enemy_timer = 500
        else:
            enemy_timer -= 1

        player.draw()
        player.draw_health_bar()

        # 显示得分
        score_text = font.render(f"得分: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    show_start_screen()
    show_instructions_screen()
    game()
