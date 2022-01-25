# Нормальное перемещение камеры(мышь)
# Движение по клеткам(волновой алгаритм, щелчки мыши)
# Прозрачные картинки
# Приближение камеры
# Изменение размеров тайлов, своя карта
from Worker import Worker
import change as change
import pygame
import sys
import os
from random import *
from pytmx import *
from PIL import Image
import copy

pygame.init()
FPS = 15
Speed = 100
tile_size = 30
size = width, height = 450, 450

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Adventure strategy")


class Board:
    def __init__(self, width, height, top=0, left=0):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = left
        self.top = top

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def render(self, screen):
        for i in range(len(self.board)):
            y = self.board[i]
            for j in range(len(y)):
                if y[j] == 0:
                    pygame.draw.rect(screen, 'white', (
                        (self.left + j * tile_size, self.top + i * tile_size),
                        (tile_size, tile_size)), 1)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // tile_size
        y = (mouse_pos[1] - self.top) // tile_size
        if -1 < x < self.width and -1 < y < self.height:
            return x, y

    def get_coords(self, cell):
        x = cell[0] * tile_size + self.left + tile_size / 2
        y = cell[1] * tile_size + self.top + tile_size / 2
        return x, y

    def change_margin(self, top, left):
        self.top += top
        self.left += left

    def get_board(self):
        # return self.board
        return copy.deepcopy(self.board)


board = Board(width // tile_size, height // tile_size)

def main():
    global board
    map = load_pygame(f'maps/some.tmx')
    all_sprites = pygame.sprite.Group()
    for _ in range(1):
        Worker(board, all_sprites)
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
                    board_render = not board_render
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for sprite in all_sprites:
                        sprite.checkselect(event.pos[0], event.pos[1])
                if event.button == 3:
                    for sprite in all_sprites:
                        if sprite.selected:
                            print('выбран')
                            coords = board.get_cell((event.pos[0], event.pos[1]))
                            if board.get_board()[coords[1]][coords[1]] < 0:
                                print('вышел')
                                break
                            sprite.set_board(event.pos[0], event.pos[1])
                            sprite.direction()
                            sprite.can_go = True
            if pygame.key.get_pressed()[pygame.K_d]: # рассматривать зажим клавиши
                xCam += 15
                for sprite in all_sprites:
                    sprite.rect.x += 15
                board.change_margin(0, 15)
            if pygame.key.get_pressed()[pygame.K_a]:
                xCam -= 15
                for sprite in all_sprites:
                    sprite.rect.x -= 15
                board.change_margin(0, -15)
            if pygame.key.get_pressed()[pygame.K_s]:
                yCam += 15
                for sprite in all_sprites:
                    sprite.rect.y += 15
                board.change_margin(15, 0)
            if pygame.key.get_pressed()[pygame.K_w]:
                yCam -= 15
                for sprite in all_sprites:
                    sprite.rect.y -= 15
                board.change_margin(-15, 0)
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
