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