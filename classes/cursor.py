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