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