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