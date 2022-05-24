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