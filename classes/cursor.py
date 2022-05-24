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