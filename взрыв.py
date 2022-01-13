import pygame
import sys
import os
from random import *

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Adventure strategy")


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    return pygame.image.load(fullname)


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = randrange(width)
        self.rect.y = randrange(height)

    def update(self):
        self.rect = self.rect.move(randrange(3) - 1,
                                   randrange(3) - 1)


def main():
    all_sprites = pygame.sprite.Group()
    for _ in range(10):
        Bomb(all_sprites)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())

