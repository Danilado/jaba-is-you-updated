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