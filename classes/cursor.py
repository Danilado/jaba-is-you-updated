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