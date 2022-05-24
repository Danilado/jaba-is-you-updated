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