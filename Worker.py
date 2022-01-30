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
    im = pygame.image.load(fullname)
    im.set_colorkey((0, 0, 0))
    return im


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
        self.imagename = f"Animations\\Down_Walk\\0.png"

        self.order_list = [("Right_Walk", 0, 1), ("Left_Walk", 0, -1), ("Up_Walk", -1, 0), ("Down_Walk", 1, 0)]
        self.rect = self.image.get_rect()
        self.cell_posx, self.cell_posy = 1, 1 # здесь задавать координаты!

        self.rect.x, self.rect.y = board.get_coords((self.cell_posx, self.cell_posy))
        self.rect.x += self.set_centre(self.rect[2], tile_size)
        self.rect.y += self.set_centre(self.rect[3], tile_size)

        self.human_board = board
        self.selected = False
        self.can_go = False

    def set_centre(self, size, cell_size):
        if cell_size >= size:
            return (cell_size - size) // 2
        return -((size - cell_size) + 2)

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

    def set_board(self, x, y):
        x, y = self.human_board.get_cell((x, y))
        self.human_board.board = self.to_wave_board(y, x, self.human_board.board)

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

    def set_rotation(self, x):
        self.rotation = x

    def direction(self):
        if self.human_board.board[self.cell_posy][self.cell_posx] == 1:
            self.can_go = False
        for rot, i, j in self.order_list:
            pole = self.human_board.board[self.cell_posy + i][self.cell_posx + j]
            if pole > 0 and pole < self.human_board.board[self.cell_posy][self.cell_posx]:
                if self.rotation != rot:
                    self.rotation = rot
                    self.index = 0
                    self.image = self.steps[rot][(self.index + 1) % 4]
                self.order_list.remove((rot, i, j))
                self.order_list.append((rot, i, j))
                break


'''if __name__ == '__main__': # можно стереть
    all_sprites = pygame.sprite.Group()
    s = [1, 2]
    for _ in range(1):
        Worker(s, all_sprites)
    sys.exit()'''
