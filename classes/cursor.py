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