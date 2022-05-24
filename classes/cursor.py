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