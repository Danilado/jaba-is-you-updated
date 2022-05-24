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