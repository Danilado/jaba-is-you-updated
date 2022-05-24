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