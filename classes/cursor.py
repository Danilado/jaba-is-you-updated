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