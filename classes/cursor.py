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