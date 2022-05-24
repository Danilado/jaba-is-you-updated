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