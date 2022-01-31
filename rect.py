import pygame
import sys
import os

pygame.init()
tile_size = 20
FPS = 30
Speed = 100
size = width, height = 400, 400

screen = pygame.display.set_mode((width + 30, height + 30))


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

    def __init__(self, *group):
        super().__init__(*group)
        self.index = 0
        self.image = self.steps["Right_Walk"][0]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect = self.rect.move((5, 0))
        self.index = (self.index + 1) % 4
        self.image = self.steps["Right_Walk"][self.index]


def main():
    all_sprites = pygame.sprite.Group()
    Worker(all_sprites)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(FPS)  # переделать смену кадров по таймеру
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())

# up - move + down - up - move + down
