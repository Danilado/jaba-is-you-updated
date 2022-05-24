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