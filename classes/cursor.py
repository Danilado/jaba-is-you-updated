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