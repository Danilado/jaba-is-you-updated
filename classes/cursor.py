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