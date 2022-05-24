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