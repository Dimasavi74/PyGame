import pygame
import sys
import os

from const import TILE_SIZE as tile_size, FPS, WIDTH as width, HEIGHT as height, BOARD as board, \
    XCAM as xCam, YCAM as yCam, KCAM as kCam, SPEED as Speed


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    im = pygame.image.load(fullname)
    im.set_colorkey((100, 100, 100))
    return im


class Worker(pygame.sprite.Sprite):
    steps1 = [load_image(f"Animations\\Right_Walk\\{i}.png") for i in range(4)]
    steps2 = [load_image(f"Animations\\Left_Walk\\{i}.png") for i in range(4)]
    steps3 = [load_image(f"Animations\\Up_Walk\\{i}.png") for i in range(4)]
    steps4 = [load_image(f"Animations\\Down_Walk\\{i}.png") for i in range(4)]

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.board = board
        self.image = Worker.steps3[0]
        self.human_board = board
        self.imagename = f"Animations\\Up_Walk\\1.png"
        self.selected = False
        self.rotation = 'Up_Walk'
        self.can_go = False

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = board.get_coords((x, y), (self.rect[2], self.rect[3]))
        self.cell_posx = x
        self.cell_posy = y
        self.order_list = [1, 2, 3, 4]

    def update(self):
        if self.can_go:
            if self.rotation == "Right_Walk":
                try:
                    self.steps1.index(self.image)
                except Exception:
                    self.image = Worker.steps1[0]
                if Speed // FPS + self.rect.x >= tile_size * self.cell_posx + xCam:
                    self.rect.x = tile_size * self.cell_posx + xCam
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

    def set_board(self, x, y):
        x, y = self.board.get_cell((x, y))
        self.human_board = self.to_wave_board(x, y, self.board.get_board())

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

    def set_rotation(self, x):
        self.rotation = x

    def can_go_true(self):
        self.can_go = True

    def direction(self):
        if self.human_board[self.cell_posy][self.cell_posx] == 1:
            self.can_go = False
        for el in self.order_list:
            if el == 1:
                try:
                    if self.human_board[self.cell_posy][self.cell_posx + 1] < self.human_board[self.cell_posy][
                        self.cell_posx] and self.human_board[self.cell_posy][self.cell_posx + 1] > 0:
                        self.rotation = "Right_Walk"
                        self.order_list.remove(1)
                        self.order_list.append(1)
                        break
                except Exception:
                    pass
            if el == 2:
                try:
                    if self.human_board[self.cell_posy][self.cell_posx - 1] < self.human_board[self.cell_posy][
                        self.cell_posx] and self.human_board[self.cell_posy][self.cell_posx - 1] > 0:
                        self.rotation = "Left_Walk"
                        self.order_list.remove(2)
                        self.order_list.append(2)
                        break
                except Exception:
                    pass
            if el == 3:
                try:
                    if self.human_board[self.cell_posy - 1][self.cell_posx] < self.human_board[self.cell_posy][
                        self.cell_posx] and self.human_board[self.cell_posy - 1][self.cell_posx] > 0:
                        self.rotation = "Up_Walk"
                        self.order_list.remove(3)
                        self.order_list.append(3)
                        break
                except Exception:
                    pass
            if el == 4:
                try:
                    if self.human_board[self.cell_posy + 1][self.cell_posx] < self.human_board[self.cell_posy][
                        self.cell_posx] and self.human_board[self.cell_posy + 1][self.cell_posx] > 0:
                        self.rotation = "Down_Walk"
                        self.order_list.remove(4)
                        self.order_list.append(4)
                        break
                except Exception:
                    pass
