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