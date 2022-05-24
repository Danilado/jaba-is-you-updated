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