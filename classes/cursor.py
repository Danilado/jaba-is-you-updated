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