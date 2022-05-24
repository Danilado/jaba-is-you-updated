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

"WjgoryJaFqMw4NQ7bYSNoeiiQ9SEmnMjUbnZCbYoVHgJtnrTVvUKHK3vYy7Mox4Bt6zi4hZ4lnf3PymE2gm8L8OI4Mj9ApPpjShNw9H1M8mz5hpFHXoLNtK2gTEiSgqCNxeoIktOh4Y1gclvw8WtFNEP0JCrnjx2nBFOfmunHzRtwlaaz4zC8277ImyWQYz4lGeEYq8z2OS7xCEO3dIMvx1jf4aOWmPhk92zHgsiSINpuZa2gYz5IrWF5YFwjr2SE4Ut0a1viSt749OA9bFRwwlIDR7rPw3iyP7il6ypZaKvrULnSEPogHmM2UI3WCZlRbFcHylXTvWv8zp9bfG6VM96vaPtAphFlonWBom18O7sxtfIrV9Dcb36qOm5Dc4PKHNzRJFeHfOw3fmJUbjaextfdssFOmUzUT4S1y8OfRGFizna3JIF6S4zs0VJNGJT8afwxphCXDs5HzH7Z1uY8cqrI9SILfrKNuDC8Ue59o197M0u7HWY6j02orDoDl7KOS8qUxRneV6SMYFYQv3QpEvCn3E56hqcjVh1ksWVxcjYKMTwTpNH8VMGsnt2FIkU5e9SxMa8ZRiDK6OogvV3qJH0tN7fBke9GpJ5q6YQ6qG1D9ST9Fo76PICZxnnuwXcfbYlCJ8IBKpap1NOyQUzew50sEXpDnhGKPsXwvLYLCJdATd8HQaBqZZ3va5eiTnsIBvlDEdOKzX55QmQEzKJM2coxSKDsJrZlqcDE26ur0DTUFQWOwiZsULZ3w5CVb4pjTySZatrPz4tcAZKMHfInxxIpvGrI5uZ7OD5CZWEo3d3kCuT2rR3hefSweygj7v2gkh6dyJCXujlWTNuuxmHENzJuVNmFHx1C6lr8DKoUqYDemUiEygnqBiTaWLVbgLY25Wm9fwwdDmzyaiw7tsBHU0ZOt95ze6fBUN8ZAKydzMNpHzqZd4NtQVkY6CujA4ifLrOyVBc2shOYQfsv7p2vJ3JFlGLyQfr7xCFhN5qO0H2YO5FJA0bJHiBgNjd6znaEH17ZHXIOkohMj6a3VelvgxH8kt8NQWGgraax0FBWceOcjXXoRvzPIjEywErMyRofFbI1udNY7htvVRxDTKqSwBmNmbRlqr79QcPpsqq8OJbVsGDKU9gN6YTaPeoUx6UWC9Kh0kUGje3KgeCfDLGugGolXxSezBxlNjlsYRwdTXIy0xMDjN456u6nu3RkLarPtuSSh8fB1WyjV1ag888SaDSpsDwZKkFtU06IspbWLxzTfTeAe6XUalobK5cDAdS18gFrweUzaPwa4LiQptq85K6a4aTZwwAuxqPGNtxfBKsAxudHnFWBQGzzmGIR5DkN54QU0bEnTjAdlF3VoyPnVb4olfi1AypMDsq8TS2vR0FJfKiQLP3PzoHR0QBRzqxIDzp3SjgH3ruazzpt6Tm2XB4zKiIIdZFMqyUFzAhLpGc6y7Z7xv0uhpdDeTpobLxsIDib1i74p5IuYxcoluzXjFgen7Ftc1PujbMJvbjspmc1izQhy3V2l7mzrIceNCdoFUhz2u6R4iW4IXYLwaB2AueAm17GAuagUlCP3HyfHFREPiHwQwP1oXkZAz4fDbRcafrC6hPKoLbqF15I3BxzmtoJMtvLnCB4WtqVBGpZF9oHEjGdcZJhuwXoaj8R5HlPKwxLJAfFCor33hwJ9CguaqTtUOr5XBD0G6YdnZrkdhH6C0hPFtned8ltss3cPjBRkEDHLm15aZNaELqNjlxcXRhdXOTKOopYmwbNkFbcMk9Az3OHgCIqZsOlPnErcjS1CELTC0mqNkrCCG7FPpsQwj8P4dkWk"