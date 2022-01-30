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
from functools import lru_cache # крутая функия, пригодится при подсчете путя
import copy

pygame.init()
tile_size = 20
FPS = 15
Speed = 100
size = width, height = 400, 400

screen = pygame.display.set_mode((width + 30, height + 30))
pygame.display.set_caption("Adventure strategy")


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    im = pygame.image.load(fullname)
    im.set_colorkey((0, 0, 0))
    return im


class Board:
    def __init__(self, width, height, size, top=0, left=0):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
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
        x = cell[0] * self.cell_size + self.left
        y = cell[1] * self.cell_size + self.top
        return x, y

    def change_margin(self, top, left):
        self.top += top
        self.left += left

    def get_board(self):
        return copy.deepcopy(self.board)



class Worker(pygame.sprite.Sprite):
    steps = {"Right_Walk": [load_image(f"Animations\\Right_Walk\\{i}.png") for i in range(4)],
             "Left_Walk": [load_image(f"Animations\\Left_Walk\\{i}.png") for i in range(4)],
             "Up_Walk": [load_image(f"Animations\\Up_Walk\\{i}.png") for i in range(4)],
             "Down_Walk": [load_image(f"Animations\\Down_Walk\\{i}.png") for i in range(4)]}
    steps1 = [load_image(f"Animations\\Right_Walk\\{i}.png") for i in range(4)]
    steps2 = [load_image(f"Animations\\Left_Walk\\{i}.png") for i in range(4)]
    steps3 = [load_image(f"Animations\\Up_Walk\\{i}.png") for i in range(4)]
    steps4 = [load_image(f"Animations\\Down_Walk\\{i}.png") for i in range(4)]

    def __init__(self, x, y, *group):
        super().__init__(*group)
        global board
        self.image = Worker.steps3[0]
        self.human_board = board
        self.imagename = f"Animations\\Up_Walk\\1.png"
        self.selected = False
        self.rotation = 'Up_Walk'
        self.can_go = False

        self.rect = self.image.get_rect()
        #self.rect.x, self.rect.y = board.get_coords((x, y))
        ###########################################
        self.rect.x, self.rect.y = board.get_coords((x, y))
        self.rect.x += self.set_centre(self.rect[2], tile_size)
        self.rect.y += self.set_centre(self.rect[3], tile_size)
        #############################################
        self.cell_posx = x
        self.cell_posy = y
        self.order_list = [1, 2, 3, 4]

        self.index = 0
        self.ost = 0
    ################################
    def set_centre(self, size, cell_size):
        if cell_size >= size:
            return (cell_size - size) // 2
        return -((size - cell_size) + 2)
    ################################

    def move_func(self, move):
        if self.rotation == "Right_Walk":
            self.rect = self.rect.move((move, 0))
        elif self.rotation == "Left_Walk":
            self.rect = self.rect.move((-move, 0))
        elif self.rotation == "Up_Walk":
            self.rect = self.rect.move((0, -move))
        elif self.rotation == "Down_Walk":
            self.rect = self.rect.move((0, move))

    def update(self):
        if self.can_go:
            if self.index == 4:
                self.move_func(self.ost)
                self.direction()
                self.ost = tile_size
                self.index = 1
                self.image = Worker.steps[self.rotation][0]
                # так и должно быть))
            else:
                move = self.ost // (4 - (self.index - 1))  # более точный расчёт, чтобы точно проходил размер тайла
                self.move_func(move)
                self.ost -= move
                self.image = Worker.steps[self.rotation][self.index]
                self.index += 1

    def delselect(self):
        self.selected = False

    def set_board(self, x, y): # 1 0
        global board
        x = board.get_cell((x, y))[0]
        y = board.get_cell((x, y))[1]
        self.human_board = board.get_board()
        self.human_board = self.to_wave_board(y, x, self.human_board)

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

    def checkselect(self, x, y):
        return self.rect[2] + self.rect[0] >= x >= self.rect[0] and self.rect[3] + self.rect[1] >= y >= self.rect[1]

    def select(self):
        self.selected = True

    def selected(self):
        return self.selected

    def set_rotation(self, x):
        self.rotation = x

    def can_go_true(self):
        self.index = 4
        self.can_go = True

    def direction(self):
        for el in self.human_board:
            print(el)
        print()
        if self.human_board[self.cell_posy][self.cell_posx] == 1:
            self.can_go = False
        else:
            for i, j, rot in ((0, 1, "Right_Walk"), (0, -1, "Left_Walk"), (1, 0, "Down_Walk"), (-1, 0, "Up_Walk")):
                if self.human_board[self.cell_posy + i][self.cell_posx + j] < self.human_board[self.cell_posy][
                    self.cell_posx]:
                    self.rotation = rot
                    self.cell_posy += i
                    self.cell_posx += j
                    print(self.human_board[self.cell_posy + i][self.cell_posx + j])
                    break
        '''if self.human_board[self.cell_posy][self.cell_posx] == 1:
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
                    pass'''



board = Board(width // tile_size, height // tile_size, tile_size)

def main():
    map = load_pygame(f'maps/some.tmx')
    all_sprites = pygame.sprite.Group()
    Worker(3, 5, all_sprites)
    clock = pygame.time.Clock()
    xCam = 0
    yCam = 0
    kCam = 1
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
                    for sprite in all_sprites:
                        if sprite.checkselect(event.pos[0], event.pos[1]):
                            sprite.select()
                            continue
                        sprite.delselect()
                if event.button == 3:
                    for sprite in all_sprites:
                        if sprite.selected:
                            coords = board.get_cell((event.pos[0], event.pos[1]))
                            if board.get_board()[coords[1]][coords[1]] < 0:
                                break
                            sprite.set_board(event.pos[1], event.pos[0])
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
        for x in range(width // tile_size):
            for y in range(height // tile_size):
                image = map.get_tile_image(x, y, 0)
                screen.blit(image, (int(tile_size * kCam * x + xCam), int(tile_size * kCam * y + yCam)))
        if board_render:
            board.render(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(FPS)  # переделать смену кадров по таймеру
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
