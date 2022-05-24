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