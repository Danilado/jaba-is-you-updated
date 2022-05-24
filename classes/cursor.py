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