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