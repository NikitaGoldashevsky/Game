import pygame
import sys
import os
import time
import random

BGCOLOR = (120, 40, 30)
NETCOLOR = (80, 20, 10)

pygame.init()
user_screen = 1920, 1080
size = width, height = user_screen[0], user_screen[1]
screen = pygame.display.set_mode(size)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as level_map:
            return level_map.read()


def generate_level(level_map):
    level_map = level_map.split()
    board.cur_lvl_map = level_map
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '-':
                Ground((y, x), tiles)
            elif level_map[y][x] == 'W':
                Wall((y, x), tiles)
            elif board.cur_lvl_map[y][x] == 'S':
                Ground((y, x), tiles)
                Skeleton((y, x), characters)
            elif board.cur_lvl_map[y][x] == 'P':
                Ground((y, x), tiles)
                hero.pos = [x, 9 - y]
                hero.rect.x = width / 2 - cell_size * (board.width / 2) + cell_size * hero.pos[0]
                hero.rect.y = height / 2 + cell_size * (board.height / 2) - cell_size * (hero.pos[1] + 1)


def main_menu():
    title_text = "Ковбой против скелетов (не финальное название)"
    level_texts = ["1 УРОВЕНЬ", "2 УРОВЕНЬ", "3 УРОВЕНЬ"]
    level1_btn_pos = (140, 380)
    level1_btn_size = (300, 100)

    fon = pygame.transform.scale(load_image('bg 4 menu.jpg'), user_screen)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)

    # кнопка 1 уровня
    pygame.draw.rect(screen, (200, 30, 20), pygame.Rect(level1_btn_pos, level1_btn_size))
    pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(level1_btn_pos, level1_btn_size), 8)
    # её текст
    string_rendered = font.render(level_texts[0], True, pygame.Color('black'))
    screen.blit(string_rendered, (level1_btn_pos[0] + 30, level1_btn_pos[1] + 30))
    # название
    string_rendered = font.render(title_text, True, pygame.Color('white'))
    title_rect = 180, 200
    screen.blit(string_rendered, title_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] in range(level1_btn_pos[0], level1_btn_pos[0] + level1_btn_size[0]) \
                        and pygame.mouse.get_pos()[1] in range(level1_btn_pos[1],
                                                               level1_btn_pos[1] + level1_btn_size[1]):
                    board.cur_lvl_num = 1
                    return 'data/level 1.txt'
        pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.cur_lvl_num = 0
        self.cur_lvl_map = []

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width + 1):
            pygame.draw.line(screen, NETCOLOR, (i * self.cell_size + self.left, self.top),
                             (i * self.cell_size + self.left, self.top + self.cell_size * self.height), 7)
        for i in range(self.height + 1):
            pygame.draw.line(screen, NETCOLOR, (self.left, self.top + self.cell_size * i),
                             (self.left + self.cell_size * self.width, self.top + self.cell_size * i), 7)


class Hero(pygame.sprite.Sprite):
    image_st = load_image("hero wo bg.png")
    image_st = pygame.transform.scale(image_st, (98, 98))

    image_mv = load_image("hero moving wo bg.png")
    image_mv = pygame.transform.scale(image_mv, (86, 115))

    def __init__(self, pos, *group, direct=1):
        super().__init__(*group)
        self.pos = pos
        self.direct = direct
        self.moved = 0
        self.rect = self.image_st.get_rect()
        self.rect.x = width / 2 - cell_size * (board.width / 2) + cell_size * pos[0]
        self.rect.y = height / 2 + cell_size * (board.height / 2) - cell_size * (9 - pos[1])
        self.image = Hero.image_st
        self.animated = False
        self.last_anim = 'y'

    def move(self, ax, step):
        if time.monotonic() - self.moved < 0.4:
            return
        self.moved = time.monotonic()
        if ax == "x":
            if (self.pos[0] + step in range(0, board.width)) and (
                    board.cur_lvl_map[board.height - self.pos[1] - 1][self.pos[0] + step] in ('P', '-')):
                self.direct = step
                self.pos[0] += step
                self.animation(1, ax)

        else:
            if self.pos[1] + step in range(0, board.height) and (
                    board.cur_lvl_map[board.height - self.pos[1] - 1 - step][self.pos[0]] in ('P', '-')):
                self.direct = step
                self.pos[1] += step
                self.animation(1, ax)

    def animation(self, v, ax):
        if ax == 'x':
            self.last_anim = 'x'
            if v:
                self.rect.y -= 15
                self.image = Hero.image_mv
                self.animated = True
            else:
                self.rect.y += 15
                self.image = Hero.image_st
                self.animated = False
            self.rect.x += self.direct * cell_size // 2
            if self.direct == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.last_anim = 'y'
            if v:
                self.image = Hero.image_mv
                self.animated = True
            else:
                self.image = Hero.image_st
                self.animated = False
            self.rect.y -= cell_size // 2 * self.direct
            if self.direct == -1:
                self.image = pygame.transform.flip(self.image, True, False)


class Skeleton(pygame.sprite.Sprite):
    image = load_image("skeleton wo bg.png")

    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = Skeleton.image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = board.left + board.cell_size * pos[1]
        self.rect.y = board.top + board.cell_size * pos[0]
        self.image = pygame.transform.scale(self.image, (100, 100))

    def update(self):
        pass


class Wall(pygame.sprite.Sprite):
    image = load_image("wall.jpg")

    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = Wall.image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = board.left + board.cell_size * pos[1]
        self.rect.y = board.top + board.cell_size * pos[0]
        self.image = pygame.transform.scale(self.image, (100, 100))


class Ground(pygame.sprite.Sprite):

    def __init__(self, pos, *group):
        super().__init__(*group)
        if random.randint(0, 1):
            image = load_image("ground_tile2.jpg")
            image = pygame.transform.rotate(image, random.randint(0, 3) * 90)
        else:
            image = load_image("ground_tile2.jpg")
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = board.left + board.cell_size * pos[1]
        self.rect.y = board.top + board.cell_size * pos[0]
        self.image = pygame.transform.scale(self.image, (100, 100))


# SPRITES
tiles = pygame.sprite.Group()
characters = pygame.sprite.Group()

# BOARD
board = Board(10, 10)
cell_size = 100
board.set_view((user_screen[0] - board.width * cell_size) / 2, (user_screen[1] - board.height * cell_size) / 2,
               cell_size)

# HERO
hero = Hero((0, 0))
characters.add(hero)

# ЗАГРУЗКА УРОВНЯ
generate_level(load_level(main_menu()))

# MUSIC
pygame.mixer.music.load('data/track1.mp3')
pygame.mixer.music.set_volume(40)
pygame.mixer.music.play()

# TIMER
timer = time.monotonic()
beat = 0.5774
beat_add = 0.1

# BG
bg_image = load_image('bg 4 game1.jpg')
bg_image = pygame.transform.scale(bg_image, user_screen)

bg_image_lighter = load_image('bg 4 game2.jpg')
bg_image_lighter = pygame.transform.scale(bg_image_lighter, user_screen)

# GAME CYCLE
held = False
running = True
while running:
    if time.monotonic() > timer + beat:
        timer = time.monotonic()
        for sprite in characters:
            if str(sprite) == '<Skeleton Sprite(in 1 groups)>':
                sprite.update()
    elif time.monotonic() > timer + beat_add:
        screen.blit(bg_image, (0, 0))
    if time.monotonic() > timer + beat - beat_add:
        screen.blit(bg_image_lighter, (0, 0))

    if pygame.mixer.music.get_pos() % 81000 > 80000:
        pygame.mixer.music.rewind()
        timer = time.monotonic()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if not held and (time.monotonic() > timer + beat - beat_add * 2 or time.monotonic() - beat_add * 2 < timer):
                if keys[pygame.K_UP]:
                    hero.move('y', 1)
                    held = True
                elif keys[pygame.K_DOWN]:
                    hero.move('y', -1)
                    held = True
                elif keys[pygame.K_LEFT]:
                    hero.move('x', -1)
                    held = True
                elif keys[pygame.K_RIGHT]:
                    hero.move('x', 1)
                    held = True
        if event.type == pygame.KEYUP:
            held = False
    if time.monotonic() - hero.moved > 0.15:
        if hero.animated:
            hero.animation(0, hero.last_anim)
    board.render(screen)
    tiles.draw(screen)
    characters.draw(screen)
    pygame.display.flip()
