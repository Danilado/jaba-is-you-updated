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