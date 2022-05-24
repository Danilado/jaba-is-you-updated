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