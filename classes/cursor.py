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

"W7c0V5Lv7VG29wVVWS936ZynfS3yb5Oe0Fp2gNJsBpYYN60BKT0IBKLY3JeVOSQ294mtmNmLPdgfQXbFDESeamTVF8gFmouq1zX8qkaoEKMOCaePTneJvE2m3fn4MtFAyGbMFcJlssUne8HI5PSq5puIqWT2MM4AE2TGEZEtLJu9x6eE6mJLZRBvwFLB8IKLxVAlIm6ZjuOmQMLNaOgptu2YC4eZoI5GDtvwF6giYQje18gXrAvjDP17kwz50zLDpkiHUs3MKxktxzwjYstVXp5Guek035yG7BGnrHJhRwBLlfWp1DHIdlqugLBj37lxdjn0JaV0giQ9bOSsiYIJSXkMpgofHiILUuLTxdc8cUXBAn0lVjbL2pXSTVKiCvzkYVDWpeMWFq9HGbrRzC8dQ2iqE8dVeH4M77B9DvCmKpfFn8SfJL2K2FDLCWSTcEsNhCkUiwjmEHAnN9KJAGe305QWCSaISrnqPA8rE6s5tCPRAJSdy9YXa38soNHoAincKtbW1bKF7UzvI3uMAoCBAamyrIOdKK8YdgahXUuZ8jEU209mF5vwtKjQENzO2WBwa04e41Ir23bgwVEJxmOj771etlwBwZMZG1PWZ3NINPRX81FhwMYUYKopMvqqpv2wyHS3nNMQEh2NFD6gIUSSJlbfvq5OGTrObKOvV0egVP9TvrXFitTYDxx6p9zuptxcxWZxCVJBusXSYh9Y7f2sF8DDnW439sqMooy2P7LVDUe1MMEbrzZbWOjPrH0wOx8ZLyT18235hIsrHynM7XHO9c2mKCtCvzb8KfUzC0hi9hQgylzlAveeIOKxVFIpng0yvStXIiMZsIjMAjY8lPCsuF2AsxpTYvgyVBt6xpqb9vnRsZFuT8wqwND5HFVioU6SskJPt5nqhIvj6qcscmElACFV4vXQlTJ14W0EqnpAbBXD8kSDxFKLOhNLfwuWd3jBq40D2l52oN0AiYXmv3lBgE5u2jO1ZY8TMmVN6bHQYTUnoswyuYmpUyP7n3Hl16pZzr0n4r7PMftfIzKfRTZwLBJpjiBhDZ6vZIfA0d4YgWlq7q091gKHKIAOBLooVVM55c96aVB4bOEBRaSqsQlwlcpVzp7hcK3qrrOIQ7eF4eMAj1WKKq43UruQFH8DdsBDhA1DfDzdVTy8O9vInzdhKXpzyp7o2S90tc6Auhw1OllOcOMAt5b2GyzBciKMghlqhR0BpZ18DJ1CurEnGrTN3nAiYJHtamhtznOCRLBTwSuBE87OAc46ltbamRNgORNIbq1yHLWSuNP5cyg5iKfyg4pXBYSZpzWscIigGYdqnmaPM6bFl852XD8TeaM2JPzTSy2aS1Erug1H7MDdKNAUfw8C78RQH8nCAWT55kXq8kUmyN8SmCrSLkstvXxCOhrY4m8snTibL8miOCfcCuaIL8Uj3eQrWzlyrkX6eL0t0zWzeTjvGGCJvsHHo53XhVUMe8mqqoueROM2kFCiJN5XR3y9UrsiihQuclbLw3ZXwfAcxS5T1A6tWpSYC6aPjuPyurBGATC3PEhN9LasSWGdohuNPIcqCPw87cqSP7B7LMcm1Q8DpY5YR9BPy80qyqMiYn6CbUv9n0NERGHaBfzOmU0qpRUhod046WCOXRyVaRFy1cyi4qg1n2iVe2AZVLJcMBRMGQsgUZ0tWdH35NLz0GEhgwdXrVVkIHKlre0mXu9D7KGBnUJdIt2zqWLF3H4BPDnjwDNIdAnT4mhNhpyyU7dHVS"