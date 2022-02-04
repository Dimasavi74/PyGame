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
from PIL import Image
import copy
import pygame_gui


pygame.init()
tile_size = 20
FPS = 30
Speed = 150
Bsize = 100
size = width, height = 1200, 800
xCam = 0
yCam = 0
kCam = 1
all_sprites = pygame.sprite.Group()
all_human_sprites = pygame.sprite.Group()
all_buildings = pygame.sprite.Group()
all_buttons = pygame.sprite.Group()
build_board = pygame.sprite.Group()
mini_buildings = pygame.sprite.Group()
buildings_in_process = pygame.sprite.Group()
houseMenuBackgrounds = pygame.sprite.Group()
building_mode = False
reset_build_menu = False
show_townhall_menu = False
townhall_strength = 1000
inTh, inBs, inSm, inMl, inCv = False, False, False, False, False
buildng_name_right_now = ''
stone = 500
wood = 500
food = 500
iron = 200
numb_of_equipment = 0
numb_of_workers = 2
all_texts = []
townHallTexts = []
manager = pygame_gui.UIManager((1200, 800))

add_Worker = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((1050, 480), (100, 50)),
    text="Добавить",
    manager=manager,
    visible=False
)

create_Equipment = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((1050, 400), (100, 50)),
    text="Создать",
    manager=manager,
    visible=False
)

exit_from_building = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((1050, 550), (100, 50)),
    text="Выйти",
    manager=manager,
    visible=False
)

building_sizes = {
    "sawmill": (4, 3),
    "cave": (4, 4),
    "mill": (4, 6),
    "living_house": (3, 5),
    "hospital": (4, 3),
    "blacksmith": (4, 4),
    "townhall": (8, 4)
}  # (x, y)
building_names = {
    "0": "sawmill",
    "1": "cave",
    "2": "mill",
    "3": "living_house",
    "4": "hospital",
    "5": "blacksmith"
}  # Для i при инициализации MiniBuildings
building_time = {
    "sawmill": 10,
    "cave": 10,
    "mill": 10,
    "living_house": 5,
    "hospital": 15,
    "blacksmith": 15
}  # seconds
building_costs = {
    "sawmill": (0, 200, 0, 20),
    "cave": (0, 200, 0, 100),
    "mill": (200, 100, 50, 20),
    "living_house": (100, 100, 0, 50),
    "hospital": (200, 200, 0, 100),
    "blacksmith": (400, 200, 0, 200)
}  # building_name: (stone, wood, food, iron)
building_strengths = {
    "sawmill": 200,
    "cave": 200,
    "mill": 200,
    "living_house": 200,
    "hospital": 300,
    "blacksmith": 300,
    "townhall": 1000
}

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adventure strategy")

def open_house_menu(building_name):
    if building_name == "townhall":
        pass


def can_build(x_cell, y_cell, building_name):
    cell_sizes = building_sizes[building_name]
    cost = building_costs[building_name]
    board_part = [[j for j in i[x_cell:x_cell + cell_sizes[0] + 1]] for i in
                  board.get_board()[y_cell:y_cell + cell_sizes[1] + 1]]
    for ely in board_part:
        for elx in ely:
            if elx < 0:
                return False
    if cost > (stone, wood, food, iron):
        return False
    return True

def add_building_to_board(x_cell, y_cell, building_name):
    cell_sizes = building_sizes[building_name]
    board_copy_to_add_building = board.get_board()
    for i in range(y_cell, cell_sizes[1] + y_cell):
        for j in range(x_cell, cell_sizes[0] + x_cell):
            board_copy_to_add_building[i][j] = -4
    board.board = board_copy_to_add_building[:]


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    im = pygame.image.load(fullname)
    im.set_colorkey((100, 100, 100))
    return im


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.imagename = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def checkselect(self, posx, posy):
        im = Image.open(f"data\\{self.imagename}")
        size = im.size
        return posx >= self.rect.x and posx <= self.rect.x + size[0] and posy >= self.rect.y and posy <= self.rect.y \
               + size[1]


class Build_button(Button):
    def __init__(self, x, y, image, *group):
        super().__init__(x, y, image, *group)
        self.build_menu = False
        self.name = "Build_button"

    def activate(self, group):
        self.build_menu = not self.build_menu
        if self.build_menu:
            for el in group:
                try:
                    el.rect.y = 600
                    if el.name == "Build_house_button":
                        el.rect.y = 625
                    elif el.name == "MiniBuilding":
                        el.rect.y = 700 - el.rect[3] // 2
                except Exception:
                    pass
        else:
            for el in group:
                el.rect.y = 800


class Build_house_button(Button):
    def __init__(self, x, y, image, buildingName, *group):
        super().__init__(x, y, image, *group)
        global building_names
        self.build_now = False
        self.name = "Build_house_button"
        self.buildingName = building_names[buildingName[0]]

    def activate(self, button, mouse, group):
        global building_mode, reset_build_menu
        button.activate(group)
        reset_build_menu = True
        building_mode = True
        mouse.image = load_image(f"{self.buildingName}.png")


class Board:
    def __init__(self, width, height, size, top=0, left=0):
        self.width = Bsize * size
        self.height = Bsize * size
        self.board = [[0] * Bsize for _ in range(Bsize)]
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
                        (self.left + j * self.cell_size, self.top + i * self.cell_size),
                        (self.cell_size, self.cell_size)),
                                     1)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        return (x, y)

    def get_coords(self, cell):
        x = cell[0] * self.cell_size + self.left
        y = cell[1] * self.cell_size + self.top
        return x, y

    def change_margin(self, top, left):
        self.top += top
        self.left += left

    def get_board(self):
        return copy.deepcopy(self.board)


class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name, *group):
        super().__init__(*group)
        global board, tile_size, building_strengths
        self.imagename = image
        self.image = load_image(self.imagename)
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = board.get_coords((x, y))
        self.is_someone_here = False
        self.strength = building_strengths[name]

    def update(self):
        global wood, stone, iron, food
        if self.name == "sawmill":
            wood += 10 / FPS
        elif self.name == "mill":
            food += 15 / FPS
        elif self.name == "cave":
            stone += 10 / FPS
            iron += 5 / FPS


    def checkselect(self, posx, posy):
        im = Image.open(f"data\\{self.imagename}")
        size = im.size
        return posx >= self.rect.x and posx <= self.rect.x + size[0] and posy >= self.rect.y and posy <= self.rect.y \
               + size[1]


class MiniBuilding(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = load_image(image)
        self.name = "MiniBuilding"
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Building_in_process(pygame.sprite.Sprite):
    def __init__(self, x, y, image, building_name, *group):
        super().__init__(*group)
        global board
        self.group = group
        self.building_steps = [load_image(f"BIPs\\BIP{building_name}\\{i}.png") for i in range(1, 5)]
        self.name = "Building_in_process"
        self.building_name = building_name
        self.step_number = 2
        self.timer = 1
        self.end_image = image
        self.image = self.building_steps[self.step_number - 2]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = board.get_coords((x, y))[0], board.get_coords((x, y))[1]
        self.x_cell_coord = x
        self.y_cell_coord = y

    def update(self):
        global FPS, building_time, all_building_sprites, buildings_in_process
        self.timer += 1
        if self.timer / FPS >= building_time[self.building_name] - building_time[self.building_name] / self.step_number:
            self.step_number += 1
            if self.step_number > 5:
                return
            self.image = self.building_steps[self.step_number - 2]
        return True


class Worker(pygame.sprite.Sprite):
    steps1 = [load_image(f"Animations\\Worker\\Right_Walk\\{i}.png") for i in range(4)]
    steps2 = [load_image(f"Animations\\Worker\\Left_Walk\\{i}.png") for i in range(4)]
    steps3 = [load_image(f"Animations\\Worker\\Up_Walk\\{i}.png") for i in range(4)]
    steps4 = [load_image(f"Animations\\Worker\\Down_Walk\\{i}.png") for i in range(4)]

    def __init__(self, x, y, *group):
        super().__init__(*group)
        global board, tile_size
        self.image = Worker.steps3[0]
        self.human_board = board
        self.imagename = f"Animations\\Worker\\Up_Walk\\1.png"
        self.selected = False
        self.rotation = 'Up_Walk'
        self.can_go = False

        self.rect = self.image.get_rect()
        self.rect.x = board.get_coords((x, 0))[0] + tile_size * 0.5
        #        self.rect.y = randrange(height - self.rect[3])
        self.rect.y = board.get_coords((0, y))[1] + tile_size * 0.5
        self.cell_posx = x
        self.cell_posy = y
        self.order_list = [1, 2, 3, 4]

    def update(self):
        global tile_size, xCam, yCam
        if self.can_go:
            if self.rotation == "Right_Walk":
                try:
                    self.steps1.index(self.image)
                except Exception:
                    self.image = Worker.steps1[0]
                if Speed // FPS + self.rect.x >= tile_size * self.cell_posx + tile_size // 2 + xCam:
                    self.rect.x = tile_size * self.cell_posx + tile_size // 2 + xCam
                    self.cell_posx += 1
                    self.direction()
                self.rect = self.rect.move(Speed // FPS, 0)
                self.image = self.steps1[(self.steps1.index(self.image) + 1) % 4]
                self.imagename = f"Animations\\Worker\\Right_Walk\\{(self.steps1.index(self.image))}.png"
            elif self.rotation == "Left_Walk":
                try:
                    self.steps2.index(self.image)
                except Exception:
                    self.image = Worker.steps2[0]
                if Speed // FPS + self.rect.x <= tile_size * self.cell_posx - tile_size // 2 + xCam:
                    self.rect.x = tile_size * self.cell_posx - tile_size // 2 + xCam
                    self.cell_posx -= 1
                    self.direction()
                self.rect = self.rect.move(-Speed // FPS, 0)
                self.imagename = f"Animations\\Worker\\Left_Walk\\{(self.steps2.index(self.image))}.png"
                self.image = self.steps2[(self.steps2.index(self.image) + 1) % 4]
            elif self.rotation == "Up_Walk":
                try:
                    self.steps3.index(self.image)
                except Exception:
                    self.image = Worker.steps3[0]
                if Speed // FPS + self.rect.y <= tile_size * self.cell_posy - tile_size // 2 + yCam:
                    self.rect.y = tile_size * self.cell_posy - tile_size // 2 + yCam
                    self.cell_posy -= 1
                    self.direction()
                self.rect = self.rect.move(0, -Speed // FPS)
                self.imagename = f"Animations\\Worker\\Up_Walk\\{(self.steps3.index(self.image))}.png"
                self.image = self.steps3[(self.steps3.index(self.image) + 1) % 4]
            elif self.rotation == "Down_Walk":
                try:
                    self.steps4.index(self.image)
                except Exception:
                    self.image = Worker.steps4[0]
                if Speed // FPS + self.rect.y >= tile_size * self.cell_posy + tile_size // 2 + yCam:
                    self.rect.y = tile_size * self.cell_posy + tile_size // 2 + yCam
                    self.cell_posy += 1
                    self.direction()
                self.rect = self.rect.move(0, Speed // FPS)
                self.imagename = f"Animations\\Worker\\Down_Walk\\{(self.steps4.index(self.image))}.png"
                self.image = self.steps4[(self.steps4.index(self.image) + 1) % 4]

    def delselect(self):
        self.selected = False

    def set_board(self, x, y):  # 1 0
        global board
        self.a = 0
        x = board.get_cell((x, y))[0]
        y = board.get_cell((x, y))[1]
        self.human_board = board.get_board()
        wave_board = self.to_wave_board(x, y, self.human_board)
        self.human_board = wave_board

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

    def checkselect(self, posx, posy):
        im = Image.open(f"data\\{self.imagename}")
        size = im.size
        return posx >= self.rect.x and posx <= self.rect.x + size[0] and posy >= self.rect.y and posy <= self.rect.y \
               + size[1]

    def select(self):
        self.selected = True

    def selected(self):
        return self.selected

    def set_rotation(self, x):
        self.rotation = x

    def can_go_true(self):
        self.can_go = True

    def direction(self):
        if self.human_board[self.cell_posy][self.cell_posx] == 1:
            self.can_go = False
        for el in self.order_list:
            if el == 1:
                try:
                    if self.human_board[self.cell_posy][self.cell_posx + 1] < self.human_board[self.cell_posy][
                        self.cell_posx] and self.human_board[self.cell_posy][self.cell_posx + 1] > 0:
                        self.rotation = "Right_Walk"
                        self.order_list.remove(1)
                        self.order_list.append(1)
                        break
                except Exception:
                    pass
            if el == 2:
                try:
                    if self.human_board[self.cell_posy][self.cell_posx - 1] < self.human_board[self.cell_posy][
                        self.cell_posx] and self.human_board[self.cell_posy][self.cell_posx - 1] > 0:
                        self.rotation = "Left_Walk"
                        self.order_list.remove(2)
                        self.order_list.append(2)
                        break
                except Exception:
                    pass
            if el == 3:
                try:
                    if self.human_board[self.cell_posy - 1][self.cell_posx] < self.human_board[self.cell_posy][
                        self.cell_posx] and self.human_board[self.cell_posy - 1][self.cell_posx] > 0:
                        self.rotation = "Up_Walk"
                        self.order_list.remove(3)
                        self.order_list.append(3)
                        break
                except Exception:
                    pass
            if el == 4:
                try:
                    if self.human_board[self.cell_posy + 1][self.cell_posx] < self.human_board[self.cell_posy][
                        self.cell_posx] and self.human_board[self.cell_posy + 1][self.cell_posx] > 0:
                        self.rotation = "Down_Walk"
                        self.order_list.remove(4)
                        self.order_list.append(4)
                        break
                except Exception:
                    pass


board = Board(width // tile_size, height // tile_size, tile_size)


def main():
    global xCam, yCam, kCam, reset_build_menu, all_sprites, all_human_sprites, all_buildings, all_buttons, \
        build_board, mini_buildings, buildng_name_right_now, building_mode, building_strengths, \
        all_texts, townHallTexts, show_townhall_menu, houseMenuBackgrounds, stone, wood, food, iron

    map = load_pygame(f'maps/some1.tmx')
    pygame.mouse.set_visible(False)

    StandardFont1 = pygame.font.Font(None, 20)
    StandardFont2 = pygame.font.Font(None, 30)
    StandardFont3 = pygame.font.Font(None, 40)

    endGame = pygame.sprite.Sprite()
    endGame.image = load_image("gameover.png")
    endGame.rect = endGame.image.get_rect()
    endGame.rect.x, endGame.rect.y = -1250, 0
    eg_x = -1250
    eg_y = 0
    eg = pygame.sprite.Group()
    eg.add(endGame)

    startGame = pygame.sprite.Sprite()
    startGame.image = load_image("gamestart.png")
    startGame.rect = endGame.image.get_rect()
    startGame.rect.x, startGame.rect.y = -1250, 0
    sg_x = -1250
    sg_y = 0
    sg = pygame.sprite.Group()
    sg.add(startGame)

    build_board_background = pygame.sprite.Sprite()
    build_board_background.image = load_image("build_board_background.png")
    build_board_background.rect = build_board_background.image.get_rect()
    build_board_background.rect.x, build_board_background.rect.y = 0, 800
    build_board.add(build_board_background)

    pygame.mixer.init()
    pygame.mixer.set_reserved(0)
    game_music = pygame.mixer.Sound("data\\DSG.mp3")  # !!!
    pygame.mixer.Channel(0).play(game_music, -1)

    mouse = pygame.sprite.Sprite()
    mouse.image = load_image("arrow.png")
    mouse.rect = mouse.image.get_rect()

    houseMenuBackground = pygame.sprite.Sprite()
    houseMenuBackground.image = load_image("HouseMenuBackground.png")
    houseMenuBackground.rect = houseMenuBackground.image.get_rect()
    houseMenuBackground.rect.x, houseMenuBackground.rect.y = 1200, 0
    houseMenuBackgrounds.add(houseMenuBackground)
    resourse_texts = []

    woodText = StandardFont1.render(f'Дерево: {int(wood)}', True, (0, 0, 0))
    resourse_texts.append(woodText)

    stoneText = StandardFont1.render(f'Камень: {int(stone)}', True, (0, 0, 0))
    resourse_texts.append(stoneText)

    foodText = StandardFont1.render(f'Еда: {int(food)}', True, (0, 0, 0))
    resourse_texts.append(foodText)

    ironText = StandardFont1.render(f'Железо: {int(iron)}', True, (0, 0, 0))
    resourse_texts.append(ironText)

    townHallStrengthText = StandardFont1.render(f'Прочность: {building_strengths["townhall"]}', True, (0, 0, 0))
    all_texts.append(townHallStrengthText)
    townHallTexts.append(townHallStrengthText)

    townHallWorkerCost = StandardFont1.render(f'Стоимость: 50 ед. еды', True, (0, 0, 0))
    all_texts.append(townHallWorkerCost)
    townHallTexts.append(townHallWorkerCost)


    townHallWorkerIn = StandardFont1.render('В здании есть человек', True, (0, 0, 0))
    all_texts.append(townHallWorkerIn)


    townHallWorkerOut = StandardFont1.render('В здании нет людей', True, (0, 0, 0))
    all_texts.append(townHallWorkerOut)

    townHallWorkerAmount = StandardFont1.render(f'В вашем поселении {numb_of_workers} человек', True, (0, 0, 0))
    all_texts.append(townHallWorkerAmount)
    townHallTexts.append(townHallWorkerAmount)

    w1 = Worker(10, 10, all_sprites)
    w2 = Worker(10, 15, all_sprites)
    all_human_sprites.add(w1)
    all_human_sprites.add(w2)
    build_button = Build_button(width - 100, height - 100, "build_button.png", all_buttons)
    all_sprites.add(Building(45, 47, "TownHall.png", "townhall", all_buildings))
    add_building_to_board(45, 47, 'townhall')
    for i in range(50, 1100, 180):
        bhb = Build_house_button(i, 800, "Build_house_button.png", f"{i // 180}.png", all_buttons)
        build_board.add(bhb)
        all_buttons.add(bhb)
        image = load_image(f"MiniBuildings\\{(i) // 180}.png")
        rect = image.get_rect()
        building = MiniBuilding(i + 70 - rect[2] // 2, 800, f"MiniBuildings\\{(i) // 180}.png", build_board)
        build_board.add(building)
        mini_buildings.add(building)
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
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == add_Worker:
                        if food > 50:
                            w = Worker(48, 51, all_sprites)
                            all_human_sprites.add(w)
            manager.process_events(event)
            if event.type == pygame.MOUSEMOTION:
                mouse.rect.x = event.pos[0]
                mouse.rect.y = event.pos[1]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] < 1000:
                        add_Worker.visible = False
                        show_townhall_menu = False
                        exit_from_building.visible = False
                    if reset_build_menu:
                        build_button.activate(build_board)
                        reset_build_menu = False
                        mouse.image = load_image("arrow.png")
                    for button in all_buttons:
                        if building_mode and button.name == "Build_house_button" and buildng_name_right_now == button.buildingName:
                            if can_build(board.get_cell((event.pos[0], event.pos[1]))[0],
                                         board.get_cell((event.pos[0], event.pos[1]))[1], buildng_name_right_now):
                                need_resources = building_costs[button.buildingName]
                                stone -= need_resources[0]
                                wood -= need_resources[1]
                                food -= need_resources[2]
                                iron -= need_resources[3]
                                bip = Building_in_process(board.get_cell((event.pos[0], event.pos[1]))[0],
                                                    board.get_cell((event.pos[0], event.pos[1]))[1],
                                                    f"{button.buildingName}.png",
                                                    button.buildingName, buildings_in_process)
                                add_building_to_board(board.get_cell((event.pos[0], event.pos[1]))[0],
                                                    board.get_cell((event.pos[0], event.pos[1]))[1],
                                                    button.buildingName)
                                all_sprites.add(bip)
                            building_mode = False
                        elif button.checkselect(event.pos[0], event.pos[1]):
                            if button.name == "Build_button":
                                button.activate(build_board)
                            elif button.name == "Build_house_button":
                                button.activate(build_button, mouse, build_board)
                                buildng_name_right_now = button.buildingName
                    for sprite in all_human_sprites:
                        if sprite.checkselect(event.pos[0], event.pos[1]):
                            sprite.select()
                            continue
                        sprite.delselect()
                    for sprite in all_buildings:
                        if sprite.checkselect(event.pos[0], event.pos[1]):
                            if sprite.name == 'townhall':
                                add_Worker.visible = True
                                show_townhall_menu = True
                                exit_from_building.visible = True


                if event.button == 3:
                    for sprite in all_human_sprites:
                        if sprite.selected:
                            coords = board.get_cell((event.pos[0], event.pos[1]))
                            if board.get_board()[coords[1]][coords[0]] < 0:
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
        all_buildings.update()
        for x in range(100):
            for y in range(100):
                image = map.get_tile_image(x, y, 0)
                screen.blit(image, (int(tile_size * kCam * x + xCam), int(tile_size * kCam * y + yCam)))
        if board_render:
            board.render(screen)
        for el in buildings_in_process:
            if not el.update():
                all_sprites.add(
                    Building(el.x_cell_coord, el.y_cell_coord, el.end_image, el.building_name, all_buildings))
                el.kill()
        buildings_in_process.draw(screen)
        all_buildings.draw(screen)
        all_sprites.draw(screen)
        all_human_sprites.update()
        if show_townhall_menu:
            houseMenuBackground.rect.x, houseMenuBackground.rect.y = 1000, 0
            houseMenuBackgrounds.draw(screen)
            for el in townHallTexts:
                screen.blit(el, (1005, 50 * townHallTexts.index(el)))

        resourse_texts = []

        woodText = StandardFont1.render(f'Дерево: {int(wood)}', True, (0, 0, 0))
        resourse_texts.append(woodText)

        stoneText = StandardFont1.render(f'Камень: {int(stone)}', True, (0, 0, 0))
        resourse_texts.append(stoneText)

        foodText = StandardFont1.render(f'Еда: {int(food)}', True, (0, 0, 0))
        resourse_texts.append(foodText)

        ironText = StandardFont1.render(f'Железо: {int(iron)}', True, (0, 0, 0))
        resourse_texts.append(ironText)
        manager.update(clock.tick(FPS))
        manager.draw_ui(screen)
        build_board.draw(screen)
        all_buttons.draw(screen)
        mini_buildings.draw(screen)
        for el in range(len(resourse_texts)):
            screen.blit(resourse_texts[el], (5, 0 + 20 * el))
        screen.blit(mouse.image, mouse.rect)
        clock.tick(FPS)  # переделать смену кадров по таймеру
        if sg_x <= 0:
            while sg_x < 0:
                if sg_x < 0:
                    sg_x += 500 / FPS
                if sg_x > 0:
                    sg_x = 0
                startGame.rect.x = sg_x
                startGame.rect.y = sg_y
                sg.draw(screen)
                clock.tick(FPS)
                pygame.display.flip()
        if townhall_strength <= 0:
            while eg_x < 0:
                if eg_x < 0:
                    eg_x += 200 / FPS
                if eg_x > 0:
                    eg_x = 0
                endGame.rect.x = eg_x
                endGame.rect.y = eg_y
                eg.draw(screen)
                clock.tick(FPS)
                pygame.display.flip()
        eg.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
