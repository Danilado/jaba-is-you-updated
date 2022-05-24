from typing import List

import pygame

from classes.objects import Object
from utils import get_pressed_direction


class MoveCursor:
    def __init__(self):
        self.turning_side = -1
        self.levels = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        self.reference_point = ('moon', 'skull', 'pillar', 'pumpkin', 'flower',
                                'spike', 'jelly', 'dot', 'leaf', 'tree', 'blossom')
        self.some_obj = ('line', 'square')
        self.blocks = (*self.levels, *self.reference_point)
        self.last_time = 0

    def move(self, matrix: List[List[List[Object]]]):
        # TODO by quswadress: split move_right, move_left, move_up, move_down into this method.
        if pygame.time.get_ticks() - self.last_time > 75:
            self.last_time = pygame.time.get_ticks()
            for i, line in enumerate(matrix):
                for j, cell in enumerate(line):
                    for k, element in enumerate(cell):
                        element.x = j
                        element.y = i
                        element.movement.start_x_pixel = element.xpx
                        element.movement.start_y_pixel = element.ypx
                        element.movement.x_pixel_delta = element.movement.y_pixel_delta = 0
            if self.turning_side == 0:
                self.move_right(matrix)
            if self.turning_side == 1:
                self.move_up(matrix)
            if self.turning_side == 2:
                self.move_left(matrix)
            if self.turning_side == 3:
                self.move_down(matrix)

    def move_up(self, matrix: List[List[List[Object]]]):
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and i > 0 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i - 1][j]) != 0 and matrix[i - 1][j][0].name.split("_")[0] != 'gate' and\
                            (matrix[i - 1][j][0].name.split("_")[0] in self.some_obj or
                             matrix[i - 1][j][-1].name.split("_")[0] in self.blocks or
                             matrix[i - 1][j][-1].name.split("_")[-1] == 'teeth'):
                        matrix[i - 1][j].append(element)
                        matrix[i - 1][j][-1].movement.start_x_pixel, matrix[i - 1][j][-1].movement.start_y_pixel = \
                            matrix[i - 1][j][-1].xpx, matrix[i - 1][j][-1].ypx
                        matrix[i - 1][j][-1].y -= 1
                        matrix[i - 1][j][-1].animation.position = (matrix[i - 1][j][-1].xpx, matrix[i - 1][j][-1].ypx)
                        matrix[i - 1][j][-1].movement.x_pixel_delta, matrix[i - 1][j][-1].movement.y_pixel_delta = \
                            matrix[i - 1][j][-1].xpx - matrix[i - 1][j][-1].movement.start_x_pixel, \
                            matrix[i - 1][j][-1].ypx - matrix[i - 1][j][-1].movement.start_y_pixel
                        matrix[i - 1][j][-1].movement.rerun(0.05)
                        cell.pop(k)

    def move_down(self, matrix: List[List[List[Object]]]):
        num_el = None
        x = None
        y = None
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and i < 17 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i + 1][j]) != 0 and matrix[i + 1][j][0].name.split("_")[0] != 'gate' and\
                            (matrix[i + 1][j][0].name.split("_")[0] in self.some_obj or
                             matrix[i + 1][j][-1].name.split("_")[0] in self.blocks or
                             matrix[i + 1][j][-1].name.split("_")[-1] == 'teeth'):
                        num_el = k
                        x = i
                        y = j

        if num_el is not None and x is not None and y is not None:
            matrix[x + 1][y].append(matrix[x][y][num_el])
            matrix[x + 1][y][-1].movement.start_x_pixel, matrix[x + 1][y][-1].movement.start_y_pixel = \
                matrix[x + 1][y][-1].xpx, matrix[x + 1][y][-1].ypx
            matrix[x + 1][y][-1].y += 1
            matrix[x + 1][y][-1].animation.position = (matrix[x + 1][y][-1].xpx, matrix[x + 1][y][-1].ypx)
            matrix[x + 1][y][-1].movement.x_pixel_delta, matrix[x + 1][y][-1].movement.y_pixel_delta = \
                matrix[x + 1][y][-1].xpx-matrix[x + 1][y][-1].movement.start_x_pixel, \
                matrix[x + 1][y][-1].ypx-matrix[x + 1][y][-1].movement.start_y_pixel
            matrix[x + 1][y][-1].movement.rerun(0.05)
            matrix[x][y].pop(num_el)

    def move_left(self, matrix: List[List[List[Object]]]):
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and j > 0 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i][j - 1]) != 0 and matrix[i][j - 1][0].name.split("_")[0] != 'gate' and\
                            (matrix[i][j - 1][0].name.split("_")[0] in self.some_obj or
                             matrix[i][j - 1][-1].name.split("_")[0] in self.blocks or
                             matrix[i][j - 1][-1].name.split("_")[-1] == 'teeth'):
                        matrix[i][j - 1].append(element)
                        matrix[i][j - 1][-1].movement.start_x_pixel, matrix[i][j - 1][-1].movement.start_y_pixel = \
                            matrix[i][j - 1][-1].animation.position
                        matrix[i][j - 1][-1].x -= 1
                        matrix[i][j - 1][-1].animation.position = (matrix[i][j - 1][-1].xpx, matrix[i][j - 1][-1].ypx)
                        matrix[i][j - 1][-1].movement.x_pixel_delta, matrix[i][j - 1][-1].movement.y_pixel_delta = \
                            matrix[i][j - 1][-1].xpx-matrix[i][j - 1][-1].movement.start_x_pixel, \
                            matrix[i][j - 1][-1].ypx-matrix[i][j - 1][-1].movement.start_y_pixel
                        matrix[i][j - 1][-1].movement.rerun(0.05)
                        cell.pop(k)

    def move_right(self, matrix: List[List[List[Object]]]):
        num_el = None
        x = None
        y = None

        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and j < 31 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i][j + 1]) != 0 and matrix[i][j + 1][0].name.split("_")[0] != 'gate' and\
                            (matrix[i][j + 1][0].name.split("_")[0] in self.some_obj or
                             matrix[i][j + 1][-1].name.split("_")[0] in self.blocks or
                             matrix[i][j + 1][-1].name.split("_")[-1] == 'teeth'):
                        num_el = k
                        x = i
                        y = j

        if num_el is not None and x is not None and y is not None:
            matrix[x][y + 1].append(matrix[x][y][num_el])
            matrix[x][y + 1][-1].movement.start_x_pixel, matrix[x][y + 1][-1].movement.start_y_pixel = \
                matrix[x][y + 1][-1].animation.position
            matrix[x][y + 1][-1].x += 1
            matrix[x][y + 1][-1].animation.position = matrix[x][y + 1][-1].xpx, matrix[x][y + 1][-1].ypx
            matrix[x][y + 1][-1].movement.x_pixel_delta, matrix[x][y + 1][-1].movement.y_pixel_delta = \
                matrix[x][y + 1][-1].xpx-matrix[x][y + 1][-1].movement.start_x_pixel, \
                matrix[x][y + 1][-1].ypx-matrix[x][y + 1][-1].movement.start_y_pixel
            matrix[x][y + 1][-1].movement.rerun(0.05)
            matrix[x][y].pop(num_el)

    def check_events(self):
        """Метод обработки событий"""
        self.turning_side = get_pressed_direction()

"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"