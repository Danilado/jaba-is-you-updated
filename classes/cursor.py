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