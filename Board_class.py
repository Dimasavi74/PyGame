import pygame
import copy


class Board:
    def __init__(self, size, Bsize, top=0, left=0):
        self.width = Bsize * size
        self.height = Bsize * size
        if Bsize % 2 != 0:
            Bsize -= 1
        # поле имеет всегда нечётное количество ячеек
        self.board = self.pole(Bsize)
        self.left = left
        self.top = top
        self.cell_size = size

    def pole(self, val):
        a = val // 2
        # отмечаю тройками ратушу по середине с размером 3 на 3
        return [[0] * (a - 1) + [-3] * 3 + [0] * (a - 1) if a + 2 > _ > a - 2 else [0] * val for _ in range(val)]

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
                        (self.cell_size, self.cell_size)), 1)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if self.width > x > -1 and self.height > y > -1:
            return x, y

    def get_coords(self, cell, sizes):
        x = cell[0] * self.cell_size + self.left + self.set_centre(sizes[0])
        y = cell[1] * self.cell_size + self.top + self.set_centre(sizes[1])
        return x, y

    def set_centre(self, size):
        if self.cell_size >= size:
            return (self.cell_size - size) // 2
        return -((size - self.cell_size) + 2)

    def change_margin(self, top, left):
        self.top += top
        self.left += left

    def get_board(self):
        return copy.deepcopy(self.board)