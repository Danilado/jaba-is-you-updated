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