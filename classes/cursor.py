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