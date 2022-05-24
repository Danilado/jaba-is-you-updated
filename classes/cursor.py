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