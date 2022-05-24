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