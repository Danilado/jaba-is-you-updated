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