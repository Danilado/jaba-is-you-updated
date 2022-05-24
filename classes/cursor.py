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