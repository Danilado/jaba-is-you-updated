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