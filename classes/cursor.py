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