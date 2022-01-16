import pygame
import sys
import os
from random import *
from pytmx import *
from PIL import Image


pygame.init()
FPS = 30
Speed = 100
size = width, height = 450, 450
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Adventure strategy")


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    return pygame.image.load(fullname)


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
                    (self.left + j * self.cell_size, self.top + i * self.cell_size), (self.cell_size, self.cell_size)),
                                     1)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if x + 1 > self.width or y + 1 > self.height or x == -1 or y == -1:
            print(None)
            return None
        print(x, y)
        return (y, x)

    def change_margin(self, top, left):
        self.top += top
        self.left += left



class Worker(pygame.sprite.Sprite):
    steps1 = [load_image(f"Animations\\Right_Walk\\{i}.png") for i in range(1, 5)]
    steps2 = [load_image(f"Animations\\Left_Walk\\{i}.png") for i in range(1, 5)]
    steps3 = [load_image(f"Animations\\Up_Walk\\{i}.png") for i in range(1, 5)]
    steps4 = [load_image(f"Animations\\Down_Walk\\{i}.png") for i in range(1, 5)]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Worker.steps3[0]
        self.selected = False
        self.rotation = 'Up_Walk'
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = randrange(height - self.rect[3])

    def update(self):
        # сюда таймер
        if self.rotation == "Right_Walk":
            self.rect = self.rect.move(Speed // FPS, 0)
            self.imagename = f"Animations\\Right_Walk\\{(self.steps1.index(self.image) + 1)}.png"
            self.image = self.steps1[(self.steps1.index(self.image) + 1) % 4]
        elif self.rotation == "Left_Walk":
            self.rect = self.rect.move(-Speed // FPS, 0)
            self.imagename = f"Animations\\Left_Walk\\{(self.steps2.index(self.image) + 1)}.png"
            self.image = self.steps2[(self.steps2.index(self.image) + 1) % 4]
        elif self.rotation == "Up_Walk":
            self.rect = self.rect.move(0, -Speed // FPS)
            self.imagename = f"Animations\\Up_Walk\\{(self.steps3.index(self.image) + 1)}.png"
            self.image = self.steps3[(self.steps3.index(self.image) + 1) % 4]
        elif self.rotation == "Down_Walk":
            self.rect = self.rect.move(0, Speed // FPS)
            self.imagename = f"Animations\\Down_Walk\\{(self.steps2.index(self.image) + 1)}.png"
            self.image = self.steps4[(self.steps4.index(self.image) + 1) % 4]


    def delselect(self):
        self.selected = False

    def checkselect(self, posx, posy):
        im = Image.open(f"data\\{self.imagename}")
        size = im.size
        return posx >= self.rect.x and posx <= self.rect.x + size[0] and posy >= self.rect.y and posy <= self.rect.y\
               + size[1]

    def select(self):
        self.selected = True

    def selected(self):
        return self.selected

    def change_rotation(self, x):
        self.rotation = x


def main():
    tile_size = 30
    map = load_pygame(f'maps/some.tmx')
    all_sprites = pygame.sprite.Group()
    for _ in range(2):
        Worker(all_sprites)
    clock = pygame.time.Clock()
    board = Board(width // tile_size, height // tile_size, tile_size)
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
                            sprite.select()
                            continue
                        sprite.delselect()
                for i in range(10):
                    Worker(all_sprites)
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
