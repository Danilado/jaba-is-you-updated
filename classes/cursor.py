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