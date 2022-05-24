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