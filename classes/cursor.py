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