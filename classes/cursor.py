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