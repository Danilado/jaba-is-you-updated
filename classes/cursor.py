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