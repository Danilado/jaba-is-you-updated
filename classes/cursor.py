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