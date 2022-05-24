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