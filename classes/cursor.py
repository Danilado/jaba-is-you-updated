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