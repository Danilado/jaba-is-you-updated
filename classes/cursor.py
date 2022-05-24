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