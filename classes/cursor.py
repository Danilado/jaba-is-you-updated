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