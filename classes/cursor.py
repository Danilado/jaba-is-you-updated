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