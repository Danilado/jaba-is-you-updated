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