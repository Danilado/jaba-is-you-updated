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