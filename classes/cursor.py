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