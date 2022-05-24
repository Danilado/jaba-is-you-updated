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

"IZOMxJMN3cS3EL0tKa5UGHa6dlurZXFduVJDKwwcpoh65rELw0PF3TDh4XWdadkEzgqv9eubGbziVqK9MQeDzSUo18Uw9e9GsCSLROp6X1KsRvcgz32XCv0Y4nxi6n7fBTFtwCFWbr7CjX1AqwWBvJBqtv5saRqVL65tb5GlPhtx58CUO33AHUonIdYOM1QtUaGhHFhjlOGMtfX9zmfzH1c1FiaLgBKffO4siDYiSudPxMffsMxNdOdNNrA1rGcZAcAK9wRHJx8mtXI8vyIjHdElpCYwrQ5gFs1Zv7PMIlL2DGq2G7UsNZ7FrZ0LNW98MyfGZepZ3ryqje8kMdjnHz0w5NY2I2wA8C8rGShx2DhugJdUMyJC2iAS6TfXnjoA8SIhLfZoAyvnOVL3eGRvoal4HIZmLZHNQp9M7t7YXMVMMA5tLShEu284FFxls8D78zgTH73qR9Tv1r5SLBYJAWEX6LzGVpyhHl2xdx5FcHHUPQK2y1afU19lScCGqlOPasm1M3Z8qrKGRAmqGl896e3zQblkJaEHGLzi4Fk4ffZJT3zUG7HhWROhleHHCMURUxaVGEwdVOHDEXEYcfCqiPOGRHfvCbzb5ZFjCrTXtunoPptCRv1fjw8jsZMYeBeLlf1Z7pGmghG4zSaFRolaPmJ1wrgIWbJRV5WLsql4OV2PXiulTmPa4mpC1cA9Ufbif2OtyYnt8j7LQtDWcpJdOlchAO3RXSGtrFKOXACVWsG26pLy7HtmVONFglnn2DDgwIA83pxvS3gZCnQFCil31ENaEMbwWTDiYFg7oeP5LjzgDXF5gIMLFdyBjCMbphQWHgFPSxVg9603TP4oDrwYHvS7yC8NkOitdFpAWtn0FE6ttawehR02C26GwHjLMhCdAFchmhhmsbsvLapOax4pLDDjpTbK3eweatXe3f1O2FRu8LGoIgffHNl5JfRTpNRS8sZOpxBq8Gaio9ubW3BxZIppHb37h9LPTnhTetld1cei5ISfO1NZ2rook1CDKBpORiCxEokbNvXXdJTb61KKE3WA12PoWTQ7OoBjAhipOeR11j36KbudqfkXOYO60WIjCDabs85moc8V7lscqhkXqQBlpASiTO4TlUmuSqT9dV7aCkDvj7O3Qkqga9pVMsKgbauAFbbZA7iByBJCsjN93gF1ZfOQthyl6BCmF1VnWtDilP2ZagAl61xLK0K8XE1JHGzGjWoMfQqGvpqGrELZSB8bfbTo9fF42XmkrO1P4j1EaReK3K017DtTYbr0q91GYxdnKbnJzMQWsADYT8Rt5iof3oYyfqSDNW2qMFaEeiBEhBxZGev77WB5wdMDDwLwGTjJVFFlKSVsclAdOFQAHOyMb73cb5TALE1cBerJWZ12RWIjh2J6Otv7CYn5SCoXZf0jt22SDwOFSW4lY02TXv1GjfgGEkIIErqfx204sEowWqKbW0prxBHrxCsmqstj2nO59aAK0uKZeQdqngPhtDijRKizkRwKrbtMUlOLFZ0fAzLMLwlcL52qJGqzv33MnaI9kZ5BPmi8CNdrcExqkUzUbgYMpQtxGYZY9LMaZxsjmDFZhne4Qrx7F3DrGlRGUfbpzdzvvvXhbohq6vs1xMsd69sizEuTwnk7QdZp3p1Fo2kCxaa0NWBKSXWsyjznExS5GcShOgraRo26fa1p"