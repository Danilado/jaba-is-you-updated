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