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