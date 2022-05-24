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