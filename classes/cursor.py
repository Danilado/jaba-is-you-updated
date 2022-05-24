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