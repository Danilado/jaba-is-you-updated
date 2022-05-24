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