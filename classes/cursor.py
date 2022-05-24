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