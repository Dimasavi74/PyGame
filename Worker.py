import change as change
import pygame
import sys
import os
from random import *
from PIL import Image

FPS = 15
Speed = 100
size = width, height = 450, 450
tile_size = 30


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    return pygame.image.load(fullname)


class Worker(pygame.sprite.Sprite):
    steps = {"Right_Walk": [load_image(f"Animations\\Right_Walk\\{i}.png") for i in range(4)],
             "Left_Walk": [load_image(f"Animations\\Left_Walk\\{i}.png") for i in range(4)],
             "Up_Walk": [load_image(f"Animations\\Up_Walk\\{i}.png") for i in range(4)],
             "Down_Walk": [load_image(f"Animations\\Down_Walk\\{i}.png") for i in range(4)]}

    def __init__(self, board, *group):
        super().__init__(*group)
        self.index = 0
        self.rotation = "Down_Walk"
        self.image = self.steps["Down_Walk"][self.index]
        self.imagename = f"Animations\\Right_Walk\\0.png"
        self.rol = [(1, 0, "Up_Walk"), (-1, 0, "Down_Walk"), (0, 1, "Right_Walk"), (0, -1, "Left_Walk")]

        self.rect = self.image.get_rect()
        self.human_board = board
        self.selected = True # выбран по умолчанию
        self.can_go = False
        self.rect.x, self.rect.y = board.get_coords((1, 1))
        self.cell_posx, self.cell_posy = board.get_cell((self.rect.x, 0))

    def update(self):
        global tile_size
        # обнулять индекс при изменении направления
        if self.can_go:
            if self.rotation == "Right_Walk":
                if self.rect.x >= tile_size * self.cell_posx:
                    self.rect.x = tile_size * self.cell_posx
                    self.cell_posx += 1
                    self.direction()
                self.rect = self.rect.move(Speed // FPS, 0)
                self.imagename = f"Animations\\Right_Walk\\{(self.index + 1) % 4}.png"
                self.image = self.steps["Right_Walk"][(self.index + 1) % 4]
            elif self.rotation == "Left_Walk":
                if Speed // FPS + self.rect.x <= tile_size * self.cell_posx - tile_size // 2:
                    self.rect.x = tile_size * self.cell_posx - tile_size // 2
                    self.cell_posx -= 1
                    self.direction()
                self.rect = self.rect.move(-Speed // FPS, 0)
                self.imagename = f"Animations\\Left_Walk\\{(self.index + 1) % 4}.png"
                self.image = self.steps["Left_Walk"][(self.index + 1) % 4]
            elif self.rotation == "Up_Walk":
                if Speed // FPS + self.rect.y <= tile_size * self.cell_posy - tile_size // 2:
                    self.rect.y = tile_size * self.cell_posy - tile_size // 2
                    self.cell_posy -= 1
                    self.direction()
                self.rect = self.rect.move(0, -Speed // FPS)
                self.imagename = f"Animations\\Up_Walk\\{(self.index + 1) % 4}.png"
                self.image = self.steps["Up_Walk"][(self.index + 1) % 4]
            elif self.rotation == "Down_Walk":
                if Speed // FPS + self.rect.y >= tile_size * self.cell_posy + tile_size // 2:
                    self.rect.y = tile_size * self.cell_posy + tile_size // 2
                    self.cell_posy += 1
                    self.direction()
                self.rect = self.rect.move(0, Speed // FPS)
                self.imagename = f"Animations\\Down_Walk\\{(self.index + 1) % 4}.png"
                self.image = self.steps["Down_Walk"][(self.index + 1) % 4]

    def set_board(self, x, y):
        x, y = self.human_board.get_cell((x, y))
        print(x, y, self.human_board.board)
        self.human_board = self.to_wave_board(x, y, 1, self.human_board.board)
        print('зашел')
        for el in self.human_board:
            print(el)

    def to_wave_board(self, x, y, cur, lab):
        n, m = len(lab), len(lab[0])
        lab[x][y] = cur
        if y + 1 < m:
            if lab[x][y + 1] == 0 or (lab[x][y + 1] != -1 and lab[x][y + 1] > cur):
                self.to_wave_board(x, y + 1, cur + 1, lab)
        if x + 1 < n:
            if lab[x + 1][y] == 0 or (lab[x + 1][y] != -1 and lab[x + 1][y] > cur):
                self.to_wave_board(x + 1, y, cur + 1, lab)
        if x - 1 >= 0:
            if lab[x - 1][y] == 0 or (lab[x - 1][y] != -1 and lab[x - 1][y] > cur):
                self.to_wave_board(x - 1, y, cur + 1, lab)
        if y - 1 >= 0:
            if lab[x][y - 1] == 0 or (lab[x][y - 1] != -1 and lab[x][y - 1] > cur):
                self.to_wave_board(x, y - 1, cur + 1, lab)
        return lab

    def checkselect(self, posx, posy):
        im = Image.open(f"data\\{self.imagename}")
        size = im.size
        if posx >= self.rect.x and posx <= self.rect.x + size[0] and posy >= self.rect.y and posy <= self.rect.y + size[1] and not self.selected:
            self.selected = True
        else:
            if self.selected:
                self.selected = False


    def set_rotation(self, x):
        self.rotation = x

    def direction(self):
        # зигзагообразное движение
        for i, j, rot in self.rol:
            pole = self.human_board.board[self.cell_posy + i][self.cell_posx + j]
            if pole > 0:
                if pole < self.human_board.board[self.cell_posy][self.cell_posx]:
                    if self.rotation != rot:
                        self.rotation = rot
                        self.index = 0
                    self.image = self.steps[rot][0]
                    # скидываем в конец списка уже использованное направление
                    self.rol.remove((i, j, rot))
                    self.rol.append((i, j, rot))


if __name__ == '__main__': # можно стереть
    all_sprites = pygame.sprite.Group()
    s = [1, 2]
    for _ in range(1):
        Worker(s, all_sprites)
    sys.exit()
