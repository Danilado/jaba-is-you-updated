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