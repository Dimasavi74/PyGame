import pygame
import sys
import os

tile_size = 20
FPS = 20
Speed = 100
size = width, height = 400, 400


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

    def __init__(self, x, y, *group):
        super().__init__(*group)
        global board
        self.index = 0
        self.image = Worker.steps["Right_Walk"][self.index]
        self.human_board = board
        self.selected = False
        self.rotation = 'Right_Walk'
        self.can_go = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = board.get_coords((x, y))
        self.cell_posx = x
        self.cell_posy = y
        self.order_list = [1, 2, 3, 4]

        self.ost = 0


    def update(self):
        if self.index == 4:
            #self.direction()
            if self.rotation == "Right_Walk":
                self.ost = tile_size - self.rect[2]
                # удвоенный остаток от картинки слева и справа
                self.index = 1
                self.image = Worker.steps[self.rotation][0]
                # так и должно быть))
        else:
            move = self.ost // (4 - self.index) # более точный расчёт, чтобы точно проходил от середины до середины
            #self.rect.x += move
            self.rect.move((move, 0))
            self.ost -= move
            self.image = Worker.steps[self.rotation][self.index]
            self.index += 1


'''        try:
            self.steps1.index(self.image)
        except Exception:
            self.image = Worker.steps1[0]
        self.rect.x += tile_size
        self.cell_posx += 1
        self.direction()
        self.rect = self.rect.move(Speed // FPS, 0)
        self.image = self.steps1[self.steps1.index(self.image) + 1]
        self.imagename = f"Animations\\Right_Walk\\{(self.steps1.index(self.image) + 1)}.png"'''


    def update_1(self):
        '''
        sl = {"Right_Walk": }

        '''

        global tile_size
        if self.can_go:
            if self.rotation == "Right_Walk":
                try:
                    self.steps1.index(self.image)
                except Exception:
                    self.image = Worker.steps1[0]
                if Speed // FPS + self.rect.x >= tile_size * self.cell_posx + tile_size // 2:
                    self.rect.x = tile_size * self.cell_posx + tile_size // 2
                    self.cell_posx += 1
                    self.direction()
                self.rect = self.rect.move(Speed // FPS, 0)
                self.image = self.steps1[(self.steps1.index(self.image) + 1) % 4]
                self.imagename = f"Animations\\Right_Walk\\{(self.steps1.index(self.image) + 1)}.png"
            elif self.rotation == "Left_Walk":
                try:
                    self.steps2.index(self.image)
                except Exception:
                    self.image = Worker.steps2[0]
                if Speed // FPS + self.rect.x <= tile_size * self.cell_posx - tile_size // 2:
                    self.rect.x = tile_size * self.cell_posx - tile_size // 2
                    self.cell_posx -= 1
                    self.direction()
                self.rect = self.rect.move(-Speed // FPS, 0)
                self.imagename = f"Animations\\Left_Walk\\{(self.steps2.index(self.image) + 1)}.png"
                self.image = self.steps2[(self.steps2.index(self.image) + 1) % 4]
            elif self.rotation == "Up_Walk":
                try:
                    self.steps3.index(self.image)
                except Exception:
                    self.image = Worker.steps3[0]
                if Speed // FPS + self.rect.y <= tile_size * self.cell_posy - tile_size // 2:
                    self.rect.y = tile_size * self.cell_posy - tile_size // 2
                    self.cell_posy -= 1
                    self.direction()
                self.rect = self.rect.move(0, -Speed // FPS)
                self.imagename = f"Animations\\Up_Walk\\{(self.steps3.index(self.image) + 1)}.png"
                self.image = self.steps3[(self.steps3.index(self.image) + 1) % 4]
            elif self.rotation == "Down_Walk":
                try:
                    self.steps4.index(self.image)
                except Exception:
                    self.image = Worker.steps4[0]
                if Speed // FPS + self.rect.y >= tile_size * self.cell_posy + tile_size // 2:
                    self.rect.y = tile_size * self.cell_posy + tile_size // 2
                    self.cell_posy += 1
                    self.direction()
                self.rect = self.rect.move(0, Speed // FPS)
                self.imagename = f"Animations\\Down_Walk\\{(self.steps4.index(self.image) + 1)}.png"
                self.image = self.steps4[(self.steps4.index(self.image) + 1) % 4]
