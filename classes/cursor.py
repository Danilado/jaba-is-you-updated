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

"zouNkUMBcxuBjAOTLZ1eMdfPUZrmwPX0ol7BFYotH99ka85ymYhyau53upTCl5myPg1zGtvmGgCRXyfBRzIIJLUwACOd2QqM6zKTyMhUTkoHl2oCoZ8mgwAVDicSsKIL98jzFSaCgVyZlI8djFbaEhe3oprNx7s3mG6XMpYOz4OqMKGcqQP6rMTM4oG78ZkTvZMA2m023qSJlYhT9GFQB4bCTkbwyWdKZ2Z4iAUKWDTTlKf6c9XV7xq7pjxtaSkO6wIXnej2i95CffkRl2iKlsSJiRzeFt6377xfziMpgDLdLJEjgM8PbczNmiltXDwUrbeX2ieHBnSMjPVoDNyRqEHNdiZeJVL0rAyEOLgV5QZNuhuKLNaFMWxpAlACAYclxVAu2P6Q9hkG0FnesDhboagnRbRo6z5oSNz6EyJyPM3gvzpaIsxyKosBPtbg1XtQK6BMH8IKND7qCSvwg9gWioeGM4fwcZld7RV5JUqvjmtOESVsM71J5zZmoWUqlDIOMzBeLTtlSFloHIQ3912fNhQjzEzhcV3B681h0WtJGy15zexyAuKcKwFYTMBM1MN13EIE5UwMZ4edL2ZzMYDhNB1FkjilFLFLbnzdTkdTj4pHoRgzSLHxCfJHAGREZAH3JhdQZrQPQfwyOulB8tb8ut5ygdLT8yaif7ZjrLo2Mb469fvOGqoYs4VzKpVUYBTJB69j9YuPDFNh0QNCOPX5tMxBkP6PsRMd7YrJrRyOzQAleZHC1A53BQLsXdK7s9o8McX2DP4nOfBbPi1aCdFjBIQo0ngmaOmBLZFror0zYPDNJgCH7huvyO7CoI0rNWKcRRnL1M5i3hLd6mcb1ltUO9lZPRrv84HIPe7VyLyKJBrjjHzlQpLOOFUFfKCLFzmTERjWvo21e2ecCbb4GJrlu58rAREONNdEVcAq8sZbxeJyfB5whNjJJi2kZLyQiEEC8Ojb8xODELUCcGojhaTAUL71vgHb0hRYrJjRsmn8yYo6MHddeMMA5C5ehlGFYbrtpE25bT1LaORKTjf2KFuDyCZF0lTHk1jxCGCRcaXCmVAqGzqfuv8jpGTuMiImE81vGcMUQutKNOHvSAIWCWC8nYhe9wory76CkKeduT1x7IPTIN3lMVwHrIDjTjdiYKQVkFJhj7JTjngldeR933gbUj95cuWdbIKo8iHUnzTt1rQvwVdWFSVK4PmPTtdcQfBPcimfEpRIizmqoV9ejIXvsq8MyXxSbMpRFv7ZCpZQngRBaAeaERZN0Nbd01pmCnknjo6SQyULm6SPsDzLYjCxxrUNMAmZRQDvxqh2L8JTL7wtwwD23WwIHHUTiofR5u4lpmieLqPkhAZ41DPuxQanj1HCrExdmwD9K9M1ektGdlUjNbb7em3qkUBKFDyPbMWoJdt3ZA3P2TqJboj91GLWJTaYtMg2riDWA1wl9WeuE4yCgCg3gYVp9Oba17GbzyG3iBlHjfpJhE3wEtapWYoFVwmJDfa40rrxpruhIs1icNIoX1s5gDpLsZSIx483BT5OhAuf0sD6yJbcBxhtKoyLs8hO6ADgfmSz2JQ9yi1d"