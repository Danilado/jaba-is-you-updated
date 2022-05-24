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