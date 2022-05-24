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