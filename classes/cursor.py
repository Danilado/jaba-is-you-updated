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