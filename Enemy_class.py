from Worker_class import Worker, load_image
from const import TILE_SIZE as tile_size, FPS, WIDTH as width, HEIGHT as height, BOARD as board, \
    XCAM as xCam, YCAM as yCam, KCAM as kCam, SPEED as Speed
import pygame
import sys
import os
from random import *
from pytmx import *
import copy

pygame.init()
screen = pygame.display.set_mode((800, 800))


def group_enemy(where='up'):
    pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        board.board[y][x] = -1  # отмечаем на карте
        self.cell_posx, self.cell_posy = x, y
        self.rotation = "Down_Walk"
        self.order_list = [(0, 1, "Right_Walk"), (0, -1, "Left_Walk"), (-1, 0, "Up_Walk"), (1, 0, "Down_Walk")]

    def direction(self):
        if self.path[self.cell_posy][self.cell_posx] == 1:
            self.can_go = False
        for i, j, rot in self.order_list:
            cur = self.path[self.cell_posy][self.cell_posx]
            new = self.path[self.cell_posy + i][self.cell_posx + j]
            if new < cur and new == 0:
                self.rotation = rot
                self.order_list.remove((i, j, rot))
                self.order_list.append((i, j, rot))

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


class Infighting(Enemy):
    def __init__(self, x, y, *group):
        super().__init__(x, y, *group)
        self.image = load_image("Animations\\Enemy\\0.png")  # кратинка ближника0


class Destroyer(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        board.board[y][x] = -1  # отмечаем на карте
        self.cell_posx, self.cell_posy = x, y
        self.main = len(board.board) // 2
        self.change_rot = ("Right_Walk" if x < self.main else "Left_Walk",
                           "Down_Walk" if y < self.main else "Up_Walk")
        self.rotation = self.change_rot[0]
        self.image = load_image("Animations\\Enemy\\0.png")  # картинка разрушителя
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = board.get_coords((x, y), (self.rect[2], self.rect[3]))

    def update(self):
        if self.rotation == "Right_Walk":
            if Speed // FPS + self.rect.x >= tile_size * self.cell_posx + tile_size // 2 + xCam:
                self.rect.x = tile_size * self.cell_posx + tile_size // 2 + xCam
                self.cell_posx += 1
                if len(self.change_rot) == 2:
                    self.direction()
            self.rect = self.rect.move(Speed // FPS, 0)
        if self.rotation == "Left_Walk":
            if Speed // FPS + self.rect.x <= tile_size * self.cell_posx - tile_size // 2 + xCam:
                self.rect.x = tile_size * self.cell_posx - tile_size // 2 + xCam
                self.cell_posx -= 1
                if len(self.change_rot) == 2:
                    self.direction()
            self.rect = self.rect.move(-Speed // FPS, 0)
        if self.rotation == "Up_Walk":
            if Speed // FPS + self.rect.y <= tile_size * self.cell_posy - tile_size // 2 + yCam:
                self.rect.y = tile_size * self.cell_posy - tile_size // 2 + yCam
                self.cell_posy -= 1
                if len(self.change_rot) == 2:
                    self.direction()
            self.rect = self.rect.move(0, -Speed // FPS)
        if self.rotation == "Down_Walk":
            if Speed // FPS + self.rect.y >= tile_size * self.cell_posy + tile_size // 2 + yCam:
                self.rect.y = tile_size * self.cell_posy + tile_size // 2 + yCam
                self.cell_posy += 1
                if len(self.change_rot) == 2:
                    self.direction()
            self.rect = self.rect.move(0, Speed // FPS)

    def nothing(self):
        if self.rotation == self.change_rot[0]:
            self.rotation = self.change_rot[1]
        else:
            self.rotation = self.change_rot[0]

    def direction(self):
        if self.cell_posx != self.main and self.cell_posy != self.main:
            self.nothing()
        else:
            if self.cell_posx == self.main:
                del self.change_rot[0]
                self.rotation = self.change_rot[0]
            else:
                del self.change_rot[1]
                self.rotation = self.change_rot[0]


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    Destroyer(1, 2, all_sprites)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(15)  # переделать смену кадров по таймеру
        pygame.display.flip()
    pygame.quit()
