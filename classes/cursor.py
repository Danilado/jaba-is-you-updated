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