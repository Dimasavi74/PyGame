import pygame
import sys
import os

from const import TILE_SIZE as tile_size, FPS, WIDTH as width, HEIGHT as height, BOARD as board, SPEED as Speed,\
    xCam, yCam, kCam


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
        ##############################
        self.hp = 100
        self.hit = 8
        self.protect = 0
        ##############################
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
        self.order_list = [(0, 1, "Right_Walk"), (0, -1, "Left_Walk"), (-1, 0, "Up_Walk"), (1, 0, "Down_Walk")]
        # self.order_list = [1, 2, 3, 4]

    def update(self, xCam, yCam):
        if self.can_go:
            if self.rotation == "Right_Walk":
                try:
                    self.steps1.index(self.image)
                except Exception:
                    self.image = Worker.steps1[0]
                ma = tile_size * (self.cell_posx + 1) + xCam + self.set_centre(self.rect[2])
                if Speed // FPS + self.rect.x >= ma:
                    self.rect.x = ma
                    self.cell_posx += 1
                    self.direction()
                    return None
                self.rect = self.rect.move(Speed // FPS, 0)
                self.image = self.steps1[(self.steps1.index(self.image) + 1) % 4]
                self.imagename = f"Animations\\Right_Walk\\{(self.steps1.index(self.image))}.png"
            elif self.rotation == "Left_Walk":
                try:
                    self.steps2.index(self.image)
                except Exception:
                    self.image = Worker.steps2[0]
                ma = tile_size * (self.cell_posx - 1) + xCam + self.set_centre(self.rect[2])
                if self.rect.x - Speed // FPS <= ma:
                    self.rect.x = ma
                    self.cell_posx -= 1
                    self.direction()
                    return None
                self.rect = self.rect.move(-Speed // FPS, 0)
                self.imagename = f"Animations\\Left_Walk\\{(self.steps2.index(self.image))}.png"
                self.image = self.steps2[(self.steps2.index(self.image) + 1) % 4]
            elif self.rotation == "Up_Walk":
                try:
                    self.steps3.index(self.image)
                except Exception:
                    self.image = Worker.steps3[0]
                ma = tile_size * (self.cell_posy - 1) + self.set_centre(self.rect[3]) + yCam
                if self.rect.y - Speed // FPS <= ma:
                    self.rect.y = ma
                    self.cell_posy -= 1
                    self.direction()
                    return None
                self.rect = self.rect.move(0, -Speed // FPS)
                self.imagename = f"Animations\\Up_Walk\\{(self.steps3.index(self.image))}.png"
                self.image = self.steps3[(self.steps3.index(self.image) + 1) % 4]
            elif self.rotation == "Down_Walk":
                try:
                    self.steps4.index(self.image)
                except Exception:
                    self.image = Worker.steps4[0]
                ma = tile_size * (self.cell_posy + 1) + self.set_centre(self.rect[3]) + yCam
                if self.rect.y + Speed // FPS >= ma:
                    self.rect.y = ma
                    self.cell_posy += 1
                    self.direction()
                    return None
                self.rect = self.rect.move(0, Speed // FPS)
                self.imagename = f"Animations\\Down_Walk\\{(self.steps4.index(self.image))}.png"
                self.image = self.steps4[(self.steps4.index(self.image) + 1) % 4]

    def set_centre(self, size):
        if tile_size >= size:
            return (tile_size - size) // 2
        return -((size - tile_size) + 2)

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
            return None
        for i, j, rot in self.order_list:
            cur = self.human_board[self.cell_posy][self.cell_posx]
            new = self.human_board[self.cell_posy + i][self.cell_posx + j]
            if cur > new > 0:
                self.rotation = rot
                self.order_list.remove((i, j, rot))
                self.order_list.append((i, j, rot))
                break
        board.board[self.cell_posy][self.cell_posx] = 0
        i, j = {"Right_Walk": (0,1), "Left_Walk": (0,-1), "Up_Walk": (-1,0), "Down_Walk": (1,0)}[self.rotation]
        board.board[self.cell_posy + i][self.cell_posx + j] = -1
