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