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