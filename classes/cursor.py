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