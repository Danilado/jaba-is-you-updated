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

"u1dpdTTUXmZm6SSTXRTEvgoDKdzmV5bFxu2EYT6PlXrcKJTFwwpUAS4p3Sq39INlXxufH19rnx9jUqXp2Vd2q82equZHZqphF9UjVbQz41tHh6tQekRd9Wc6AsyCMNNO3yAiysfbFjrDyhjQ1gQsu7Pracwprzk6wB1zYzQa1TGzvCjWruKUoj2BAyfEOETot9DnnQ7z81aAf4VSr2hViW3LgeaMr0xBcSsrvzo5z5gBgFHUouuGwvee5g0KmoRmj0ZFzcGxXAMXalTalubHeOoejZj5u98hKDa8NKenN0UxX1IJ0biR6htcxW9wRcQIhYwLvEdistLqXbVCJfaICTTRjb8impx20aGIwCCtKkrDNJlXGR0IBDVLGCmPNMJuGkfzSvhYqSvi5htCErUuwSUjqlP57bU20vdqLDHfWw0jRCBC5xFHJji7PRBOLUnni2NY3OfXlZnBUm2fc5dTeOr5tg5BuvLT437SNa1yqUPhJqrF4tjV5mqkVeNv1OUkJj6WwKsHz6vcx1m2GrZszihswRtvAagApklhXTw5b1Ro2VDCaUtEKuQEbno0iSJn4enw1j1BEGUrcLRCw6lymC8C8lLer7U1K48TMbjS3z1MpdNLGoW9ZJndTVWMy1FZ7VdjOgxVJd8jR2ItujIyyvutT1ZvjlpavbHw4MyIhy6z6AA0KWldJkbZ3nrNtM4uE139kkueIf9yn0IirEsGDzxu40pmLyZ83VqG3PAG2h6eagx9aJGnoUd1HKGMhwCWwA1WMM9kLMKo8QBUilKQUe1fj35MiNsNWtzWYWZUYyPEOtLrqta9753FOcBROqMOIQRLzQaJr2p7Liyj6X5QIj3ApLQejZ3ztSTbeVo6X7SOq7N1CKPLN5ik3XuOeHiRB1V49GTp1VP2uijH4ozve9SmZVZwi3N9g2HOOcT6ue6ztgSmUn7yM8mcOyOUkBMKzrpGUv9P0Q2kzXBBUOceCtya5BHoz2i7QJzsLf7DSpT0DV9oeMc8yHKqCdwrZKQ734r5t1eiBhMC31ff6QtdrW3FOx3YSU7F5Rq8GKpChyCcR1ARwpP7hGkymvnB3eggjE4ueBb7UWvJMwsocHYMyMX3XGtFjEMvghWeJWyFW09R8ghavSKtgf7lpOhOp6nszDZG90YHJsHKKrisUDcVKpov0c4hbVrIVUJC2n7SQbsniDiP7h9Yytv9WyK3T71IGeZhz8ZDshQqzDei59oBEKqEcyLb0dVGCHQk4DpJGjqm99D6p4sWxfnJcK3vyZtqbH9aJfuleB9P2zYsfCfN12RQvYVHV1N2nN6BRN7N14lBYguwwU54XTiqSd0Wwz2YWQLk0xwW1VK6pQtEQ1pu3ykGD2vEMK9DCjIsmq70K6R9gXWQidNKw4UOlFD4Rx9EIy8PBsaOoC71y2jolqgXf5CIICDS4nt6knIdd0eL2wyNDwqvWSYhpcnSjOl3WwegC0AGffN3TXTn4dmjwAcz1TGvIn5wrgLbSawr9qRiP4d2Ovo1w4oVdzj3igujcrmGy0YQ7Y0MBCRhO9YNuTT715D2bE54VmXoyAPSo2u4LeMJFkbrtUQ9KPZMWmfbjnKFePkCaO0GbG6h4uf9PKkMm9X8Tvs9om9K5O68Q1AVeQPCvgltGrLfJjax9NEX9NNo5DjBYRICOGZkxyesqwpw475ClKnIhNbkfhf4jqi85xz7eV3bg4I8FidLgwIXTwMU4WT6kRZkTGXlLcF7IjJ4p0kgXvS0OavnMlBBrRTQ2pABhOx9m78yK4PMYFIOW0TTsny9D6pBHEh1VhQzOyvnroe9PYVOuQSmM0Sjk7QSKIrr49nBme6kSpFCuh8mkqwbtrXccQtnOGzIcNpCLwf81dE446BnPzMMIMpWH8TBVws34fc3otEta9O0cPNzexoNOmIdaq61hDTRAbL3eE0voqFiK0eESx1dl"