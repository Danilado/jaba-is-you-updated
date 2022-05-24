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

"vfADgpDfo4P7LADDDqBXy0eM7hEP7KBDVBVmtpLRl6E7JQB0PGtNyFU4BWkcwJU0lpRsOJRWDCF2fn5dLjtkBrqsErQyonAXib6BwBEMj3V9z8kySWGg2ukL5nP90X0sTgbvk4C0w5xKG1H1YLad4ChpsabUh0aUkADV4xgm0QEeLqkycpqi4EHGTsl0siW3JpLRj3c8UfS0sFR8uoHi6hj4a9f7micNPMx57sqZsNyGJL8BZeenWHBeB9orhVekXJcgqZy0JwGVcO2rEokGi9OIGzuBxCBVHVrQMgo1aF1G9Lm2YbsA5chdIE9vk3p1bhx0XRoDONPE1kxjCtTHr8SG8pDvGWt9rhnWLbc2AavBt0abW1WdAQ898OkWWGioJlbR6M5603g2yjTTpQZmuB0VIrSXuX3A8JVgILumPSOjW4Wxmwt7AAFZsv183cKYjhEn3XD5axzW7OaSivvrFgTgh3CjVYr4cErPH9CqiAdqsG3PuYJuOyhcrP9j6XpuG6U4wqx1EqeUa16PiFMC9iDQRipK1FJJ3SSQJhDQlJ0qPep945Q4zysIfwJA9PyyYAKkmXuWgiEiHQOuF4opVUcXuKUdhfxqLcIxPZrmrIOxEbJ5DOLwyIJ3ZeyqiN8dX226uMBjLHqV86nVIjCzaRCU0OaSlnbrHBdU6yWOr8mONSBUSQ30mXQItY2U0yfS0y1F753UhXsDG7k4KLfpqASe5PlT4gehRjo0xLwys5r6LJi7XRGqktXbRU5yHcB9ntVAJwqWEYFIT9aTkD7wqasgnaMmYp0Hu1MWxTzIzh3uTVomEbCNLtcf7rGVapFSO3b8NSpiUauMEBFOTwla5DN1IvMkVqgRwkD0epFN9WQch1eAiCDS7qZ6ZMlMkKrKFbOvW8oKvBaO01CHO85PL9mcTTrlUN3uznHt2y2TAdVkOV6q95jzqnqM6COtoV4Mtumdby7gGamUR3QBeowPW7O491UN21poAosRKK9hwtThUE44YZHmjsr43z4ALjmeHoXZ2eRl7UgnjlCiyw1DgnFV3kY3lIxYCyFDcAsgo5nYSlfC0brMkil0E3vvIgJVIIazFGFGjlFTKfkHo6h3HUrxoURZSjhiXhso0Uy97JTZyAcIjHnRnfP40lBJQ542JgEc9TcE3tDBMimGWAmabizIHjdsFcc5DBcnegvdgClQcStFpN9JyehfADeqd6S9rkgmjLJoBhVsU8pKGyXV2tkXhf6PMpy3aabJ4rUmOEgohkF1zoDHoVFMHvYgR6gFf8vYFaW5egN9DlwroT6y2RgwKTHNvnyl9SE6v4BdraW3rDxp8ULuU7ArdkbiOh00iDkqSDmTwP6DJuiiM7xMtMQ3QbeSbeDkuvsUJtvNyr6VpzMaclEb9g23VSTI7UVRjhg7daljUCg11dfFeZFjElon7DxarH7EqHjJeNMFROc2YwRuOTXK5YSb9nu5XYNjiEs2NTX3rbLGGM0O97WrdDI2H7JtNZ3Au0mkNwS9rMEepwSFgYsqLHi0ptZiuzvqkvoKhzniuZJOpdKkvopEmOnDpO59VeQsiNIUVSHIPBHr5cazDQzKbhhoCgyPw9TmNyqvyVlexoni5DgMh2RExxcD6RXx0l3CC7XmrIAqU6htR64OTcpf7YdG71gM2Vt8CgLxrs2jHcsS0UyMD5cITPOe2ezpjZa2xlLfx6ADDxtsK1SE8T3qxVVCcW8UVeEWW78lNJzHQnHF3rtFnjAk3gZcxpRPgDdApRQlSS38NUBI6wtHZqsny5uHs2LXHvxXG1EvS0ILx35EwUO15yN1PgUeckhpnBLTyHcwndJxQassrLE5PEd65SATC2G3U9CsfkY6WeRWhWCLiNn2LTNurNg5BKl1yNmJuwbwkuT8gS98DjNiRwgvqvT9EKpFALu1KiqBrPeFX9FMUFjOtLFlYbvN24qPTCcQWJOLW72mFjQkbYthu1yRJEFqr6hG55ImC3orAPKaZF778VXRb98FKWqczl2PpQsLCIYSRumBa8M6VnHV7KmSNmMcxZOk1xmbJWwez5LSUX8VLXwIPgNEzuiCwPXhU522MfbwMhBhOVxrE6C1yMrWH8AXXfBhc3BM6XjLqX17mXUxfwgQVt4Nmno5S2FhiG8GI1CZrlieSTXW5A9b8YNhnZchuT3Zh58Xkpziabjj7uEzLrEKgmIzXcHAysDWgKZ8QWKzARZ9Ewi6VZmTHTqy8WO3IxusTVKIjpjnsOpCNxOSCN5GhTa4h6aBQVmcsUuMacCAw22HwqSqkwoKCXbvmTK7x0xuVULQRSPxaPF4DqW7ZiFn2UdUcCTu5aBL3lvaaHnldMWEQfT2xNEhXMKVQw3x710agWB3aJbjtApvBsHCt3X6d4mSa6oiVdNe1w08DnDtvUDZSrMhqDJ0TE4HuJIlzXeYkYUN1i9sDe9hTgDdzthdDB5di111QcUjrNHwiMEPiDmgqrfsKjgXDL98cUEh3jwKuOdSuGA0XPN5JjLDUz7g9lhastPLCtpnjHQCvpE3IPAqcsJaDQOhgluClHmS8oEBnTlhO3fG7bxG6WaKxwBUFbZZLGpJI8ZShqaPQdjtsUgAWYl6ER4meeKy9E5x3MaEqFbrss1t9r8OXvQEajE4zTTa0rwTDskEIPcAGz57VrzpzppkaWTgs9ApVHnAsiPwiSQefzmZXq2t9mqLMyimKvFcZz5fWHKtsrmKZQ8OPhYwf8n7GaKVasS7g0UQOhq9VTTF3hG2s1j4vRp1BViVHvHQh1efHNw9uinpUz6RheUfpHzHZh6mjVa9lKeGFu51FXGszJlBxXtppHqfN3QouBsbcOrdudHXFZDGzwClx510YP4GxAAhyQ86QOGI5pLdNJvMVaDqYpiTIRlpI5SQSLXGKuJDAC5qcltKxWG0LEgRzftqDQpWys1VsuUhQsOlikEtKXJrDHZoMFfPYGqr6LEW4cZyT4E07bWCom1SeF0GAeWDVtKUaPxvBZ1zAdyxBfaMilSqoa6uA5ZbluFkcym9tLi91LFA3yHkbJqdLyk3jFQA2MXcxpX56Qg0XVruwq89OhdvA6flO9fXFgsMMb1P7F6HoCQrQmwLSN1SSIfiA91M63cGwkiBNwGio3fGULfSLJegem0TCp1h6F4GO01JoY7sY6KUtYPUmwzGGcLvSDZTtX8ZLglI67RXSrQsoAIM5eONYqYgcZXyF37r7dXeYVMG8MAEdEhSr7ELtfbAwvJZ1GiANDS0MrpiAK3dJQXg284bLPmuquuHFoj8IIqm7c1VJzUkINZoScv6eaKjYiTVIpPL0yOrLRsfgMnSTi7WLbYB82P1ZlCiuzIGiwatCOWbkCaKSAdHr7OfSALeiKJ878Qi4A1UPdBBPgydovmSYGA96eAeUQkj5BmywN2DUkGcPk343y6RgyQGGQqBvI7KfvA1IYgsvbUxu1B4JpStNXBuFIgWWE67j8zh7qtSX8HAYkbd0rVwsXFJejKnFG13Jwt7T73qa4rwDTeAerA4zQ5Wji4QptREZ1l4bxLz22YaMnwZSrejz5mBzonpFclNWVkKUOBb6YhdsZ89rgfhxLrLIpvoIMfSJRYd0ZZOY71jDMW3tLlrj4M1Nv4aONyBgyz5PJTINjiYCYmka8gxhcoa9A6v7HvaH4fDjBPTH1Jn6p56qWBdUqsvYhVZVZKSHYVmFrDpGSpN"