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