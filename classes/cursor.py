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