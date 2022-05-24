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