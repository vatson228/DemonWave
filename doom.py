try:
    from pypresence import Presence, DiscordNotFound
except:
    pass
import psutil
import pygame
import random
import math
import sys
import time
import json
import os
from threading import Thread
pygame.mixer.pre_init(frequency=44100, size=-16, channels=10, buffer=512)
pygame.mixer.init()
channel = pygame.mixer.find_channel()
pygame.mixer.music.load("music/background_music.mp3")
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=1500)
pygame.mixer.music.set_volume(0.5)
channel = pygame.mixer.find_channel(force=True)
shotgun_sound = pygame.mixer.Sound("sound/drobo_ik-vystrel (mp3cut.net).mp3")
shotgun_sound.set_volume(0.5)
rpg_sound = pygame.mixer.Sound("sound/rpg.mp3")
rpg_sound.set_volume(1)
sniper_rifle_sound = pygame.mixer.Sound("sound/sniper rifle.mp3")
sniper_rifle_sound.set_volume(1)
machinegun_sound = pygame.mixer.Sound("sound/gun-machine-gun-automatic-762-caliber-m-134-minigun-burst-distant-perspecti_fju3jqv_ (mp3cut.net).mp3")
machinegun_sound.set_volume(0.5)
pistol_sound = pygame.mixer.Sound("sound/pistol.mp3")
pistol_sound.set_volume(0.20)
zombie = "texture"
imp = "texture"
cacodemon = "texture"
cyberdemon = "texture"
archvile = "texture"
hellknight = "texture"
# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DemonWave")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
DARK_RED = (150, 0, 0)
GRAY = (100, 100, 100)
ds_found = 0
def is_process_with_keyword_running(keyword):
    """
    Проверяет, есть ли процессы, содержащие ключевое слово в имени
    """
    for proc in psutil.process_iter(['name']):
        try:
            if keyword.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def try_found_ds():
    try:
        global ds_found
        if is_process_with_keyword_running('Discord'):
            ds_found == 0
        if ds_found == 0:
            # Замените на ваш Client ID из Developer Portal
            CLIENT_ID = "1414290161969135809"
            # Инициализация RPC
            RPC = Presence(CLIENT_ID)
            RPC.connect()
            # Установка базового статуса
            pass
            RPC.update(
            state="Играет в DemonWave",
            large_image="a_simple_and_moder_image",
            small_image="a_simple_and_moder_image",
            start=time.time()  # Время начала активности (сейчас)
            )
            ds_found += 1
    except:
        pass
# Игровые переменные
debug  = False
wave_number = 1
Monster_upgraded_speed = 0
Monster_upgraded_max_health = 0
Monster_upgraded_damage = 0
CLIENT_ID = "1414290161969135809"
RPC = Presence(CLIENT_ID)
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)
class Player:
    def __init__(self):
        self.x = WIDTH
        self.y = HEIGHT
        self.health_regen = 0
        self.regen_timer = 0
        self.radius = 20
        self.speed = 7
        self.max_health = 100
        self.health = self.max_health
        self.score = 0 
        self.time_alive = 0
        self.weapon = "pistol"
        self.weapons = {
            "pistol": {"damage": 10, "cooldown": 30, "color": GRAY},
            "shotgun": {"damage": 10, "cooldown": 80, "color": BLUE},
            "machinegun": {"damage": 1, "cooldown": 3, "color": GREEN},
            "rocketlauncher": {"damage": 100, "cooldown": 100, "color": (255, 100, 0)},
            "sniper rifle": {"damage": 70, "cooldown": 80, "color": GRAY}
        }
        self.cooldown = 0
        self.bullets = []
        
    def move(self, keys):
        if keys[pygame.K_w] and self.y - self.speed > 0:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y + self.speed < HEIGHT:
            self.y += self.speed
        if keys[pygame.K_a] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x + self.speed < WIDTH:
            self.x += self.speed
            
    def shoot(self, mouse_pos):
        if self.cooldown <= 0:
            dx = mouse_pos[0] - self.x
            dy = mouse_pos[1] - self.y
            dist = max(1, math.sqrt(dx * dx + dy * dy))
            dx, dy = dx / dist, dy / dist
            
            if self.weapon == "shotgun":
                channel.play(shotgun_sound)
                for angle in [-0.4, -0.2, 0, 0.2, 0.4]:
                    angle_dx = dx * math.cos(angle) - dy * math.sin(angle)
                    angle_dy = dx * math.sin(angle) + dy * math.cos(angle)
                    self.bullets.append({
                        "x": self.x, 
                        "y": self.y, 
                        "dx": angle_dx * 30, 
                        "dy": angle_dy * 30,
                        "damage": self.weapons[self.weapon]["damage"],
                        "color": self.weapons[self.weapon]["color"]
                    })
            elif self.weapon == "rocketlauncher":
                channel.play(rpg_sound)
                self.bullets.append({
                    "x": self.x, 
                    "y": self.y, 
                    "dx": dx * 30, 
                    "dy": dy * 30,
                    "damage": self.weapons[self.weapon]["damage"],
                    "color": self.weapons[self.weapon]["color"]
                })
            elif self.weapon == "sniper rifle":
                channel.play(sniper_rifle_sound)
                self.bullets.append({
                    "x": self.x, 
                    "y": self.y, 
                    "dx": dx * 30, 
                    "dy": dy * 30,
                    "damage": self.weapons[self.weapon]["damage"],
                    "color": self.weapons[self.weapon]["color"]
                })
            elif self.weapon == "machinegun":
                channel.play(machinegun_sound)
                self.bullets.append({
                    "x": self.x, 
                    "y": self.y, 
                    "dx": dx * 30, 
                    "dy": dy * 30,
                    "damage": self.weapons[self.weapon]["damage"],
                    "color": self.weapons[self.weapon]["color"]
                })
            elif self.weapon == "pistol":
                channel.play(pistol_sound)
                self.bullets.append({
                    "x": self.x, 
                    "y": self.y, 
                    "dx": dx * 30, 
                    "dy": dy * 30,
                    "damage": self.weapons[self.weapon]["damage"],
                    "color": self.weapons[self.weapon]["color"]
                })
            else:
                self.bullets.append({
                    "x": self.x, 
                    "y": self.y, 
                    "dx": dx * 30, 
                    "dy": dy * 30,
                    "damage": self.weapons[self.weapon]["damage"],
                    "color": self.weapons[self.weapon]["color"]
                })
                
            self.cooldown = self.weapons[self.weapon]["cooldown"]
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        # Обновление пуль
        for bullet in self.bullets:
            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]
            
            # Удаление пуль за пределами экрана
            if (bullet["x"] < 0 or bullet["x"] > WIDTH or 
                bullet["y"] < 0 or bullet["y"] > HEIGHT):
                self.bullets.remove(bullet)
        self.regen_timer += 1
        if self.regen_timer >= 60:  # 60 кадров = 1 секунда
            try:
                th = Thread(target=try_found_ds, args=(1))
                th.start
            except:
                pass
            self.regen_timer = 0
            if self.health_regen > 0 and self.health < self.max_health:
                self.health = min(self.max_health, self.health + self.health_regen)
        
        
    
    def draw(self, screen):
        # Рисование игрока
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 5)
        
        # Рисование пуль
        for bullet in self.bullets:
            pygame.draw.circle(screen, bullet["color"], 
                              (int(bullet["x"]), int(bullet["y"])), 5)
        
        if self.health_regen > 0:
            regen_text = small_font.render(f"Regen: +{self.health_regen} HP/s", True, GREEN)
            screen.blit(regen_text, (10, 70))
        
        # Рисование здоровья
        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, 200 * (self.health / self.max_health), 20))
        self.fixhealth = round(self.health)
        health_text = font.render(f"HP: {self.fixhealth}/{self.max_health}", True, WHITE)
        screen.blit(health_text, (15, 12))
        
        # Рисование очков и времени
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 150, 10))
        
        time_text = font.render(f"Time: {int(self.time_alive)}s", True, WHITE)
        screen.blit(time_text, (WIDTH - 150, 50))

        
        # Рисование текущего оружия
        weapon_text = font.render(f"Weapon: {self.weapon}", True, self.weapons[self.weapon]["color"])
        screen.blit(weapon_text, (10, 40))
# Класс для системы частиц
class Monster:
    def __init__(self, x, y, monster_type):
        self.x = x
        self.y = y
        self.type = monster_type
        if monster_type == "zombie":
            self.radius = 25
            self.speed = 2.5 + Monster_upgraded_speed
            self.health = 30 + Monster_upgraded_max_health
            self.damage = 5 + Monster_upgraded_damage
            self.color = (100, 150, 100)
        elif monster_type == "imp":
            self.radius = 20
            self.speed = 3.5 + Monster_upgraded_speed
            self.health = 20 + Monster_upgraded_max_health
            self.damage = 8 + Monster_upgraded_damage
            self.color = (150, 100, 100)
        elif monster_type == "cacodemon":
            self.radius = 30
            self.speed = 1.5 + Monster_upgraded_speed
            self.health = 50 + Monster_upgraded_max_health
            self.damage = 15 + Monster_upgraded_damage
            self.color = (200, 100, 200)
        elif monster_type == "cyberdemon":
            self.radius = 40
            self.speed = 1.15 + Monster_upgraded_speed
            self.health = 100 + Monster_upgraded_max_health
            self.damage = 25 + Monster_upgraded_damage
            self.color = (150, 150, 150)
        elif monster_type == "archvile":
            self.radius = 28
            self.speed = 1.70 + Monster_upgraded_speed
            self.health = 80 + Monster_upgraded_max_health
            self.damage = 20 + Monster_upgraded_damage
            self.color = (255, 100, 0)
        elif monster_type == "hellknight":
            self.radius = 32
            self.speed = 2.55 + Monster_upgraded_speed
            self.health = 120 + Monster_upgraded_max_health
            self.damage = 30 + Monster_upgraded_damage
            self.color = (150, 0, 50)        
    
    def move(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = max(1, math.sqrt(dx * dx + dy * dy))
        self.x += (dx / dist) * self.speed
        self.y += (dy / dist) * self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Рисование глаз для монстров
        angle = math.atan2(self.y - player.y, self.x - player.x)
        eye_x = self.x + math.cos(angle) * self.radius * 0.6
        eye_y = self.y + math.sin(angle) * self.radius * 0.6
        pygame.draw.circle(screen, RED, (int(eye_x), int(eye_y)), 5)
class UpgradeScreen:
    def __init__(self, player):
        self.player = player
        self.upgrades = {
            "health": {"cost": 50, "value": 20, "name": "Max Health +20"},
            "speed": {"cost": 40, "value": 1, "name": "Speed +1"},
            "damage": {"cost": 60, "value": 5, "name": "Damage +5"},
            "heal": {"cost": 30, "value": 50, "name": "Heal +50 HP"},
            "regen": {"cost": 70, "value": 1, "name": "Health Regen +1 HP/s"},
        }
        self.selected = 0
    def draw(self, screen):
        screen.fill(BLACK)
        
        title = font.render("UPGRADE SCREEN", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        score_text = font.render(f"Available Points: {self.player.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 100))
        
        time_text = font.render(f"Time Survived: {int(self.player.time_alive)} seconds", True, WHITE)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 140))
        
        # Рисование опций улучшений
        y_pos = 200
        for i, (key, upgrade) in enumerate(self.upgrades.items()):
            color = YELLOW if i == self.selected else WHITE
            text = font.render(f"{upgrade['name']} - Cost: {upgrade['cost']}", True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))
            y_pos += 50
            
        hint = small_font.render("Use UP/DOWN to select, ENTER to buy, SPACE to continue", True, GREEN)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 50))
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.upgrades)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.upgrades)
            elif event.key == pygame.K_RETURN:
                self.buy_upgrade()
            elif event.key == pygame.K_SPACE:
                return "start_game" 
        return "upgrade"
    
    def buy_upgrade(self):
        upgrade_key = list(self.upgrades.keys())[self.selected]
        upgrade = self.upgrades[upgrade_key]
        
        if self.player.score >= upgrade["cost"]:
            self.player.score -= upgrade["cost"]
            
            if upgrade_key == "health":
                self.player.max_health += upgrade["value"]
                self.player.health = self.player.max_health
            elif upgrade_key == "speed":
                self.player.speed += upgrade["value"]
            elif upgrade_key == "damage":
                for weapon in self.player.weapons:
                    self.player.weapons["pistol"]["damage"] += 0.5
                    self.player.weapons["shotgun"]["damage"] += 0.5
                    self.player.weapons["machinegun"]["damage"] += 0.05
                    self.player.weapons["sniper rifle"]["damage"] += 3.5
                    self.player.weapons["rocketlauncher"]["damage"] += 5
                    if debug == True:
                        for weapon_name, weapon_stats in self.player.weapons.items():
                            damage = weapon_stats["damage"]
                            print(f"{weapon_name}: {damage}")
            elif upgrade_key == "heal":
                self.player.health = min(self.player.max_health, self.player.health + upgrade["value"])
            elif upgrade_key == "regen":
                self.player.health_regen += upgrade["value"]
# Создание игровых объектов
player = Player()
monsters = []
monster_spawn_timer = 0
game_state = "start"  # start, playing, upgrade, game_over
wave_number = 1
monsters_per_wave = 10 * wave_number
# Основной игровой цикл
running = True
upgrade_wave = 1
while running:
    if upgrade_wave * 5 == wave_number:
        list_of_upgrades = [1,2,3]
        choise = random.choice(list_of_upgrades)
        if choise == 1:
            Monster_upgraded_damage += 10
        elif choise == 2:
            Monster_upgraded_max_health += 5
        elif choise == 3:
            Monster_upgraded_speed += 1
        upgrade_wave += 1

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка всех событий клавиатуры здесь
        if event.type == pygame.KEYDOWN: 
            if game_state == "game_over" and event.key == pygame.K_r:
                game_state = "upgrade"
                upgrade_screen = UpgradeScreen(player)
        
        # Обработка состояний игры
        if game_state == "upgrade":
            result = upgrade_screen.handle_input(event)
            if result == "start_game":
                game_state = "playing"
                player.health = player.max_health
                monsters = []
                wave_number += 1
                monster_spawn_timer = 0
    
    # Получение состояния клавиш
    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    
    # Обновление игры в зависимости от состояния
    if game_state == "start":
        screen.fill(BLACK)
        title = font.render("DemonWave", True, RED)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        
        hint = font.render("Press SPACE to start", True, GREEN)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 50))
        
        if keys[pygame.K_SPACE]:
            game_state = "playing"
            player = Player()
            monsters = []
            wave_number = 1
            monster_spawn_timer = 0
    
    elif game_state == "playing":
        # Обновление игрока
        player.move(keys)
        if mouse_buttons[0]:  # Левая кнопка мыши
            player.shoot(mouse_pos)
        player.update()
        player.time_alive += 1/60
        
        # Смена оружия
        if keys[pygame.K_1]:
            player.weapon = "pistol"
        elif keys[pygame.K_2] and player.time_alive > 25:
            player.weapon = "shotgun"
        elif keys[pygame.K_3] and player.time_alive > 50:
            player.weapon = "machinegun"
        elif keys[pygame.K_4] and player.time_alive > 75:
            player.weapon = "sniper rifle"
        elif keys[pygame.K_5] and player.time_alive > 100:
            player.weapon = "rocketlauncher"
        
        # Спавн монстров
        monster_spawn_timer += 1
        if monster_spawn_timer >= 60 and len(monsters) < monsters_per_wave * wave_number:
            side = random.choice(["top", "right", "bottom", "left"])
            if side == "top":
                x, y = random.randint(0, WIDTH), -50
            elif side == "right":
                x, y = WIDTH + 50, random.randint(0, HEIGHT)
            elif side == "bottom":
                x, y = random.randint(0, WIDTH), HEIGHT + 50
            else:
                x, y = -50, random.randint(0, HEIGHT)
            
            monster_type = random.choices(
                ["zombie", "imp", "cacodemon", "cyberdemon", "archvile", "hellknight"],
                weights=[0.5, 0.5, 0.17, 0.07, 0.07, 0.07]
            )[0]
            
            monsters.append(Monster(x, y, monster_type))
            monster_spawn_timer = 0
        
        # Обновление монстров
        for monster in monsters[:]:
            monster.move(player.x, player.y)
            
            # Проверка столкновения с игроком
            dist = math.sqrt((monster.x - player.x)**2 + (monster.y - player.y)**2)
            if dist < monster.radius + player.radius:
                player.health -= monster.damage / 10  # Меньший урон за кадр
                if player.health <= 0:
                    game_state = "game_over"
            
            # Проверка столкновения с пулями
            for bullet in player.bullets[:]:
                bullet_dist = math.sqrt((bullet["x"] - monster.x)**2 + (bullet["y"] - monster.y)**2)
                if bullet_dist < monster.radius:
                    monster.health -= bullet["damage"]
                    if bullet in player.bullets:
                        player.bullets.remove(bullet)
                    if monster.health <= 0:
                        player.score += monster.radius  # Большие монстры дают больше очков
                        monsters.remove(monster)
                        break
        
        # Отрисовка
        screen.fill(BLACK)
        
        # Отрисовка монстров
        for monster in monsters:
            monster.draw(screen)
        
        # Отрисовка игрока
        player.draw(screen)
        
        # Отрисовка волны
        wave_text = font.render(f"Wave: {wave_number}", True, WHITE)
        screen.blit(wave_text, (WIDTH - 150, 90))
        
        # Проверка завершения волны
        if len(monsters) == 0 and monster_spawn_timer > 120:
            game_state = "upgrade"
            upgrade_screen = UpgradeScreen(player)
    
    elif game_state == "upgrade":
        upgrade_screen.draw(screen)
    
    elif game_state == "game_over":
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        
        score_text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        
        time_text = font.render(f"Time Survived: {int(player.time_alive)} seconds", True, WHITE)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + 50))
        
        hint = font.render("Press R to upgrade and restart", True, GREEN)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 100))
    
    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)
RPC.close
pygame.quit()
sys.exit()