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