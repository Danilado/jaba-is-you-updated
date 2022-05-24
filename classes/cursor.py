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