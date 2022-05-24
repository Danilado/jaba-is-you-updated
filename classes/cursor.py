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

"EKjNOHAlNdpzJECpEBUu7x791aDUD7HZrWtxGT4YZoXiwN31UktHD2nhQA0Nq0NQNgK9IHImdyWi0nlmbAChYnrmjHSnUG9MxOQ2KhTYK2KyYIwHtMmIMCY4gG61RGQ7YBMUHEJNP54Z5C6WYTZwVcpIS8nYEJUpxNv1SMaQgyv0eVbizUrBWPCZpum8pnTwJKv9EEwohGvjb0R5HOmE6f7yfTTzZRxc4BC7wxiyj1oQhElRK8IK8DEuUxC9AaD2xmfvswUZqRJNgXle4maonIP2gSbcZt6y7yR2XjZylFPNE5BQpn5JjIjrreL9lAOcQswox8tzmzVkynBM5DK9Ntqbw5RC3gtEBMEKuIFDlJ9wwTJ9IJz111wVy96NR4DTnTasDKed3i7rmwSdj4iicIlT9TYADGyWgGbVcl0COnvbLzE9HU6Qblgwo5ZBMYFhrqjDFyO6SOAQ8NkC9z1i6qxmTrhN83y1dUy69s59Mw90f7gtnp96hcAnDshKmBJQ80bpXLEPPSLyTLvCaBKPCv1smPTedzzzJhJOXmab0xIiLwepvoyOJDJ55m3XLsafv0eJx9M5XRBgUvhGJ1DKaVGOrIotlhFJJsV3d3O9wb4Xjt35iFDR519E0L5PB8gzvHbxCj5DfjrJyAi5VEdaLYj1MKQCnBGFiC8CDwr05Epjm1FmEXW2NJ1iMN6xGDi9GoFLcy3H0ZOUhqgIKLCdkTLgUxGtdlD5NEJHLj6BZtnu1TM3qG503xpb20xGl0H4h8eaai1C7jKTIUADipKz1EAb8q3HCib0WXvxEoCjOHFeCt2voAHz3Cs85AqPqUug6V0Ob0QTBjUT2qXyqB58gdneNAVJddMfc7kFLsiKbZufgqbeh7pUgKx1fBJuTtmJdF7LAY8aXpPUddnwxTiXcYfSxgDQlRdMRLcgRJGp7tXW63s4bLOXZVvNe06686fdIeiLJtDW7gAs1tpc7skVCiEDqH38C8IUuvzWpdEdq0ydpsqjyqev0p3suvAH3DtGWqBPUMyxYwmSzcqJOzaS6Pcqz2fnl1n3Yfrh4VYfb7PyGhhXUSkfBZQgvnrBmvGRcq7clexgTmmcazxjUjQsIsfiws9zkGh4sAcwGOKwNNtF63a2osRsN0HMMLdDFq3gyib8uQlG89tPWqVEOxBUNJloo3CG2RCB2d3Yovuox0P2RZUdVHz3f4CcI6sZZS5wfxJIKs8diNb0bl1D3HXlI4KlCKoDuWNFtKsOr9fq0R4u3mevMryJI67lAHGUiymvMNpSvbT1QjKlEfmUPgaNKttQvrXnDYL1EYE0ybPw8QSIFFF7qpRHBaqrtXj49NM2fUy22Ne9NOINAoTXytDWRdOxg1BLMf69eyZ267CldmIPR6Ehqfohn14spioXqygpyY616zuA86fonVR9TCoJixs8CNb8I0eI9cmaH2lW4Y6p3NDxZQYr7Hebp8SFXrMM32ep1Gft7XQIjMMMHUK3TxjTMndHPrXSkETytK3QxH1S9XvtWncyAndlrbNwbSvcqVPBfrxtdImB74zCR76Bhz3rRcgysmcJbPuh0HAkTn9vCk9vzjppXLaRnnKBzFoOrZuarVr1tG2BWZSX6osTCnhfAUup5FON01wPRICZK85lKDAAfsN2ePjE86If1Bj0YegYcR95AkICeoNK3u78dGG6IqCFW5sYOhUjpBul4sj48vmyvhjmW6JbiOCOCCbfXL3YDlADd4RMsM2n62DeLmHS3tpyMUac9ORatLX3gnXLbtAkoZuoCp5ZDXS87QiYGkX87uN5XOy3fpSs1ryEMS9UqInyzvmQ3k5h3DLGhPR3qtQaIExov6n7byuSPv6oh28BICsq5ASpmtz0"