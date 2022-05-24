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