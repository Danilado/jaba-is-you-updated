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