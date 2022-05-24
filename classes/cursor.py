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