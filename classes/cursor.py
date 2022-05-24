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