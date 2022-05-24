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