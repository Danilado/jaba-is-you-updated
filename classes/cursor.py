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