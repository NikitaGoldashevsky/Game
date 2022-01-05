import pygame
import sys
import os
import time
import random

BGCOLOR = (120, 40, 30)
NETCOLOR = (40, 10, 5)

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
    map_len_y = int(level_map.split()[0])
    level_map = level_map.split()[1:]
    board.cur_lvl_map = level_map
    for i in range(map_len_y):
        level_map[i] = list(level_map[i])
    board.cur_lvl_map = level_map[:map_len_y]
    cur_path = 0
    for y in range(map_len_y):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '-':
                Ground((y, x), tiles)
            elif level_map[y][x] == 'W':
                Wall((y, x), tiles)
            elif board.cur_lvl_map[y][x] == 'S':
                Ground((y, x), tiles)
                Skeleton((x, 9 - y), level_map[map_len_y + cur_path], characters)
                cur_path += 1
            elif board.cur_lvl_map[y][x] == 'T':
                Trap((y, x), traps)
            elif board.cur_lvl_map[y][x] == 'F':
                Ground((y, x), tiles)
                Fireball((y, x), traps)
            elif board.cur_lvl_map[y][x] == 'P':
                Ground((y, x), tiles)
                hero.pos = [x, 9 - y]
                hero.rect.x = width / 2 - cell_size * (board.width / 2) + cell_size * hero.pos[0]
                hero.rect.y = height / 2 + cell_size * (board.height / 2) - cell_size * (hero.pos[1] + 1)
                board.cur_lvl_map[y][x] = '-'


def main_menu():
    title_text = "Название"
    level_texts = ["1 УРОВЕНЬ", "2 УРОВЕНЬ", "3 УРОВЕНЬ"]
    level1_btn_pos = (160, 380)
    level1_btn_size = (300, 100)

    fon = pygame.transform.scale(load_image('bg 4 menu.jpg'), user_screen)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)

    # кнопка 1 уровня
    pygame.draw.rect(screen, (200, 30, 20), pygame.Rect(level1_btn_pos, level1_btn_size))
    pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(level1_btn_pos, level1_btn_size), 8)
    # её текст
    button_rendered = font.render(level_texts[0], True, pygame.Color('black'))

    # название
    title_rendered = font.render(title_text, True, pygame.Color('white'))
    title_rect = 180, 200
    screen.blit(title_rendered, title_rect)

    pygame.mixer.music.load('data/menu music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    click_sound = pygame.mixer.Sound('data/click.mp3')
    click_sound.set_volume(0.6)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif pygame.mouse.get_pos()[0] in range(level1_btn_pos[0], level1_btn_pos[0] + level1_btn_size[0]) and \
                    pygame.mouse.get_pos()[1] in range(level1_btn_pos[1], level1_btn_pos[1] + level1_btn_size[1]):
                pygame.draw.rect(screen, (180, 30, 20), pygame.Rect(level1_btn_pos, level1_btn_size))
                pygame.draw.rect(screen, (15, 0, 0), pygame.Rect(level1_btn_pos, level1_btn_size), 8)
                screen.blit(button_rendered, (level1_btn_pos[0] + 30, level1_btn_pos[1] + 30))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    board.cur_lvl_num = 1
                    return 'data/level 1.txt'
            else:
                pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(level1_btn_pos, level1_btn_size))
                pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(level1_btn_pos, level1_btn_size), 8)
                screen.blit(button_rendered, (level1_btn_pos[0] + 30, level1_btn_pos[1] + 30))
        pygame.display.flip()


def beginning(level=0):
    global board, tiles, characters, cell_size, hero, traps

    # SPRITES
    tiles = pygame.sprite.Group()
    characters = pygame.sprite.Group()
    traps = pygame.sprite.Group()

    # BOARD
    board = Board(10, 10)
    cell_size = 100
    board.set_view((user_screen[0] - board.width * cell_size) / 2, (user_screen[1] - board.height * cell_size) / 2,
                   cell_size)

    # HERO
    hero = Hero((0, 0))
    characters.add(hero)

    # ЗАГРУЗКА УРОВНЯ
    if not level:
        generate_level(load_level(main_menu()))
    else:
        generate_level(load_level(f'data/level {level}.txt'))
        board.cur_lvl_num = level
    start_level()


def start_level():
    # MUSIC
    pygame.mixer.music.load('data/track1.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()
    fail_sound = pygame.mixer.Sound('data/fail.mp3')

    # TIMER
    timer = time.monotonic()
    beat = 0.576
    beat_add = 0.1

    # BG
    bg_image = load_image('bg 4 game1.jpg')
    bg_image = pygame.transform.scale(bg_image, user_screen)

    bg_image_lighter = load_image('bg 4 game2.jpg')
    bg_image_lighter = pygame.transform.scale(bg_image_lighter, user_screen)

    # game cycle
    hero_moved = False
    next_move = True
    held = False
    running = True
    screen.blit(bg_image, (0, 0))
    while running:
        if time.monotonic() > timer + beat:
            timer = time.monotonic()
            for sk in board.skeletons:
                sk.update()
            traps.update()
        elif time.monotonic() > timer + beat_add:
            screen.blit(bg_image, (0, 0))
        if time.monotonic() > timer + beat - beat_add:
            screen.blit(bg_image_lighter, (0, 0))
        if time.monotonic() - timer > beat_add * 1.5 and time.monotonic() - timer < beat / 2:
            next_move = True
        if time.monotonic() - timer > beat - beat_add * 1.5 and next_move:
            hero_moved = False
            next_move = False
        if pygame.mixer.music.get_pos() % 81000 > 80000:
            pygame.mixer.music.rewind()
            timer = time.monotonic()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE]:
                    dif = time.monotonic() - timer
                    screen.blit(bg_image, (0, 0))
                    pause()
                    timer = time.monotonic() - dif
                if not held and (
                        time.monotonic() - timer < beat_add * 1.5 or time.monotonic() - timer > beat - beat_add * 1.5) \
                        and not hero_moved:
                    hero_moved = True
                    if keys[pygame.K_UP] or keys[pygame.K_w]:
                        hero.move('y', 1)
                        held = True
                    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        hero.move('y', -1)
                        held = True
                    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        hero.move('x', -1)
                        held = True
                    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        hero.move('x', 1)
                        held = True
            if event.type == pygame.KEYUP:
                held = False
        if time.monotonic() - hero.moved > 0.15:
            if hero.animated:
                hero.animation(0, hero.last_anim)
        if time.monotonic() - timer > 0.1:
            for sk in board.skeletons:
                if sk.animated:
                    sk.animation(0, sk.last_anim)
        if time.monotonic() - timer > beat / 2:
            for fb in board.fireballs:
                if not fb.moved:
                    fb.move()
        if hero.death():
            pygame.mixer.music.stop()
            fail_sound.play()

            hero.image = load_image('grave.png')
            hero.image = pygame.transform.scale(hero.image, (100, 100))

            board.render(screen)
            tiles.draw(screen)
            traps.draw(screen)
            characters.draw(screen)
            pygame.display.flip()

            time.sleep(1.2)
            end_screen()
        board.render(screen)
        tiles.draw(screen)
        traps.draw(screen)
        characters.draw(screen)
        pygame.display.flip()


def pause():
    pygame.mixer.music.pause()
    text_top = "Пауза"
    retry_text = "Начать заново"
    retry_btn_pos = (user_screen[0] // 3, user_screen[1] // 2)
    retry_btn_size = retry_btn_pos[0] - 30, user_screen[1] // 6 - 40
    return_text = 'Главное меню'
    return_btn_pos = (user_screen[0] // 3, user_screen[1] * 2 // 3)
    return_btn_size = return_btn_pos[0] - 30, user_screen[1] // 6 - 40
    cont_text = 'Продолжить'
    cont_btn_pos = (user_screen[0] // 3, user_screen[1] // 3)
    cont_btn_size = cont_btn_pos[0] - 30, user_screen[1] // 6 - 40
    font = pygame.font.Font(None, 60)

    text_top_rendered = font.render(text_top, True, pygame.Color('black'))
    retry_text_rendered = font.render(retry_text, True, pygame.Color('black'))
    return_text_rendered = font.render(return_text, True, pygame.Color('black'))
    cont_text_rendered = font.render(cont_text, True, pygame.Color('black'))
    text_top_rect = (user_screen[0] - text_top_rendered.get_rect()[2]) // 2, user_screen[1] // 6 + 40

    pygame.draw.rect(screen, (100, 30, 20),
                     pygame.Rect(user_screen[0] // 3 - 30, user_screen[1] // 6 - 30, user_screen[0] // 3 + 30,
                                 user_screen[1] * 2 // 3 + 30))
    pygame.draw.rect(screen, (30, 30, 20),
                     pygame.Rect(user_screen[0] // 3 - 30, user_screen[1] // 6 - 30, user_screen[0] // 3 + 30,
                                 user_screen[1] * 2 // 3 + 30), 9)

    pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(retry_btn_pos, retry_btn_size))
    pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(retry_btn_pos, retry_btn_size), 8)

    pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(return_btn_pos, return_btn_size))
    pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(return_btn_pos, return_btn_size), 8)

    pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(cont_btn_pos, cont_btn_size))
    pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(cont_btn_pos, cont_btn_size), 8)

    screen.blit(retry_text_rendered, (retry_btn_pos[0] + 20, retry_btn_pos[1] + 50))
    screen.blit(return_text_rendered, (return_btn_pos[0] + 20, return_btn_pos[1] + 50))
    screen.blit(cont_text_rendered, (cont_btn_pos[0] + 20, cont_btn_pos[1] + 50))
    screen.blit(text_top_rendered, text_top_rect)

    click_sound = pygame.mixer.Sound('data/click.mp3')
    click_sound.set_volume(0.6)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif pygame.mouse.get_pos()[0] in range(retry_btn_pos[0], retry_btn_pos[0] + retry_btn_size[0]) and \
                    pygame.mouse.get_pos()[1] in range(retry_btn_pos[1], retry_btn_pos[1] + retry_btn_size[1]):
                pygame.draw.rect(screen, (180, 30, 20), pygame.Rect(retry_btn_pos, retry_btn_size))
                pygame.draw.rect(screen, (15, 0, 0), pygame.Rect(retry_btn_pos, retry_btn_size), 8)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    beginning(board.cur_lvl_num)
            else:
                pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(retry_btn_pos, retry_btn_size))
                pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(retry_btn_pos, retry_btn_size), 8)
            screen.blit(retry_text_rendered, (retry_btn_pos[0] + 20, retry_btn_pos[1] + 50))
            # --------------
            if pygame.mouse.get_pos()[0] in range(return_btn_pos[0], return_btn_pos[0] + return_btn_size[0]) and \
                    pygame.mouse.get_pos()[1] in range(return_btn_pos[1], return_btn_pos[1] + return_btn_size[1]):
                pygame.draw.rect(screen, (180, 30, 20), pygame.Rect(return_btn_pos, return_btn_size))
                pygame.draw.rect(screen, (15, 0, 0), pygame.Rect(return_btn_pos, return_btn_size), 8)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    beginning()
            else:
                pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(return_btn_pos, return_btn_size))
                pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(return_btn_pos, return_btn_size), 8)
            screen.blit(return_text_rendered, (return_btn_pos[0] + 20, return_btn_pos[1] + 50))
            # --------------
            if pygame.mouse.get_pos()[0] in range(cont_btn_pos[0], cont_btn_pos[0] + cont_btn_size[0]) and \
                    pygame.mouse.get_pos()[1] in range(cont_btn_pos[1], cont_btn_pos[1] + cont_btn_size[1]):
                pygame.draw.rect(screen, (180, 30, 20), pygame.Rect(cont_btn_pos, cont_btn_size))
                pygame.draw.rect(screen, (15, 0, 0), pygame.Rect(cont_btn_pos, cont_btn_size), 8)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    pygame.mixer.music.unpause()
                    return
            else:
                pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(cont_btn_pos, cont_btn_size))
                pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(cont_btn_pos, cont_btn_size), 8)
            screen.blit(cont_text_rendered, (cont_btn_pos[0] + 20, cont_btn_pos[1] + 50))
        pygame.display.flip()


def end_screen():
    text_top = "Вы проиграли!"
    advice = random.choice(('Двигайтесь в одном ритме с музыкой', 'Избегайте столкновений с врагами',
                            'Переходите через шипы тогда, когда они скрыты', 'Старайтесь не касаться огненных шаров'))
    retry_text = "Начать заново"
    retry_btn_pos = (520, 640)
    retry_btn_size = (340, 150)
    return_text = 'Главное меню'
    return_btn_pos = (1060, 640)
    return_btn_size = (340, 150)

    fon = pygame.transform.scale(load_image('bg 4 game1.jpg'), user_screen)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    adv_font = pygame.font.Font(None, 52)
    click_sound = pygame.mixer.Sound('data/click.mp3')
    click_sound.set_volume(0.6)

    advice_rendered = adv_font.render(advice, True, pygame.Color('black'))
    text_top_rendered = font.render(text_top, True, pygame.Color('black'))
    text_top_rect = (user_screen[0] - text_top_rendered.get_rect()[2]) // 2, user_screen[1] // 4 + 110
    advice_rect = (user_screen[0] - advice_rendered.get_rect()[2]) // 2, text_top_rect[1] + 110
    retry_text_rendered = font.render(retry_text, True, pygame.Color('black'))
    return_text_rendered = font.render(return_text, True, pygame.Color('black'))
    screen.blit(text_top_rendered, text_top_rect)

    pygame.draw.rect(screen, (100, 30, 20),
                     pygame.Rect(user_screen[0] // 4, user_screen[1] // 4, user_screen[0] // 2,
                                 user_screen[1] // 2))
    pygame.draw.rect(screen, (30, 30, 20),
                     pygame.Rect(user_screen[0] // 4, user_screen[1] // 4, user_screen[0] // 2,
                                 user_screen[1] // 2), 10)
    pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(retry_btn_pos, retry_btn_size))
    pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(retry_btn_pos, retry_btn_size), 8)

    pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(return_btn_pos, return_btn_size))
    pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(return_btn_pos, return_btn_size), 8)

    screen.blit(retry_text_rendered, (retry_btn_pos[0] + 20, retry_btn_pos[1] + 50))
    screen.blit(return_text_rendered, (return_btn_pos[0] + 20, return_btn_pos[1] + 50))
    screen.blit(text_top_rendered, text_top_rect)
    screen.blit(advice_rendered, advice_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif pygame.mouse.get_pos()[0] in range(retry_btn_pos[0], retry_btn_pos[0] + retry_btn_size[0]) and \
                    pygame.mouse.get_pos()[1] in range(retry_btn_pos[1], retry_btn_pos[1] + retry_btn_size[1]):
                pygame.draw.rect(screen, (180, 30, 20), pygame.Rect(retry_btn_pos, retry_btn_size))
                pygame.draw.rect(screen, (15, 0, 0), pygame.Rect(retry_btn_pos, retry_btn_size), 8)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    beginning(board.cur_lvl_num)
            else:
                pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(retry_btn_pos, retry_btn_size))
                pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(retry_btn_pos, retry_btn_size), 8)
            screen.blit(retry_text_rendered, (retry_btn_pos[0] + 20, retry_btn_pos[1] + 50))
            # --------------
            if pygame.mouse.get_pos()[0] in range(return_btn_pos[0], return_btn_pos[0] + return_btn_size[0]) and \
                    pygame.mouse.get_pos()[1] in range(return_btn_pos[1], return_btn_pos[1] + return_btn_size[1]):
                pygame.draw.rect(screen, (180, 30, 20), pygame.Rect(return_btn_pos, return_btn_size))
                pygame.draw.rect(screen, (15, 0, 0), pygame.Rect(return_btn_pos, return_btn_size), 8)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    beginning()
            else:
                pygame.draw.rect(screen, (160, 20, 10), pygame.Rect(return_btn_pos, return_btn_size))
                pygame.draw.rect(screen, (20, 0, 0), pygame.Rect(return_btn_pos, return_btn_size), 8)
            screen.blit(return_text_rendered, (return_btn_pos[0] + 20, return_btn_pos[1] + 50))
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
        self.skeletons = []
        self.traps = []
        self.fireballs = []

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in (0, self.width):
            pygame.draw.line(screen, NETCOLOR, (i * self.cell_size + self.left, self.top),
                             (i * self.cell_size + self.left, self.top + self.cell_size * self.height), 14)
        for i in (0, self.height):
            pygame.draw.line(screen, NETCOLOR, (self.left, self.top + self.cell_size * i),
                             (self.left + self.cell_size * self.width, self.top + self.cell_size * i), 14)


class Hero(pygame.sprite.Sprite):
    image_st = load_image("hero wo bg.png")
    image_st = pygame.transform.scale(image_st, (98, 98))

    image_mv = load_image("hero moving wo bg.png")
    image_mv = pygame.transform.scale(image_mv, (86, 115))

    def __init__(self, pos, *group, direct=1):
        super().__init__(*group)
        self.pos = pos
        self.direct = direct
        self.rect = self.image_st.get_rect()
        self.rect.x = width / 2 - cell_size * (board.width / 2) + cell_size * pos[0]
        self.rect.y = height / 2 + cell_size * (board.height / 2) - cell_size * (9 - pos[1])
        self.moved = 0.0
        self.image = Hero.image_st
        self.animated = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, ax, step):
        last_pos = self.pos[0], self.pos[1]
        self.moved = time.monotonic()
        if ax == "x":
            if (self.pos[0] + step in range(0, board.width)) and (
                    board.cur_lvl_map[board.height - self.pos[1] - 1][self.pos[0] + step] in ('-', 'T', 'F')):
                self.direct = step
                self.pos[0] += step
                self.animation(1, ax)
            else:
                return
        else:
            if self.pos[1] + step in range(0, board.height) and (
                    board.cur_lvl_map[board.height - self.pos[1] - 1 - step][self.pos[0]] in ('-', 'T', 'F')):
                self.direct = step
                self.pos[1] += step
                self.animation(1, ax)
            else:
                return

    def animation(self, v, ax):
        if ax == 'x':
            self.last_anim = 'x'
            if v:
                self.rect.y -= 25
                self.image = Hero.image_mv
                self.animated = True
            else:
                self.rect.y += 25
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

    def death(self):
        if board.cur_lvl_map[9 - self.pos[1]][self.pos[0]] == "S":
            return True
        if board.cur_lvl_map[9 - self.pos[1]][self.pos[0]] == "T":
            if board.traps[0].state == 3:
                return True
        for elem in board.fireballs:
            if pygame.sprite.collide_mask(self, elem) and 9 - elem.pos[0] == self.pos[1]:
                print(elem.pos, self.pos)
                print(elem.pos[0], self.pos[1])
                return True
        return False


class Skeleton(pygame.sprite.Sprite):

    def __init__(self, pos, path, *group):
        super().__init__(*group)
        self.image_st = load_image("skeleton wo bg.png")
        self.image_mv = load_image("skeleton moving wo bg.png")
        self.image_mv = pygame.transform.scale(self.image_mv, (84, 90))
        self.image = self.image_st
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.y = board.top + board.cell_size * (9 - pos[1])
        self.rect.x = board.left + board.cell_size * pos[0]
        self.direct = 1
        self.path = path
        self.path_len = len(path)
        board.skeletons.append(self)
        self.animated = False

    def update(self):
        self.path = self.path[1:] + self.path[0]
        self.move(self.path[0])

    def move(self, dir):
        board.cur_lvl_map[9 - self.pos[1]][self.pos[0]] = '-'
        if self.direct == 1 and dir == 'l' or self.direct == -1 and dir == 'r' or self.direct == 1 and dir == 'd' \
                or self.direct == -1 and dir == 'u':
            self.direct *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        if dir == 'u':
            self.pos = self.pos[0], self.pos[1] + 1
            self.animation(1, 'y')
        elif dir == 'd':
            self.pos = self.pos[0], self.pos[1] - 1
            self.animation(1, 'y')
        elif dir == 'r':
            self.pos = self.pos[0] + 1, self.pos[1]
            self.animation(1, 'x')
        elif dir == 'l':
            self.pos = self.pos[0] - 1, self.pos[1]
            self.animation(1, 'x')

    def animation(self, v, ax):
        if ax == 'x':
            self.last_anim = 'x'
            if v:
                self.rect.y -= 14
                self.image = self.image_mv
                self.animated = True
            else:
                self.rect.y += 14
                self.image = self.image_st
                self.animated = False
                board.cur_lvl_map[9 - self.pos[1]][self.pos[0]] = 'S'
            self.rect.x += self.direct * cell_size // 2
            if self.direct == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.last_anim = 'y'
            if v:
                self.image = self.image_mv
                self.animated = True
            else:
                self.image = self.image_st
                self.animated = False
                board.cur_lvl_map[9 - self.pos[1]][self.pos[0]] = 'S'
            self.rect.y -= cell_size // 2 * self.direct
            if self.direct == -1:
                self.image = pygame.transform.flip(self.image, True, False)


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


class Trap(pygame.sprite.Sprite):

    def __init__(self, pos, *group, state=0):
        super().__init__(*group)
        self.image_st = load_image("trap.png")
        self.image_st = pygame.transform.scale(self.image_st, (100, 100))
        self.image_act = load_image("trap_act.png")
        self.image_act = pygame.transform.scale(self.image_act, (100, 100))
        self.image = self.image_st
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = board.left + board.cell_size * pos[1]
        self.rect.y = board.top + board.cell_size * pos[0]
        self.state = state
        board.traps.append(self)

    def update(self):
        self.state = (self.state + 1) % 4
        if self.state == 3:
            self.image = self.image_act
        else:
            self.image = self.image_st


class Fireball(pygame.sprite.Sprite):

    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = load_image("fireball.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image = pygame.transform.flip(self.image, True, False)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x = board.left + board.cell_size * pos[1]
        self.rect.y = board.top + board.cell_size * pos[0]
        self.direct = 1
        self.moved = True
        self.mask = pygame.mask.from_surface(self.image)
        board.fireballs.append(self)

    def update(self):
        if self.pos[1] + self.direct not in range(board.width):
            self.direct *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        self.pos = self.pos[0], self.pos[1] + self.direct
        self.rect.x += board.cell_size * self.direct // 2
        self.moved = False

    def move(self):
        self.rect.x += board.cell_size * self.direct // 2
        self.moved = True


# Начало
beginning()
