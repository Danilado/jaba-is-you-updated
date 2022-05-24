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

"GsQOTSLB6tslxV8KI7U6jAY3Te0KoqclPOkgJypbEYQz249BCEq9HtHFNOmq5aB6clDd1NDUWgDdXHdbksKdWCbtMSFKQEzODW6LSVwfaFV4cx7hvF6xOTfNLuYQW0ZWptDYsolg1ee8mHwYQIFscnM1Q4vCeIHTCTIAE52UVoEGJtsgMFOPYelygmBFyZ0KoQisfdbEDr8Dw7UQ2nXUfsXO0iImkkpstLnNhe3dMF3li9gHnU0mI1Rl8IHwXpjtFGhbTbAYAqr60tot8r5kVJa6ebhGCt0fl2J5nD9AEWIMRtsenacGiTltdJMTRuH1IAXNMRtmKKLYEbOJLQDkqqAhQOjFw8SGha3QhqtqtT8tXd32C0amtZasW40hnz1H0e2pkslTN1bQ4cLYjpCLiELulsczEMZdkIGBUDkI4SmqqtBdht9kBRl2Qvxx6Q13Y1ZHfifa40uWfNLMOVm9V372c54Qi4cfDqk4D5i2knHOmWB0uEEjPS6yBtPexFG4DIwEwbgi9thFdJyKxb3pnyQwzAdz1hsCO6SFVkgDl1RVtx5xeeuqFbLWDjV4LYUfB0DYYwXGEWaVYWvE6vhaiDYjsCfxr6kyxObO4EkaQLyJfI4jKszEn3UXnCweLF4fiN4fu4EfTg2jhfMABxzlj4SVTMuJKz6tAtJ2xCOa8KmF0NSDzN6tC08h6Z9yMeVDlszz2kRnYM4mqFE0bJqDYzAV97hUlczTQ6NbbYnVLtE17Y6F3uS1Imb42mihwisuS6xRVMaQ2fibWfai5jCTDk8qyYxNh52mMiEIAAPH8sIEk0H8uoNj8neuiDOAhGeMKWY2SPNyRzVAFcqU9UeXbYW8SmGTwPSNctWjJbUijcG5EdOPMK1TWzRslRwpbywfh9eqvL0jaNCA10LuF59yqAhDr6vjGVQUBI45QNQ5Mjn3fsza9PoGYnjgJPdoCic5NEhRx6UxNsSW0D1fXd4r9N8veoZcXDjT5gtUhKT6t6tg6v9rXzcVnRfO5RChdnLSrSD8hwhHrMUEHxfcpD2YZPo0F0pGzld4SGgHwfX86xb3oQ2XHKF2n24ab1K7dMl7I3dFgYnV1UyK6dj7pvIK5GRs27cRwKQ7u1gs7k0yIUGX86e7AJIeBaaLqv15n2Htus1J9W8oemnh2vnYzRBRagqpusN8q5RVjh8RP54IhOQalx3bq1qPdEfaMwC0afVar0afnwltdDejHcnwzDaU9n7dlf3lQl8XVcGJjdyW82AtxKm92rCUpJInfXVK6nw9dbA66XfN3bzSrVKpWvgCTSSHGS4q4ILoFQUh767zHrYhdXyb0o4aOQxONt3dd9KJDerrKEVVPMGxDmbRlJsy4HHHr8U1XU0GWDqd3m0yDj6jhJTv8LpmhViyX6JmsXl8gbmlQSNdvBD5tvCjCdDYNB3F5m6ccwnxIY1ZOZAMlUWBMzY6dqNp3o4lHQ5uJDM8dmw74Tmhgte01MFj4CmamMSGHduneckgynSIlgykDYREx7OGVFQMfaWNG9c12mj3u0r158W8A3EVwMewxzRyBModv4NieoHGYzVrZWSRG9BDMbvViVNW9xv0UobZJ3GNVDOAEsPfOIHvopoRnXxAAjhcNmfHP4k6tq1mxmwOMI2vc1oqc161CHzfl6CtTjBgOyjdwuMddJfcXhFg7wZP7Z1jBM3D3pZ2x1fpogi"