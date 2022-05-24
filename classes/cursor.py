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