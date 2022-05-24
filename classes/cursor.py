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