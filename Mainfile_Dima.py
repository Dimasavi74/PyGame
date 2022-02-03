# Нормальное перемещение камеры(мышь)
# Движение по клеткам(волновой алгаритм, щелчки мыши)
# Прозрачные картинки
# Приближение камеры
# Изменение размеров тайлов, своя карта
import pygame
import sys
import os
from random import *
from pytmx import *
import copy
from Worker_class import Worker, load_image
from const import TILE_SIZE as tile_size, FPS, WIDTH as width, HEIGHT as height, BOARD as board, \
    XCAM as xCam, YCAM as yCam, KCAM as kCam

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adventure strategy")


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.imagename = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def checkselect(self, x, y):
        return self.rect[2] + self.rect[0] >= x >= self.rect[0] and self.rect[3] + self.rect[1] >= y >= self.rect[1]


class Build_button(Button):
    def __init__(self, x, y, image, *group):
        super().__init__(x, y, image, *group)
        self.build_menu = False

    def activate(self, group):
        for el in group:
            if self.build_menu:
                el.rect.y = 800
            else:
                el.rect.y = 600
        self.build_menu = not self.build_menu


class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.imagename = image
        self.image = load_image(self.imagename)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = board.get_coords((x, y), (self.rect[2], self.rect[3]))

    def update(self):
        pass


def main():
    global xCam, yCam, kCam
    map = load_pygame(f'maps/some1.tmx')
    all_sprites = pygame.sprite.Group()
    all_human_sprites = pygame.sprite.Group()
    all_building_sprites = pygame.sprite.Group()
    all_buttons = pygame.sprite.Group()
    build_board = pygame.sprite.Group()

    build_board_background = pygame.sprite.Sprite()
    build_board_background.image = load_image("build_board_background.png")
    build_board_background.rect = build_board_background.image.get_rect()
    build_board_background.rect.x, build_board_background.rect.y = 0, 800
    build_board.add(build_board_background)

    # слегка надоедает)
    '''pygame.mixer.init()
    pygame.mixer.set_reserved(0)
    game_music = pygame.mixer.Sound("data\\DSG.mp3")
    pygame.mixer.Channel(0).play(game_music, -1)'''

    Worker(1, 1, all_sprites)
    Worker(1, 2, all_sprites)
    Build_button(width - 100, height - 100, "build_button.png", all_buttons)
    clock = pygame.time.Clock()
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
                    for button in all_buttons:
                        if button.checkselect(event.pos[0], event.pos[1]):
                            button.activate(build_board)
                    for sprite in all_sprites:
                        if sprite.checkselect(event.pos[0], event.pos[1]):
                            sprite.select()
                            continue
                        sprite.delselect()
                if event.button == 3:
                    for sprite in all_sprites:
                        if sprite.selected:
                            print(board.get_cell((event.pos[0], event.pos[1])))
                            coords = board.get_cell((event.pos[0], event.pos[1]))
                            if board.get_board()[coords[1]][coords[1]] < 0:
                                break
                            sprite.set_board(event.pos[0], event.pos[1])
                            sprite.direction()
                            sprite.can_go_true()
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
        for x in range(100):
            for y in range(100):
                image = map.get_tile_image(x, y, 0)
                screen.blit(image, (int(tile_size * kCam * x + xCam), int(tile_size * kCam * y + yCam)))
        if board_render:
            board.render(screen)
        all_sprites.draw(screen)
        build_board.draw(screen)
        all_buttons.draw(screen)
        all_sprites.update()

        clock.tick(FPS)  # переделать смену кадров по таймеру
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
