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

"Z5IpTPD7dniIXFVLHovjMf792QrJnJZ7v0EpBryOhHD5Dm7jQHQP7drthavQo6MeGVikwLHlYvhjpCJLSL09Dtv18UhPLa2FMFY1rUCnwy8rnRXkpvWpNcFhTHWfqfFdmgaVMJc5xObzfFVK7a05bDOM2JY8reAM7bnU14iWKBEZ56wcpzIVMWD7mdp5hdIwckTyifDr4HhtQ4kvPe9eKGzzlJGlKRvuYMsykZhIspS8Qt4D3J6LjJJfRbqJXyJ80Sw9Db6AZINURIGoGkvh16UpwnzW7FG7hXsME2QnISr4ihJqLN1QgI2yxWymljrUOE0pF3vxiEb2dEwfv21qBiM7K7MQuK1YUs5DINRPx9hTCnifq5u5en7vMGgidPXoribP7p6noL1f64h55QRkXNmnug15Uyt2vtVBZu9Wb9yxBnnQi6kTbSXVZ3hE6fTBNgQuRxbPFkECyk0qFCqinY3XVoPsfnvObVUnwN8EzN48cXQ4ukWnnxQMHvEwCbpVzsZHRvU2buWtGXWCT8vX1Qwsg6rQFB8UiBFICO79iYysDpXbL1hy1ez1f78ZyQZ5myPPcd79JEYbMoFVH7uP75MRRulT8GsogOEylNhyoca02ohAESua7fdshbVFpHQuEu2BB6BzgmbzETeqFgOB2fi9UJdjk5e0a0jgfGj8stOrXSKp0hIsmCWrSKB8Rqoew51YimQkd5mI2nGNoQJEuo0cc36Bl6KYonHVtR81OkueRpeCXxPN6X48e49tBKofubWH904Kp10jyU0GP4jRcO5H5DJFJXUr5aPdZOAE8gwT46s1EEiIzGjUvAzaQqeZjVd2Ea8xzbfC7qhKORpoRBOjl03qColmAyJAoS0Oa44EvWpVNRY5rK1LvnpQmuLRnKW6xIBLohUpo5G0FaDX62yxpo4gSjsMYmTGMwyZ2qaqClsGKplMC2663ZsdqsxOJjmVx2FKtj9HXeMzQl05wkaJ1Crh83C1is7FXmLT0BRtbc80BmWbv4wh3Y9Apzg4frZXdEekOfBrUu2ODGSzuYBMmaqs3ISP8oTCyuRNhyyusgqOkmbf7CRkiLR1x2hjXy2KbtVTLnTZX37QsmDNUHYMKCrfniVrnIgP29oKeOMxU02lQSqlfJSg87edpnamiRtwD3VlYHV2m915GghvkobPWHEmsEnOHVlYYUWLsuQvqdhqFFBEbDg5Eu4eoHdmv2pf3tjQCe9F1yxnlp8CaXchyFDfzhPUNa9WGnHqsXPTeFA8vCTG7k5ZTI71BpvWjNzwtpy0w6Jg0EEzWnOtKBdH4H6IlTd2ropam95FWySpVgjnJq05BR56nCR27iFuDsIkfzGOgQZljlty1UZXhKBRGeVZcPu7UrZSt3DRxUttUNDakZnD96H8XsOUT7fjeGjQKeMSvmYLZ1gFzakMMxJ8bmnQgY5j4DD0nGBX80DdwBBAp0r1nNQZNUi8QwqbI7NeSNw4R5FXShou52TAT1S6RBeiqkfmsIxJU6x6PaXtPSAVy2xpB38eeftv6DR4gwan1OvbsvMagd799FvbRZoFFB3JIzoMjTfLBNXOonUIcB8UFaJqryTYWeTil5YlfI3j5ax9ep5zLqPj0iLi2gpxhCJPSyqqFPgX6prXC2J0z6ynGoTxGbsG18UDbdk6QgG08VwlbecAMppNKwBjptjejE0l9YV9z4p4qdBbgFN"