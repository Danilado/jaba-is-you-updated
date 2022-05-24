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