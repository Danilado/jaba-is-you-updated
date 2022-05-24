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