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