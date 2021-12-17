import pygame
import sys
import os
import time

BGCOLOR = (120, 40, 30)
NETCOLOR = (80, 20, 10)

pygame.init()
user_screen = 1920, 1080
size = width, height = user_screen[0], user_screen[1]
screen = pygame.display.set_mode(size)

# 0 - nothing
# 1 - wall
# 2 - skeleton
current_level = 1
level1 = [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
          [0, 0, 0, 2, 0, 1, 0, 0, 2, 0],
          [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
          [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 0, 0, 2, 0, 0],
          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]


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


class Hero:
    def __init__(self, pos, direct=1):
        self.pos = pos
        self.direct = direct

    def move(self, ax, step):
        if ax == "x":
            if (self.pos[0] + step in range(0, board.width)) and (
                    level1[board.height - self.pos[1] - 1][self.pos[0] + step] not in (1, 2)):
                if self.direct != step:
                    self.direct = step
                    hero_sprite.image = pygame.transform.flip(hero_sprite.image, True, False)
                self.pos[0] += step
                hero_sprite.rect = hero_sprite.rect.move(step * cell_size, 0)

        else:
            if self.pos[1] + step in range(0, board.height) and (
                    level1[board.height - self.pos[1] - 1 - step][self.pos[0]] not in (1, 2)):
                self.pos[1] += step
                hero_sprite.rect = hero_sprite.rect.move(0, - step * cell_size)


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

    def move(self):
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


# BOARD
board = Board(10, 10)
cell_size = 100
board.set_view((user_screen[0] - board.width * cell_size) / 2, (user_screen[1] - board.height * cell_size) / 2,
               cell_size)

# SPRITES
all_sprites = pygame.sprite.Group()
hero_sprite = pygame.sprite.Sprite()
hero_sprite.image = load_image("hero wo bg.png")
hero_sprite.image = pygame.transform.scale(hero_sprite.image, (98, 95))
hero_sprite.rect = hero_sprite.image.get_rect()
all_sprites.add(hero_sprite)
hero_sprite.rect.x = width / 2 - cell_size * (board.width / 2)
hero_sprite.rect.y = height / 2 + cell_size * (board.height / 2 - 1)

# HERO
hero = Hero([0, 0])

# WALLS
for x in range(board.width):
    for y in range(board.height):
        if current_level == 1 and level1[x][y] == 1:
            Wall((x, y), all_sprites)

# SKELETONS
for x in range(board.width):
    for y in range(board.height):
        if current_level == 1 and level1[x][y] == 2:
            Skeleton((x, y), all_sprites)

# MUSIC
pygame.mixer.music.load('data/track1.mp3')
pygame.mixer.music.play()

# TIMER
timer = time.monotonic()
beat = 0.5774
beat_add = 0.1

# GAME CYCLE
held = False
running = True
while running:
    screen.fill(BGCOLOR)
    if time.monotonic() > timer + beat:
        timer = time.monotonic()
    elif time.monotonic() > timer + beat_add:
        BGCOLOR = 120, BGCOLOR[1], BGCOLOR[2]
    if time.monotonic() > timer + beat - beat_add:
        BGCOLOR = 160, BGCOLOR[1], BGCOLOR[2]

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
    board.render(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
