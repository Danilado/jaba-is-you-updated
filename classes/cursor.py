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