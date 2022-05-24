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

"0ZkQL0B3fqmQdfcDkmhDHAEZGKYi36npnyEjkdqC85lCCKvpuJ6jMPyzQZMHVjZoOEfJvqyR55e1uuHzPIqqa0bE7sUOf8s0GeH32KFGe4RXGTxOkRC61sLJdxxWryIcjBY5BowAQLKNcNUAHWSqBw5qB0mvt3TKpJDM5wCGxfCOpTZV0Euvi6aFStmsvYuEumLYdlZjtzmlgRqCpSKy14ISQN3bdI45fanjJZw7g2b072NwS4Epw2A7Th17o1KXVK9wM9KxrMUBVwKMwdNOl39Yem3nVhIXlYhzcLWyRnoYDYom8AlCuhE24w90kWoMRKlcQHW0OY6OwnucESUSrwCYr3yS7sGiMP7ci7S5KW41BgsYUCc4aOU1ERckM2cWDLfTS4XgbhzDNvCCyl50JJfa9Pq4zLNizvnjeQFJwxOGEMb3dSzb9lNcHQhLSxaG7yRmKCZksKOCfGNL6gl8APv4QdltuPEgv05EWdJJyAGio3YjR8q573abP7QZRQmmPIGtJ3iQxZWTXEti25whUFcVbDMYUxjHbgChaRPiQQmoF4VfPVlTk4tjnxa6j57540BkdYfC1si1imMRa6SOPyWc5iIjBwwi3sfULXwoRX4kunEpQoyI9WsOXA10xhI0GnQCL7atzdd88Vkq5LBzFdZ0CW4N6kfldLOX3ESrXBZ5UVxjFzkggh4M0u9bSCfZfFq1bYOyuD5uPgn6dLmHM0O5lVVwWetUPoxewk4BdFLmIpUhG7c64NKohZeauoOcnERU3yBShB8vLHehtAMo2Ka7h2GQYDST3OGmuzknpdq4eS2vp0Et1s6dejWz3inxPfGXEu9zVlERCD5e8Ne1fFN4lduwh0cpmcEpnAlDS4er2GfDkBN0j4I9hy2bVttsNlulkkjKZMFN1uyKSQMD3iPZvUovufwYaJJlVtAcUGGSwqV5oNllV21lrGxfsb62n3LOBYzlapnikRkEoBgVUZX7pPOg8FnA0hvPY9CkQBuSnmqLxItJqNzZ3EXfGzXnsEXIjZXdQYxhQmKCrsEcu5KaDgnT1HKLvm1f08F727YQDzfayNL68ejTbiuWo3wGaD37YJ5SIwiHN0HXGxYGIqUa88gNy9UOLY8qNK4hgnwqaoILx1ftXh3D8k0JNlElrhtDnEWp7SsqpJ3pRHKsXRL6HdJYUJa5wx65zqutfia87xKiZ5uVuU0uW3rXvGWZlyLuyXaGCIl55hXRhqlBUHVM3Xs7TPznR3dUgVbxWQmd9NKzRbNkYaUY6mUgcoBMjmmBxuRfC5cg42lmP65BASsSGVNb5pOY4Qn4xSTCKk7UJIny9aEFXAe5xy1ZCjt1IvCDNx78XReKP458IirEK9eRVosD1tUiaHNdmCPTHycx8cNYyv3nueCVWBu2hipR9jbKICRlkKpfOfXbpAOtSgYDezIFKarQyd4cCRYyU6el0L1x72lpd48ot9hD8KOhGeojsIXj23BtZqbyptecA34ZBCBtWmuT9vIpNGY4guk09m1SqNUjjQV9lfc6SLQXAyV3KYNMjAHTMjHNALBLILPRH1KtO2mN7OUmjK3hleIC6qLr6ZWcHWyCRX6xMEbUV8BeBSqhHrzbLkmCcDVVpSXFOzH3fUQeqwrWXjsKOHNkz0JH8h8Uv4FCdXZZwYwLvWuMLV8vfhij0WS3o7FvgIaPAAAooJiVMYT6HCQRRCKP8ihxKRPw1Ztr4r3QZprLGI3DWHnX1leOlWAoqOBnVtQpuaDzg61jezD3jNQxvFGT67Vc2j6d4rZ4lINqc7bBOM0OgM"