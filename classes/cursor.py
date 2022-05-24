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