# Нормальное перемещение камеры(мышь)
# Движение по клеткам(волновой алгаритм, щелчки мыши)
# Прозрачные картинки
# Приближение камеры
# Изменение размеров тайлов, своя карта
import pygame
import sys
import os
from random import *
from pytmx import *
from PIL import Image
import copy

pygame.init()
tile_size = 20
FPS = 15
Speed = 100
Bsize = 100
size = width, height = 1200, 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adventure strategy")


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    im = pygame.image.load(fullname)
    im.set_colorkey((100, 100, 100))
    return im

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.imagename = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def checkselect(self, posx, posy):
        im = Image.open(f"data\\{self.imagename}")
        size = im.size
        return posx >= self.rect.x and posx <= self.rect.x + size[0] and posy >= self.rect.y and posy <= self.rect.y \
               + size[1]

class Build_button(Button):
    def __init__(self, x, y, image, *group):
        super().__init__(x, y, image, *group)
        self.build_menu = False

    def activate(self, group):
        if self.build_menu:
            for el in group:
                el.rect.y = 800
        else:
            for el in group:
                el.rect.y = 600
        self.build_menu = not self.build_menu

class Board:
    def __init__(self, width, height, size, top=0, left=0):
        self.width = Bsize * size
        self.height = Bsize * size
        self.board = [[0] * Bsize for _ in range(Bsize)]
        self.left = left
        self.top = top
        self.cell_size = size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def change_size(self, x):
        self.cell_size = x

    def render(self, screen):
        for i in range(len(self.board)):
            y = self.board[i]
            for j in range(len(y)):
                if y[j] == 0:
                    pygame.draw.rect(screen, 'white', (
                        (self.left + j * self.cell_size, self.top + i * self.cell_size),
                        (self.cell_size, self.cell_size)),
                                     1)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if x + 1 > self.width or y + 1 > self.height or x == -1 or y == -1:
            return None
        return (x, y)

    def get_coords(self, cell):
        x = cell[0] * self.cell_size + self.left + self.cell_size / 2
        y = cell[1] * self.cell_size + self.top + self.cell_size / 2
        return x, y

    def change_margin(self, top, left):
        self.top += top
        self.left += left

    def get_board(self):
        return copy.deepcopy(self.board)

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        global board, tile_size
        self.imagename = image
        self.image = load_image(self.imagename)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = board.get_coords((x, y))


    def update(self):
        pass



class Worker(pygame.sprite.Sprite):
    steps1 = [load_image(f"Animations\\Right_Walk\\{i}.png") for i in range(4)]
    steps2 = [load_image(f"Animations\\Left_Walk\\{i}.png") for i in range(4)]
    steps3 = [load_image(f"Animations\\Up_Walk\\{i}.png") for i in range(4)]
    steps4 = [load_image(f"Animations\\Down_Walk\\{i}.png") for i in range(4)]

    def __init__(self, x, y, *group):
        super().__init__(*group)
        global board, tile_size
        self.image = Worker.steps3[0]
        self.human_board = board
        self.imagename = f"Animations\\Up_Walk\\1.png"
        self.selected = False
        self.rotation = 'Up_Walk'
        self.can_go = False

        self.rect = self.image.get_rect()
        self.rect.x = board.get_coords((x, 0))[0] + tile_size * 0.5
#        self.rect.y = randrange(height - self.rect[3])
        self.rect.y = board.get_coords((0, y))[1] + tile_size * 0.5
        self.cell_posx = x
        self.cell_posy = y
        self.order_list = [1, 2, 3, 4]

    def update(self):
        global tile_size, xCam, yCam
        if self.can_go:
            if self.rotation == "Right_Walk":
                try:
                    self.steps1.index(self.image)
                except Exception:
                    self.image = Worker.steps1[0]
                if Speed // FPS + self.rect.x >= tile_size * self.cell_posx + tile_size // 2 + xCam:
                    self.rect.x = tile_size * self.cell_posx + tile_size // 2 + xCam
                    self.cell_posx += 1
                    self.direction()
                self.rect = self.rect.move(Speed // FPS, 0)
                self.image = self.steps1[(self.steps1.index(self.image) + 1) % 4]
                self.imagename = f"Animations\\Right_Walk\\{(self.steps1.index(self.image))}.png"
            elif self.rotation == "Left_Walk":
                try:
                    self.steps2.index(self.image)
                except Exception:
                    self.image = Worker.steps2[0]
                if Speed // FPS + self.rect.x <= tile_size * self.cell_posx - tile_size // 2 + xCam:
                    self.rect.x = tile_size * self.cell_posx - tile_size // 2 + xCam
                    self.cell_posx -= 1
                    self.direction()
                self.rect = self.rect.move(-Speed // FPS, 0)
                self.imagename = f"Animations\\Left_Walk\\{(self.steps2.index(self.image))}.png"
                self.image = self.steps2[(self.steps2.index(self.image) + 1) % 4]
            elif self.rotation == "Up_Walk":
                try:
                    self.steps3.index(self.image)
                except Exception:
                    self.image = Worker.steps3[0]
                if Speed // FPS + self.rect.y <= tile_size * self.cell_posy - tile_size // 2 + yCam:
                    self.rect.y = tile_size * self.cell_posy - tile_size // 2 + yCam
                    self.cell_posy -= 1
                    self.direction()
                self.rect = self.rect.move(0, -Speed // FPS)
                self.imagename = f"Animations\\Up_Walk\\{(self.steps3.index(self.image))}.png"
                self.image = self.steps3[(self.steps3.index(self.image) + 1) % 4]
            elif self.rotation == "Down_Walk":
                try:
                    self.steps4.index(self.image)
                except Exception:
                    self.image = Worker.steps4[0]
                if Speed // FPS + self.rect.y >= tile_size * self.cell_posy + tile_size // 2 + yCam:
                    self.rect.y = tile_size * self.cell_posy + tile_size // 2 + yCam
                    self.cell_posy += 1
                    self.direction()
                self.rect = self.rect.move(0, Speed // FPS)
                self.imagename = f"Animations\\Down_Walk\\{(self.steps4.index(self.image))}.png"
                self.image = self.steps4[(self.steps4.index(self.image) + 1) % 4]

    def delselect(self):
        self.selected = False

    def set_board(self, x, y): # 1 0
        global board
        self.a = 0
        x = board.get_cell((x, y))[0]
        y = board.get_cell((x, y))[1]
        self.human_board = board.get_board()
        wave_board = self.to_wave_board(x, y, self.human_board)
        self.human_board = wave_board
        print(x, y)

    def to_wave_board(self, x, y, lab):
        sp = [(x, y)]
        cur = 0
        while sp != []:
            cur += 1
            sp1 = []
            for el in sp:
                point = lab[el[1]][el[0]]
                if point == 0:
                    lab[el[1]][el[0]] = cur
                try:
                    if lab[el[1] + 1][el[0]] == 0:
                        sp1.append((el[0], el[1] + 1))
                except Exception:
                    pass
                try:
                    if el[1] - 1 > -1 and lab[el[1] - 1][el[0]] == 0:
                        sp1.append((el[0], el[1] - 1))
                except Exception:
                    pass
                try:
                    if lab[el[1]][el[0] + 1] == 0:
                        sp1.append((el[0] + 1, el[1]))
                except Exception:
                    pass
                try:
                    if el[0] - 1 > -1 and lab[el[1]][el[0] - 1] == 0:
                        sp1.append((el[0] - 1, el[1]))
                except Exception:
                    pass
            sp = list(set(sp1))
        return lab

    def checkselect(self, posx, posy):
        print(self.imagename)
        im = Image.open(f"data\\{self.imagename}")
        size = im.size
        return posx >= self.rect.x and posx <= self.rect.x + size[0] and posy >= self.rect.y and posy <= self.rect.y \
               + size[1]

    def select(self):
        self.selected = True

    def selected(self):
        return self.selected

    def set_rotation(self, x):
        self.rotation = x

    def can_go_true(self):
        self.can_go = True

    def direction(self):
        print(self.cell_posx, self.cell_posy)
        if self.human_board[self.cell_posy][self.cell_posx] == 1:
            self.can_go = False
        for el in self.order_list:
            if el == 1:
                try:
                    if self.human_board[self.cell_posy][self.cell_posx + 1] < self.human_board[self.cell_posy][self.cell_posx] and self.human_board[self.cell_posy][self.cell_posx + 1] > 0:
                        self.rotation = "Right_Walk"
                        self.order_list.remove(1)
                        self.order_list.append(1)
                        break
                except Exception:
                    pass
            if el == 2:
                try:
                    if self.human_board[self.cell_posy][self.cell_posx - 1] < self.human_board[self.cell_posy][self.cell_posx] and self.human_board[self.cell_posy][self.cell_posx - 1] > 0:
                        self.rotation = "Left_Walk"
                        self.order_list.remove(2)
                        self.order_list.append(2)
                        break
                except Exception:
                    pass
            if el == 3:
                try:
                    if self.human_board[self.cell_posy - 1][self.cell_posx] < self.human_board[self.cell_posy][self.cell_posx] and self.human_board[self.cell_posy - 1][self.cell_posx] > 0:
                        self.rotation = "Up_Walk"
                        self.order_list.remove(3)
                        self.order_list.append(3)
                        break
                except Exception:
                    pass
            if el == 4:
                try:
                    if self.human_board[self.cell_posy + 1][self.cell_posx] < self.human_board[self.cell_posy][self.cell_posx] and self.human_board[self.cell_posy + 1][self.cell_posx] > 0:
                        self.rotation = "Down_Walk"
                        self.order_list.remove(4)
                        self.order_list.append(4)
                        break
                except Exception:
                    pass



board = Board(width // tile_size, height // tile_size, tile_size)
xCam = 0
yCam = 0
kCam = 1

def main():
    global xCam, yCam, kCam
    map = load_pygame(f'maps/some1.tmx')
    all_sprites = pygame.sprite.Group()
    all_human_sprites = pygame.sprite.Group()
    all_building_sprites = pygame.sprite.Group()
    all_buttons = pygame.sprite.Group()
    build_board = pygame.sprite.Group()

    build_board_background = pygame.sprite.Sprite()
    build_board_background.image = load_image("build_board_background.png")
    build_board_background.rect = build_board_background.image.get_rect()
    build_board_background.rect.x, build_board_background.rect.y = 0, 800
    build_board.add(build_board_background)

    pygame.mixer.init()
    pygame.mixer.set_reserved(0)
    game_music = pygame.mixer.Sound("data\\DSG.mp3")  # !!!
    pygame.mixer.Channel(0).play(game_music, -1)

    Worker(1, 1, all_sprites)
    Worker(1, 2, all_sprites)
    Build_button(width - 100, height - 100, "build_button.png", all_buttons)
    clock = pygame.time.Clock()
    board_render = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if board_render:
                        board_render = False
                    else:
                        board_render = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in all_buttons:
                        if button.checkselect(event.pos[0], event.pos[1]):
                            button.activate(build_board)
                    for sprite in all_sprites:
                        if sprite.checkselect(event.pos[0], event.pos[1]):
                            sprite.select()
                            continue
                        sprite.delselect()
                if event.button == 3:
                    for sprite in all_sprites:
                        if sprite.selected:
                            print(board.get_cell((event.pos[0], event.pos[1])))
                            coords = board.get_cell((event.pos[0], event.pos[1]))
                            if board.get_board()[coords[1]][coords[1]] < 0:
                                break
                            sprite.set_board(event.pos[0], event.pos[1])
                            sprite.direction()
                            sprite.can_go_true()
            if pygame.key.get_pressed()[pygame.K_a]:
                xCam += 15
                for sprite in all_sprites:
                    sprite.rect.x += 15
                board.change_margin(0, 15)
            if pygame.key.get_pressed()[pygame.K_d]:
                xCam -= 15
                for sprite in all_sprites:
                    sprite.rect.x -= 15
                board.change_margin(0, -15)
            if pygame.key.get_pressed()[pygame.K_w]:
                yCam += 15
                for sprite in all_sprites:
                    sprite.rect.y += 15
                board.change_margin(15, 0)
            if pygame.key.get_pressed()[pygame.K_s]:
                yCam -= 15
                for sprite in all_sprites:
                    sprite.rect.y -= 15
                board.change_margin(-15, 0)
        screen.fill((255, 255, 255))
        for x in range(100):
            for y in range(100):
                image = map.get_tile_image(x, y, 0)
                screen.blit(image, (int(tile_size * kCam * x + xCam), int(tile_size * kCam * y + yCam)))
        if board_render:
            board.render(screen)
        all_sprites.draw(screen)
        build_board.draw(screen)
        all_buttons.draw(screen)
        all_sprites.update()

        clock.tick(FPS)  # переделать смену кадров по таймеру
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
