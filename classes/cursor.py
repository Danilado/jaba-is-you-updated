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

"ErFA9wPTQfqfmSeyDco2opbtUOxtmvDR56Mmq69CPrt6JUTOrZz0Cwjgt6JZanzFfsS9J7sutEEBELVhu1sH5S5nlxJVZfOAH53oIkeKHCWh6iDQ4fI2b7oSnljunLeGXybXaBdfbCYAEuwclHnCRQRltVa2AwrHdnHr8YvYtB3OqVNTW7scOIPMLlwcW0skVJEU2sMOhxA42irSe5FaVUL7EuYQTUySWmkdW6SEILVtOEf1UdwkPf5qzuZquGa9ICzqnrTpwalLRaBFJ27roFa9lFtQdoLplU4bHjJcgJcM3FqJYAzxnTqV1WjZDSuZOiRoeprlWpNNy0jBh4KrYqNuyX0osM82UZDlsiPVz12p986pQnSjfBHyPEzKp2wZiF2aEKvIBpJaYzYlmtz1bZrdAD124jp4RBJZnHO62kESQyDgpnDbZERako52YHatNxCAzUaC2j9JNJYmsgLei0LqBNWeQ6cDnN2Gt3RhrfNa1ZdVZa5Wg9fekY7Ks4MJppT4shsXMhLBOOfd4EeI0qj1BsVUVFvmUALIv37RccTI9tkieIebvXYuEOslfruUVwayyoaF6m9TkysZQYYfX5cXEU34R3H7NVSr7dNMWEp6k83qGAhVQxBLupmBrR0PL8w13Sl3d7cGArzhgmYSrPDNoR8MWm14ojlyESy47jVXnkO7SeOZl639geQfGZ0pVN8T8jnOvkKtktPBsG2Sxw30DyVqbNDi4oaFrF4ayzqLWAXalTTWDyViWBce2ozfUNeoWxKkXaFyIFpvmq3dZiUWOMFnmtW1culVak4JmpOqovqKPHxlnN9LyMSMjdDtRTILrLv9utRAXlfemuaMh2Q990esCwWXTneMmZxPb78YGkXkcjdBEQZCmeadsNCC4QIbeZPEDWAOVe4QH2dB2zBeTfXsCQTlTMg17biIMToduMcbeERc3JGoJxbAxn6hs3UCJuBv9WukMNly1pUDLMpvfVOXYXyUoGgYx8tOFwji5m7aUgmJ2hcHeDTaaVMD59QpNmWiwQ47IcEIijAHLEcf39koXqEeVJPvqoVhdI0z6TwiMSIivGEQHKKcuhlgApETzwe5mh27lpyS6xALoECPPDUp5ZjASdctkWsn9i4cTNGmxKCXHtNzeg5Ls7ogAxjkSdaXMVQ90IPVyyz3Xlr41WMmq8ffPK5dFnPXZJJ73WW9cJxxbOPL1CPBIS9xZBPnje4jz1mr6HS3iUf6J316AnETyI08XL5Idln1QzMVNxlYRKd9M5Slxpfp2gsr2VnOdQ3HRbf3c23EaaHrzJgUf2l3Imvtwlnhvuja3dsZs8MuNFJRcM8KNS0ZLWZm1X4QsOIM13PL82oEJdhe8KXcFGoUwDfZXZKPTTCPMmLIroIsTpc0gkWeuhX42iakR7ZiERqxUB9U1qp2GmlJmq9DDtBjLRfKLGC1GOYhFAURwVSowdeSpOcX8QGO1A7VAxq1xjeZiGXIN0TqpRQBgQuMyuTLOXCyChi5WRuVaATNVyrsn0ZZ6iT88jAqKqvtl90VPjMor4uq2ibO53FuB1x03qd9QxFd9o6kd9VH3GmxNHo8vkAEvx0pDww0mPQ6w7fxZFh8C4WVwkCQtNhqbRGV7WaMoSNzPTkzTlZVIKv3l9zNnJ8K1kvGUhXZTwi8zKvPgMsSY4tESysDDZKyFfaIdQrXlnXtJy93bWQN5SJFT6kaJJvqztSQoniYae5VXdxxgfmnjjn6kBcAKgc3QmBP0eCbqNuDoL9FeFllFJRwN9C32uXRWafgabsIB7eT3OEJREAz8VtFiW4XH0EmkZQt7qFOVad1fj3elw1arP2ZWtko706wuRbLkJo6hLDXIpdBGo9M4Dhh09OehQMvCAnmSMvTyKsIAckDqVtDF1ShJ4qHgIMpBkeqnI1sW8aQAxeyJrRA4Y68So75alczD8HiIrAGrVHl2Qti73yczjtxbiTdBdRVHGIVCwQWGETh8MsPMP43"