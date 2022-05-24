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