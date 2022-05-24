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