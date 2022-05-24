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