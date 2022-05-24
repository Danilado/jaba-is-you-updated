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