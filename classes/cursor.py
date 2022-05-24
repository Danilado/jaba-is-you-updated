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