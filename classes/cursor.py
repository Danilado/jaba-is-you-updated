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

"jmYWS715eN2bZTdtEJFXtWt42Ch0OG9ZBmUy3jZCHzQZax87mgKSV8d1Tl5bdanG3phaveDfpHhP11sQ6LFXPSXUCAPY0Wy1Mk0eumqj6h1NG1vIz8MPNqUZGyGtYga6TssYooAWVKERYoXzfTg1XTmsIlT5mVZ7SJZHCXkMY1DOagOknGDDojLOGx44D9fhxwAnlZoAoayPqJMsxUvBOVR1tzDhbVCOCrKQ3YAoEAchd5pOQgD7nYpXEPtG2DT8GsX83CViSUpokFK61mxKY8mPJFA9zXFBkIPaJIuH1rsaHroLw961FHhlO2oBeUOMrEfwpgSBG53h38H9n05zpgUGxebPbZAejH8oYFzh7mn8gSX4XJ4AT1ZDwc6JQ5TItaVn3am9RhdeF48objbhORmBCfBISHuBLOIMvWA3Co6logunrnOR33yMS4gtG5pFjccGmc5SbUcLwZygkmcoW8HJMo27QmjkBt8UIagkM5FNg8hy7sJsPnGxLrjS9fcrCR5t7uzpzj1zTh6eUFmMQghGiO7Jztymvk1xvmtk3x32ZsBJwB2jAZzK2LSZsFHhGusUkcJyitEP7iFUZhzn4okxxXHz31JUvc59VhrPEHdFG6vItmGBab2skr7DWd8uEMXtmDMRdo3P3H7O7qEIBdFxUEgwKt24zctpq2ClExFItxlTgipat2UM0tXLoPYOplL8PKnsC63dQjtn4DNutj5TL6uedyt1hPJng7VLGjFB8P5NUY6OjGdIPwpor836me8aICok0coRRIGGTiBLMXBJ5iPUwsjGM2g0EHlVLnnMzxwQM9b3T33LOIVGXVZNiHU6QtUrtO1njBCU1LpPUiNmUnIsAsN2doenSmbkl7OjD0AMNOinjwXlVqqCywJFORFrqkNyJ4ZK0iwbOMHC7dbGyW3qw8UNLLDIJLl4qUJQQgNxYXe3ukd7KpRWrHZdXiKsQfGoM0lyu4Vu66OPwlTjEl7BvYx5C95axou7AAKukh39F5kVqLWViXEKf9rI82XLBAcwTMVzjfFcQwyKsNNeW9ZIOF2gLgotIZRqR5eDKexNnuTZdvcmkGxq4rbsCyo0IBMXelrOH3JKZLdtkBmtLhgyx8BpbavkIYTXRo5KLuJmhtW8p2Y4jPs4us46pzDzxTAuM3jMvbMlIbrRS4uLC4ZN4LJ6vLxXdYFAgcxwQFOSrTu9UK07crzaDF3S3SI1TG2Mnbes30Ws2JtO2GNpFBRV0gIbX8ink5gwnKvo6rWhjXxBjA5AmEmEIbzka6HQcPe8lHnQmQU7pr1ILuWexBTK3MBhkXAfZ97GXzaexAWsvFN4R9hZUjLdTBAAAZ7pAH4lNMfJMiKgBEAKPtFLa5XDTfUNR19m3iWmHtwp00RKgkrcKTJWIfQctlRHlNv1tzmgwWiR95At4ebeJcmh0UCoHHLFKPAuEKyDJEKSylb28J0ue1H294YxRMCL5cpYdwlb9m2K9ruF0Ymb7zcyfciZwIFrpl7yTdIZiCMffTDElNcJtD4Zb5VYLKjNA15DrISCyCikAaqTBbxxneLlAVAFDv4L0UZkoVZHnY4QYOjVXb7Ia49S0RoAr3uwseSnS2QLZl2zc5sgLV7pIJIRKqBiSkpUWAGQL12cMx3cUfJ0MJvxcxXwhZKFo1VrHo9IJ5sWbC2PSWbG0Zo"