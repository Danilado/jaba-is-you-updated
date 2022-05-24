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