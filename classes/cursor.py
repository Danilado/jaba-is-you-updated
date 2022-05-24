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