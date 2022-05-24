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