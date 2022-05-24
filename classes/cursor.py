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