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