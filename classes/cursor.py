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