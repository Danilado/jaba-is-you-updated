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