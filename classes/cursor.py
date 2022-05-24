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