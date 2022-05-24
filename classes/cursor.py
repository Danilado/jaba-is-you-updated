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