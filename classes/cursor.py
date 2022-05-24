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