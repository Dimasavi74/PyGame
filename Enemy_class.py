from Worker_class import Worker, load_image
from const import TILE_SIZE as tile_size, FPS, WIDTH as width, HEIGHT as height, BOARD as board, SPEED as Speed
import pygame
import sys
import os
from random import *
from pytmx import *
import copy

Speed *= 2
pygame.init()
screen = pygame.display.set_mode((800, 800))


def battle():
    pass


def group_enemy(where='up'):
    pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        board.board[y][x] = -1  # отмечаем на карте
        self.cell_posx, self.cell_posy = x, y
        self.rotation = "Down_Walk"
        self.can_go = True
        self.order_list = [(0, 1, "Right_Walk"), (0, -1, "Left_Walk"), (-1, 0, "Up_Walk"), (1, 0, "Down_Walk")]

    def direction(self):
        if self.path[self.cell_posy][self.cell_posx] == 1:
            self.can_go = False
        for i, j, rot in self.order_list:
            cur = self.path[self.cell_posy][self.cell_posx]
            new = self.path[self.cell_posy + i][self.cell_posx + j]
            if cur > new > 0:
                self.rotation = rot
                self.order_list.remove((i, j, rot))
                self.order_list.append((i, j, rot))
                break

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
        ##############################
        self.hp = 100
        self.hit = 20
        self.protect = 0.5
        ##############################
        self.image = load_image("Animations\\Enemy\\0.png")  # кратинка ближника0


class Destroyer(pygame.sprite.Sprite):
    steps = {"Right_Walk": [load_image(f"Animations\\Enemy\\Right_Walk\\{i}.png") for i in range(4)],
             "Left_Walk": [load_image(f"Animations\\Enemy\\Left_Walk\\{i}.png") for i in range(4)],
             "Down_Walk": [load_image(f"Animations\\Enemy\\Down_Walk\\{i}.png") for i in range(4)],
             "Up_Walk": [load_image(f"Animations\\Enemy\\Up_Walk\\{i}.png") for i in range(4)]}

    def __init__(self, x, y, *group):
        super().__init__(*group)
        ##############################
        self.hp = 100
        self.hit = 10
        self.protect = 0.1
        ##############################
        board.board[y][x] = -1  # отмечаем на карте
        self.can_go = True
        self.cell_posx, self.cell_posy = x, y
        self.main = len(board.board) // 2
        self.change_rot = ["Right_Walk" if x < self.main else "Left_Walk",
                           "Down_Walk" if y < self.main else "Up_Walk"]
        self.rotation = self.change_rot[0]
        self.image = load_image(f"Animations\\Enemy\\{self.rotation}\\0.png")
        self.index = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = board.get_coords((x, y), (self.rect[2], self.rect[3]))

    def update(self, xCam, yCam):
        if self.can_go:
            self.image = load_image(f"Animations\\Enemy\\{self.rotation}\\{self.index}.png")
            self.index = (self.index + 1) % 4
            if self.rotation == "Right_Walk":
                ma = tile_size * (self.cell_posx + 1) + self.set_centre(self.rect[2]) + xCam
                if Speed // FPS + self.rect.x >= ma:
                    self.rect.x = ma
                    self.cell_posx += 1
                    self.direction()
                    return None
                self.rect = self.rect.move(Speed // FPS, 0)
            if self.rotation == "Left_Walk":
                ma = tile_size * (self.cell_posx - 1) + self.set_centre(self.rect[2]) + xCam
                if self.rect.x - Speed // FPS <= ma:
                    self.rect.x = ma
                    self.cell_posx -= 1
                    self.direction()
                    return None
                self.rect = self.rect.move(-Speed // FPS, 0)
            if self.rotation == "Up_Walk":
                ma = tile_size * (self.cell_posy - 1) + self.set_centre(self.rect[3]) + yCam
                if self.rect.y - Speed // FPS <= ma:
                    self.rect.y = ma
                    self.cell_posy -= 1
                    self.direction()
                    return None
                self.rect = self.rect.move(0, -Speed // FPS)
            if self.rotation == "Down_Walk":
                ma = tile_size * (self.cell_posy + 1) + self.set_centre(self.rect[3]) + yCam
                if self.rect.y + Speed // FPS >= ma:
                    self.rect.y = ma
                    self.cell_posy += 1
                    self.direction()
                    return None
                self.rect = self.rect.move(0, Speed // FPS)

    def set_centre(self, size):
        if tile_size >= size:
            return (tile_size - size) // 2
        return -(size - tile_size + 2)

    def direction(self):
        if len(self.change_rot) == 2:
            if self.cell_posx != self.main and self.cell_posy != self.main:
                if self.rotation == self.change_rot[0]:
                    self.rotation = self.change_rot[1]
                else:
                    self.rotation = self.change_rot[0]
                self.index = 0
            else:
                if self.cell_posx == self.main:
                    del self.change_rot[0]
                    self.rotation = self.change_rot[0]
                else:
                    del self.change_rot[1]
                    self.rotation = self.change_rot[0]
        i, j = {"Right_Walk": (0,1), "Left_Walk": (0,-1), "Up_Walk": (-1,0), "Down_Walk": (1,0)}[self.rotation]
        new_cell = board.board[self.cell_posy + i][self.cell_posx + j]
        if new_cell < 0:
            self.can_go = False
            if new_cell == -4:
                pass
                # добавить окончание игры, ведь врга дошёл до ратуши
            elif new_cell == 5:
                self.destroy()
        else:
            board.board[self.cell_posy][self.cell_posx] = 0
            new_cell = -1

    def destroy(self):
        pass
        # здесь сделаем также как и при строительстве здания (можно добавить взрырвы), то есть оно будет всё меньше меньше а потом:
        # board.board[self.cell_posy][self.cell_posx] = 0 старую освобождаем
        # board.board[self.cell_posy + i][self.cell_posx + j] = -1 новую занимаем
        # self.can_go = True


'''if __name__ == '__main__':
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
    pygame.quit()'''
