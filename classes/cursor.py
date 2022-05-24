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