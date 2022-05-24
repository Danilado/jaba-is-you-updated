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