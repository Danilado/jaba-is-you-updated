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

"LMcEhZw1IrJaY9YZr1G81Ikq0PhZ8byXAtjMeKYvDPsH4AMstdGbtKOUrysy2QQuoRTwrVpaAlUJ7fu9GADDZfITeo3Y21hqdGrVk4eFpkXEcXfTNr3l5PqEBgyhvAZr6opZmgXmDfepnODN44a0eCkY4Cj83h5Z2PNUdJ0m9IACJXXBO03kqihc6PwcvNv2cUkn1mccEVdpG6JdTc8kKdhyAkAhM79VKC3cfy1T33QwjDeSEk9IR8wBn8gEyjun1y6dkTVpVZj2Qd8m4h7DDPz31IezQiAcoxN5ovaWDqkb2vi4GRpqfd4j0jd78wL3GFacpX6YqwJgDhqHKJkEaVPnH3JTLZLnjJb1A8na6MVPEi8fRP4sR9ttEW3kbHQYtW77wyrMI6RLD3p7gFJM0azVKCA3dD2Zr5kkOs1jhfcTsAI2VNEpBpQd0eArmPz71MnnIPN694zIGbdV78uCnl97mIOfc1V0HFfxoPC71qVU7RHyQBCOM5dkQgBNQ9AC5xKsutoNLWLOUuwkxWpvRD2oWqwxDgUwBqnjT7AVHgu28cjJ3pFgyzAk7XSIssDPXXZPJEW2WVauC6Zx6MdSYh7OyN1qR3pGGJwMMfGjRxSRoVuRcEbmi0nVecn6c6EETI08tBfoA1o6W71ldgfrF0R4KqmOWdJvcFYsL8hjWfiXTgzRZeaAopBgFru7kGMx8xycDeV7hG3bXkoZKX6mYwHWbTthhD21ZU24l985GEbEhPxMZaZjGmuW6puTKZuGFInMgbustOTbRISlabTinFbPi2GVJbZnemEtZw7wy9Ax4XacZhStMY5Skyuz1ACjPw1kgnfg3uz2oKM6XM4eUWPpb13FT93DXIDoiZhq8dlqSYiz6eLpkGYATPm4J9q35yambws5Fohi1ZETmuXkQvW55YjEgUPsLcLXkqop4wuBoCUDnBHOQR6MWLaue6dx99t4eXL6lWkBG5kAEZq6x6JMGtac7Dr5v70gUMKxSrDOfqA5atvZf8FUYNmCwOutgNlOdXpJEM9NrmVDCnsYEdd7yr0aKJJd6RnjStRoctbf38SKYjQB01t5lCb1G9vJQI2vBQGR8krcn9VEkJy3ezGgIV8bHBnEyN75X4ju3jOxZ3wXEGuycHHt0agtLPa6DlGQY2EQrfmm4lbNpWmjGDYhWT2Hs11iRUcG71blJ0xzSAgiWmWjHC98WQXK4tkTeoIQG820IqNXZqEYH6I6eez1tWPyhjM9gXKUpP7J7x9Dry1OUYeYLeTs8LTXJnyJHlXMUjpoOlJ4Ub6KRIBUGnV1Xc03sfyKWYGEVBxa4ve5WqigKwzf921SWRs9ic5RqxObydMT7TI532utnjnBmCtMIRGsHnFwUWHuuCQJEnBTcoURkihwmcZc6hzdfSxsiQocd4QkX5wIJ10yM8kfDEPycprewEgEFrCTwr7lQm41aF7Qnjs2i9Nc785zuML6dnldUw3GqbUa2wyLYSF1wgCyGtzOA7BpYUR6prmwxibctVCOSHL268ncfDq8D06OchwTx3eq40lvrF0XCOfs14l3QYImj3txWNRb7wp4MFqg7pX3aBrfmTrzb4biRaz9DHJI7OYppOszYQlleeP7E83clTuynzahfVX6TwDyJysK502QYJF8aqWnjWCCFNuEbbAxX3DD"