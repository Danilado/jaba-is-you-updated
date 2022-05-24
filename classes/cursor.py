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

"0ZSkSjJpyM0GxoAPRfRfxNdbESgRxLI0YliAixtnycoh9eWxgadxrfvl70h068QRKwjv1dpc9e5DrxYGnjGy6omE4kty9N7aobRlATg3l1RGDsM64lBqF1SO6FatSSgXeg5t7quk0sFwm3hWoMX4jG07mMTLmqSYnYC28fEoz9tifMli3IaiK7n1vFEFU1PXc6nJR1XMSqmGsKFpkvoeq1f6DP8IOMU8lSrzjp9nQf0pziKfKXrKbzjZuUavnZ1NiZWRWsixXpkPsEu02jvO4CURwb8HCtQAHuvIr33tro5cOLODWgYNh8zyVFQOd7GpzeBIth7WtIfyKWWJjkC9BDhy1ynezCVItZloidUngEnNCgnNtX4WYynK19Mw0QsDUwa2JoO2EkDUCdOCyUhaYPRYPGtOnTytWkv5fjxVgHaCfIExCpo5aEcWOrxhM0jhZIAYA6vLPGnv0fPykRR2OsxMW4tZcRiI9vFvFIneIQrPo4pvlfh6Hp2fhxAEozxC3nJoXgwMSiplMRmvHFuHMy0xK9oWvNZoGP7h6pzKtXiTyaiXb3tNssxeDCwRq4uQIgv8spYoK56oZUuJRQOz6wNg4GVLamyijGwLf7CaHce0qYSwBmGnOalNeMpMWm32DxhlJ6RPQ6FEAZxkJAvw9W60sPE0PJpCvKfCHfkCFQIrOM49xB1I9F30K64X4sITLT0lCsXF4MVA2B9FZBjIfZH4roAM4O7asC0kCkzHU6FqVyMKYIieH5M4NB8Qe5IJUF0FG362CQkMjYdfEgGWOH9e7qKM6DeUw8njsFnPmXFL69PdWMrgDaXGEJ8h4vtFiydXsdbcDvlqGemBRVlB1SdTGLTIV7ZJ3qAwkneYtzGe6RPjMyROUYF7PV2AGqN2GvD5WWYIhJJ9yUu9nkFU6cS4cQGgAnPNq7dd221mdeUentkO74Wmdn3uSsxtKz2iUlaka9kfrc16Ro6JXQedsjeWaVqcLG2NL1OmjttgNNZO2MS9FLPLBbHZIlfDJUvQQEt8hFWBwyJzoJsEGiY3d1L86EvNAnnWCr0EBJEIWPpPyyMoOQcomTVAwyyly5oPAx41Rsv2Is9Dg0TFsX9M1nd9Ge9FtxhfihxRzrEgzNtO0Plfb9nqe2wmadKcP3tH2o9T5imPjSp38mGkgvj8Gfak3p1PkblKPtJpsm5dvTBpW9leqFM4eCmK5LsHj1W5nmvm1mgVaHJJEhMMTtL15RuSXv7yWGiLnMCc7JMEH5jRAjCk8fA59VKi6K0foEuNle3ujYnnXD5WUdLvnCTyuCAQk7LqvyjOE2xEQFgsSiTVuwR28dlDbrYZzdw724TlkfJtADS4Bx26zYbhlBzosGMteEvzjmobSjyjxhhqAPh8rWPLFdTHWe6jzSedaATBOXctUWrHhLTrFaovKt3yuD94NImJleu6thA1tttc0u7nC02tqeysTzW8aqRYtzRDbAZL2HJp11V7WFYT68njXahU2jnaokkitrYX5s6pjfsXQ9XTzYw4W9Mv9PbZ4sesnRtRPKD6989KyssK8D26wXD9IiI3hL5xQ59BGblPDsi4wFfwHepFf2EKdcijEXrAfYla5rX08w67VHppQlRUlwRMAr0AUA2n4K9ta0Xa7ZpA4RIUQtIxoP8TiNWfSr0I3nz7jC8nQ1rzNFTNTyHXpo4AGMktW2n8UH2I5E6ofzefme1lcAo412KPoiKJgIHvuElmAU67sSUd5NiMmhHINAbe7WQlFDpcxE0y5j7sh1PuhbYUWwIWSaUIEyB8kSoRmpI2QDqqbKbf68IC6tS2CCzwEHEUUGN4TkntWS0BVyT1Cd7450PEaiSKo8JlxtbGhBOSijbgjjapmxhUfzfVXYcZuPdwWBovYWsDde1GyyA0hbVQkmVoeCFgZvS8yEwLzVVTQiNgMtmqTlx2TFe0gw4XAWMxWXekO16KmoBHwrmngyUKSwn70AAUQ1k1hUc3Od68ZHrMlojDtvmsYYxEFMjFYA1HlFiKRjVgunhzNadhU5kEGLp9vA86cpakIXKlY3D52CXjIbMespXoALR99D7eOY127jaV0jEt9BnL70X0EIRRrmcj3xtxag"