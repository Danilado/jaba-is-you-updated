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