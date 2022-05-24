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