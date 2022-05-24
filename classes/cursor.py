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