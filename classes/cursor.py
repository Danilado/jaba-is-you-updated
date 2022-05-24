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