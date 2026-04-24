import pygame
import random
import math
import sys

# Pygame ni ishga tushirish
pygame.init()

# Ekran o'lchamlari
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Kosmik Otishma - Space Shooter")

# Ranglar
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
PURPLE = (200, 0, 255)

# Soat (FPS uchun)
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Zarralar klassi (portlash uchun)
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.size = random.randint(2, 5)
        self.lifetime = random.randint(20, 40)
        self.age = 0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravitatsiya
        self.age += 1
        self.size = max(1, self.size - 0.1)
    
    def draw(self, screen):
        if self.age < self.lifetime:
            alpha = int(255 * (1 - self.age / self.lifetime))
            color = (self.color[0], self.color[1], self.color[2], alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
    
    def is_dead(self):
        return self.age >= self.lifetime

# Yulduz klassi (fon animatsiya)
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(100, 255)
    
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
    
    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

# O'yinchi kemasi
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.width = 40
        self.height = 50
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.shoot_cooldown = 0
    
    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(0, self.x - self.speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(WIDTH - self.width, self.x + self.speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = max(0, self.y - self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y = min(HEIGHT - self.height, self.y + self.speed)
    
    def shoot(self):
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = 15
            return Bullet(self.x + self.width // 2, self.y, -10, BLUE)
        return None
    
    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def draw(self, screen):
        # Kema tanasi
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 2, self.y + self.height - 10),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, BLUE, points)
        pygame.draw.polygon(screen, WHITE, points, 2)
        
        # Dvigatel alangasi (animatsiya)
        flame_length = random.randint(10, 20)
        flame_points = [
            (self.x + 10, self.y + self.height),
            (self.x + 15, self.y + self.height + flame_length),
            (self.x + 20, self.y + self.height)
        ]
        pygame.draw.polygon(screen, ORANGE, flame_points)
        
        flame_points2 = [
            (self.x + self.width - 10, self.y + self.height),
            (self.x + self.width - 15, self.y + self.height + flame_length),
            (self.x + self.width - 20, self.y + self.height)
        ]
        pygame.draw.polygon(screen, ORANGE, flame_points2)

# Dushman kemasi
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 40)
        self.y = random.randint(-100, -40)
        self.width = 40
        self.height = 40
        self.speed = random.uniform(1, 3)
        self.health = 30
        self.shoot_timer = random.randint(60, 120)
    
    def update(self):
        self.y += self.speed
        self.shoot_timer -= 1
    
    def shoot(self):
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(60, 120)
            return Bullet(self.x + self.width // 2, self.y + self.height, 7, RED)
        return None
    
    def draw(self, screen):
        # Dushman tanasi
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, ORANGE, (self.x, self.y, self.width, self.height), 2)
        
        # Ko'z
        pygame.draw.circle(screen, YELLOW, (int(self.x + 15), int(self.y + 20)), 5)
        pygame.draw.circle(screen, YELLOW, (int(self.x + 25), int(self.y + 20)), 5)
    
    def is_off_screen(self):
        return self.y > HEIGHT

# O'q klassi
class Bullet:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 5
        self.height = 15
    
    def update(self):
        self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.width // 2, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x - self.width // 2, self.y, self.width, self.height), 1)
    
    def is_off_screen(self):
        return self.y < -20 or self.y > HEIGHT + 20

# Bonus klassi
class PowerUp:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -30
        self.size = 20
        self.speed = 2
        self.type = random.choice(['health', 'shield'])
        self.angle = 0
    
    def update(self):
        self.y += self.speed
        self.angle += 5
    
    def draw(self, screen):
        color = GREEN if self.type == 'health' else PURPLE
        points = []
        for i in range(8):
            angle = math.radians(self.angle + i * 45)
            if i % 2 == 0:
                r = self.size
            else:
                r = self.size // 2
            x = self.x + r * math.cos(angle)
            y = self.y + r * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, color, points)
    
    def is_off_screen(self):
        return self.y > HEIGHT

# Asosiy o'yin funksiyasi
def main():
    # O'yin ob'ektlari
    player = Player()
    enemies = []
    player_bullets = []
    enemy_bullets = []
    stars = [Star() for _ in range(100)]
    particles = []
    powerups = []
    
    # O'yin o'zgaruvchilari
    score = 0
    level = 1
    enemy_spawn_timer = 0
    powerup_spawn_timer = 0
    game_over = False
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Hodisalarni tekshirish
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bullet = player.shoot()
                    if bullet:
                        player_bullets.append(bullet)
                if event.key == pygame.K_r and game_over:
                    # O'yinni qayta boshlash
                    player = Player()
                    enemies = []
                    player_bullets = []
                    enemy_bullets = []
                    particles = []
                    powerups = []
                    score = 0
                    level = 1
                    game_over = False
        
        if not game_over:
            # Klaviatura kiritishini olish
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.update()
            
            # Dushmanlarni yaratish
            enemy_spawn_timer += 1
            spawn_rate = max(30, 90 - level * 5)
            if enemy_spawn_timer > spawn_rate:
                enemies.append(Enemy())
                enemy_spawn_timer = 0
            
            # Bonuslarni yaratish
            powerup_spawn_timer += 1
            if powerup_spawn_timer > 300:
                powerups.append(PowerUp())
                powerup_spawn_timer = 0
            
            # Dushmanlarni yangilash
            for enemy in enemies[:]:
                enemy.update()
                bullet = enemy.shoot()
                if bullet:
                    enemy_bullets.append(bullet)
                
                if enemy.is_off_screen():
                    enemies.remove(enemy)
            
            # O'qlarni yangilash
            for bullet in player_bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    player_bullets.remove(bullet)
            
            for bullet in enemy_bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    enemy_bullets.remove(bullet)
            
            # Bonuslarni yangilash
            for powerup in powerups[:]:
                powerup.update()
                if powerup.is_off_screen():
                    powerups.remove(powerup)
            
            # To'qnashuvlarni tekshirish
            for bullet in player_bullets[:]:
                for enemy in enemies[:]:
                    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.width and
                        bullet.y > enemy.y and bullet.y < enemy.y + enemy.height):
                        enemy.health -= 10
                        if bullet in player_bullets:
                            player_bullets.remove(bullet)
                        
                        if enemy.health <= 0:
                            # Portlash effekti
                            for _ in range(30):
                                particles.append(Particle(enemy.x + enemy.width // 2, 
                                                         enemy.y + enemy.height // 2, 
                                                         random.choice([RED, ORANGE, YELLOW])))
                            if enemy in enemies:
                                enemies.remove(enemy)
                            score += 10
                            
                            # Daraja oshirish
                            if score % 100 == 0:
                                level += 1
                        break
            
            # Dushman o'qlari bilan to'qnashuv
            for bullet in enemy_bullets[:]:
                if (bullet.x > player.x and bullet.x < player.x + player.width and
                    bullet.y > player.y and bullet.y < player.y + player.height):
                    player.health -= 10
                    if bullet in enemy_bullets:
                        enemy_bullets.remove(bullet)
                    
                    # Zarar effekti
                    for _ in range(10):
                        particles.append(Particle(player.x + player.width // 2,
                                                 player.y + player.height // 2,
                                                 RED))
            
            # Dushman bilan to'qnashuv
            for enemy in enemies[:]:
                if (player.x < enemy.x + enemy.width and
                    player.x + player.width > enemy.x and
                    player.y < enemy.y + enemy.height and
                    player.y + player.height > enemy.y):
                    player.health -= 20
                    if enemy in enemies:
                        enemies.remove(enemy)
                    
                    for _ in range(20):
                        particles.append(Particle(enemy.x + enemy.width // 2,
                                                 enemy.y + enemy.height // 2,
                                                 ORANGE))
            
            # Bonus bilan to'qnashuv
            for powerup in powerups[:]:
                if (player.x < powerup.x + powerup.size and
                    player.x + player.width > powerup.x - powerup.size and
                    player.y < powerup.y + powerup.size and
                    player.y + player.height > powerup.y - powerup.size):
                    if powerup.type == 'health':
                        player.health = min(player.max_health, player.health + 30)
                    if powerup in powerups:
                        powerups.remove(powerup)
                    
                    for _ in range(15):
                        particles.append(Particle(powerup.x, powerup.y, GREEN))
            
            # O'limni tekshirish
            if player.health <= 0:
                game_over = True
                for _ in range(50):
                    particles.append(Particle(player.x + player.width // 2,
                                             player.y + player.height // 2,
                                             random.choice([RED, ORANGE, YELLOW, WHITE])))
        
        # Yulduzlarni yangilash
        for star in stars:
            star.update()
        
        # Zarralarni yangilash
        for particle in particles[:]:
            particle.update()
            if particle.is_dead():
                particles.remove(particle)
        
        # ==================== CHIZISH ====================
        screen.fill(BLACK)
        
        # Yulduzlarni chizish
        for star in stars:
            star.draw(screen)
        
        if not game_over:
            # O'yinchini chizish
            player.draw(screen)
            
            # Dushmanlarni chizish
            for enemy in enemies:
                enemy.draw(screen)
            
            # O'qlarni chizish
            for bullet in player_bullets:
                bullet.draw(screen)
            
            for bullet in enemy_bullets:
                bullet.draw(screen)
            
            # Bonuslarni chizish
            for powerup in powerups:
                powerup.draw(screen)
            
            # Sog'liq ko'rsatkichi
            pygame.draw.rect(screen, RED, (10, 10, 200, 20))
            health_width = int(200 * (player.health / player.max_health))
            pygame.draw.rect(screen, GREEN, (10, 10, health_width, 20))
            pygame.draw.rect(screen, WHITE, (10, 10, 200, 20), 2)
            
            health_text = font.render(f"HP: {player.health}/{player.max_health}", True, WHITE)
            screen.blit(health_text, (15, 12))
            
            # Ball va daraja
            score_text = font.render(f"Ball: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH - 180, 10))
            
            level_text = font.render(f"Daraja: {level}", True, YELLOW)
            screen.blit(level_text, (WIDTH - 200, 50))
            
            # Yo'riqnoma
            help_text = pygame.font.Font(None, 24).render("WASD/Strelkalar - harakat | SPACE - otish", True, WHITE)
            screen.blit(help_text, (WIDTH // 2 - 200, HEIGHT - 30))
        
        # Zarralarni chizish
        for particle in particles:
            particle.draw(screen)
        
        # O'yin tugadi ekrani
        if game_over:
            # Qorong'i fon
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # O'yin tugadi matni
            game_over_text = big_font.render("O'YIN TUGADI!", True, RED)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
            screen.blit(game_over_text, text_rect)
            
            # Yakuniy ball
            final_score = font.render(f"Sizning ballingiz: {score}", True, WHITE)
            score_rect = final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(final_score, score_rect)
            
            # Daraja
            final_level = font.render(f"Erishilgan daraja: {level}", True, YELLOW)
            level_rect = final_level.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(final_level, level_rect)
            
            # Qayta boshlash
            restart_text = font.render("Qayta boshlash uchun 'R' ni bosing", True, GREEN)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
            screen.blit(restart_text, restart_rect)
            
            # Chiqish
            exit_text = pygame.font.Font(None, 28).render("Chiqish uchun oynani yoping", True, WHITE)
            exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
            screen.blit(exit_text, exit_rect)
        
        # Ekranni yangilash
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()