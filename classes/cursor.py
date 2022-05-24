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

"CR7DJU5GGfOEx6mks7irFrJWnt7YXg2rXxBqgqaCpxIqbjqiXrq1V5vOk82fS5aeGRtJw9T7Qp1QDvzodx6hlFEMx23QsELgpxWAjXbgY2ZGYmDly6m1ckEv9HcWW6wK7EWg3IBb1hRpXIKGl1THZvcFTBOULJOVWyMN7A465yR6fdq5j0ylYJ0seU290gdedX4SAOXlpotvOTWAwZQvEKPfwt2lkQIQILLndugb5QH09hxotELtF69pCr7V6szgM7QAKSFpRT0cS9WwK9Y3nyYKbXsXEMfiqiDQg8yo5mV3vzJ34zNYt0duOjg9H8J7Gwv6NtQNhlOsQ5mW91UCsd2wJUKmrg3bjQvHoixbcYFs9MkEUjpFIaUQfoC80hRAaXuXNsCOTxFJhJSpMdz5PZgdUKyyPIhKCO8HD5jbHqfh4tQhGyQj5Fhqv76y5bKlOoP80U45ny8aEnHJfQMJ3UO7LdLewu0qbnZDXrvyZwgQPwlipAW4DiRpyamk5zWgpoI6Pa6wuaxSNTDxC7UYaKDzTBbQ16BLq2aJQDxTvt4MG7EVPfjJE9zryvB5WP8j7Q9TSRyndHmVQCNbHvRaBVhL2fyC29ksTIriwOPGnOTREXuM3WEmM6ukoPQpFrcvOSxd5AdR7tBjJuWJGceSXwrx9F35Tc4RKxqyPz2jgxTyjIobC5dPsk61xUYetNe1MBs7ZBgpaAFBM7KbonohIOAfoCOiY9wILaGrZUF6EAyD4Cm2VLaXZsHvss2Zntr3a27O29o8geS9zoLREAIuf1aJiPGhtyoPjTIvxI8nZvxp7GZ1HlfuMRdN3NRP4SLOB3qGIVXNODsrIayQCCSydvLaZeLeHXIk37jBFkQPnTwpNEjSGBGEC9oKtKRYtOUjNQA3yBdh3e9ieDnh0YJigXAFhyDFei7i1cNgKwVyEQyXLA2GE5irAf28bmP0MtgWzs9IEhIwezYLHTFLCfrsBRbBdClK873SX0ucjmQzzZJ6PeHlKPFD3z5Sl1r1783dGoljmWZGD8rLMAx4rn1amIQ7A3FfEQK8gWbkRsPL5acpaL8YBsaHkMZa4LRzPes52fJRvhHw3LOGufnWDPjR5uqbaa9LLtONn6oVaqGgMfRdxG9WLyMmljLTgkj6v2VUdlyOutdn2P5pCsDRsOzSaJIURgtj61nmodgC43SzE2eetViv6IlBdbOJXLefVjwWmjnDpmB33Ci7W2QIvtWwzBiQbDafdaYgUNidYwGuciLlLvLe3YkKS017CqECeaMVD8FI2gAH5XGvYAmESu8VyHKVXwD4yGEOB39Ext7Tqm0ID6oH2ggAv6hmpD5l2nqVZFCSvpHucxorALgJhDOtSsoxBiIe7qoI7yKptAVIpctJuK7q1Any9eCNboGfmOXcQ9OUUaFEOR4DC2T2n3XQYwr5GyeATg6hiUo30vJsmLebFBB8Z2or2JGYxtdgm21l7EuWJIxFEG4iL3ZB82juYjMuSi2510CXXhiJ7HayJO2YH5LXjXIzdgxWIpHUGnBlKeaSI4QZalhREna6ZSujxEtzS7BPFf1ML6LgTQneBNe8xGhIGFBEznObmuAz6qXXnCW5wAQMQg"