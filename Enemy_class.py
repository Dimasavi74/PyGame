from Worker_class import Worker, load_image
from const import BOARD as board
import pygame
import sys
import os
from random import *
from pytmx import *
import copy

print(board.board)
pygame.init()
screen = pygame.display.set_mode((800, 800))


def group_enemy(where='up'):
    pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image("Animations\\Enemy\\0.png")

    def update(self):
        pass



if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    Enemy(1, 2, all_sprites)
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
