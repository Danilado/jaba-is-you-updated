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