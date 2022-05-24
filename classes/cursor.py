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