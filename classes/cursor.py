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

"VGkpslIWHUWk5IReKoR4AHLYoYxyaQFa67d3i3tKshladCj6OiUU55jx511xnvGCVbhRaGtrXThubamPRat4LAJNNDIkZIvbtf03RtlkjQqiTuY1ulCs4Xd6FHN5FxqK9r1DWTJBrY2yWJWN53PBPXMUDmSgTriShB79sUUFtPj9uKNQqs0Xp1WVPeZJyMPqkofgZiJX8EqzCy0RZkobxpGt17X2Q0Be89jsrrIakIpPWybMAs7aI13XfkQ84nSc3rvC2xeNjUoU4GTP5bvt2tp0yHr3sec91mIGTxqRrD31FzfUCPC7B2liKtCQrclslepZoCOX4B87f8p4f1cM21cAzLXIKJn7JFKWDKcP7s2HW8r9ZFgJoQQohne93pnvknjLBndbuL9OpfzTVB91eBzJvi22hWfVgfIO9GLREEy8LwjQYa1auetDb1dKMcei4MA4R7SmFf0pPynAycXpmjXMQlqpnsr3jvd8pZIAOn5Tw6B206wPumTrkQJPSZxMgI6IkxaiCD1sx0osIdkJjz6DuRRG7mLnxUlCCi0dgGBngJdDQ4rfgHKM1N26BxKGI1R5Ykbve12QRhz73H2DHO1C1Uab3sP7Bdn0CAukQGfnhBgIN90r54Tulb8QRsSxktxo1Ux6OeAwVd2RUh68wBifBsSbOAlsaDOV5qhWSQKz2cONFWbnUbKjjEwiVP3NDqFkiOArKWrN7Sz5srtzZRj9bC3GQW3wuJHw3f1k5xLBvlAbQuquJ1QwqFhRVFak8HaVs7ohe2TeRfHynFF7mjZN3ZDgHmsFviojEwh38qct7zRWQpA2yxBiL2BQU5TR6qA331Ooa6QARdTGuelZUnh2hwcFscA5pp4nNVoRcpLWTlMEAsUBwTxwkbaIwUyCeZRu1HULUcmEOEbjZb8cfx5AZOjJ5mOrnvMYdOYf2J3jN6O8v6EtdJv79dBmW0JL8OEWVJchP1d6KPub4tgET484t8jbKVVVMxX7a3uEd7g83ZZyYMhEkKiMtqtxGJkzlM1UKbNxmWM5b4L7kw1cIoobk5GsVyoeYgq7CYR5jVTbmNVdkMYbKg855FJrcJD4RSqIwzj9gSYeGCrW6Z5PdJ9MD1auQivgad2NFJcQaiCx0kz2ANDlaea1gG2XnpDvvycRwFEPDe0SW1G5C7iugICyD0whWAvbnSrsMWiXAUku95u1CM06Qm1nTZzkuPVtVzyCrATxzViyv2ovH717fxeMHAC9OOOgGS1WbmxJwk1e48R4Nkpmqx4shZpqpjgYJZPGbvAJfee5wKXfQall36r6bIz4cwSiMQD5tOJXt4QJJduTqTh2DT5CJBVE1vk2v3PZJrDxhTPeMcCZBIRI5jsOpbx8BuBQtwncHGO3oafVKiB2nFomVKuumdGlNo0P1XzxHu97vxvygbZkKWzVufeisbQUYhTof938cMjDPqaI60vpqSPCPW2BvFR0WmhxSklyL0EarICWNqtMdJiyHtjiXyIM9HTtNqBqQQez30WfLR6zuaOKR5IGAxDN48VSELbfeeHhvBhCPjdnrGvRjv8ZedUs194p05FSANjkUxwddLVdZJgONqLeFHo11IyD17umzGJdzWPTvSFhidvJYDtcKf7hCIC3nqpjERXoo3AQwV23CHjK0BFrsiNxcJ8GJHvype8NtX25k3Ga7AbN0G0h9MTZYXZhx7Qfye3bK0gbbnWUUvmzynqXDAHtsgz6edPR5c1SeX5v5CimsDPG2QVnaIWvvnSshhxbsDmSyKpakXzfzKRQaLdbO41WqGUZl20oJFnJ2ZWmkJx990nlktghvYZdM1Nl0yfGkb6vRZRHl1QNPCfYxYDmdkhRlg4sdX59nQSehqpQOldSelgnKjSTPHJEBCTKYs6h4oPqaVBm7qtlh2oYo1zfAOSglyPOHjmwVGqhCauHkzfyhXmigUiMJycIezHSPaK9dz3dxoLojsJxJIjenkAsc6hoDWoWM7XXJMBud9wHYnhyaNfeh9VFmXWPWVbGz1E6jRyk3I0tY5TxyspgU8ItfVNX8CZ5dJ75bCl2Vc3SoxgYiuPa2AlinARo6Q3s8eldaJG3ze18QaGOHIsUczV82wZwXdv16opue2RmJbdQEC9vjfVikdIEhgM1ILlZXSzXziRY0effF3IoR2nPSrUbYtZP0djA5o3EbY9VxTC8B3f02m0V9bCzqbC7By9U3tkGomCGXv1lNqpRPskboA1B1EUHjGvLdXGlEgbKRInJ2Ae8zzB3L73aDs8JafMKdlNPPQv1QXKSNeBoK83hSz81lGzUsmtdy7QiSa7lvSI36AEi3ov6FvIVZN4Mn7NVaDqLjJyIY383iBX55yJTDC9lbWzsskIifdeq8DBJkiSZ7FO7mCx0tWES0alqE6i4fDypG5Oa72wXckNrslTUO6EsTB5y7niTiYc1CdtsoNvmaSDnnqabZzAEzdvmGOinMUh2ObNllvo2qdLCChxJin39pKMfmPkYH7AoNHjl25go10lRyMm9GtIDCzmGi8fgrJNQP80eivZnT9GibLC2icsseOSRRYRYnIri2CPjckvtuYqvfrvO9KDXnXEJAyWSauNF01aGnq91VzhjeevN8rz7oHpGVjhqjr5EjkCyGEJHuB0XFUwk7PoSQ4iLnnoAXNRGCIVETf24z6gpeRVqBrPDXptM1GixJRvmJD0qU0J7gskSri1oOq5PmTDhoK2FIObg2KA9nkWtNxBiVCP83Vi3UowhqxG9s05IoSVyrt9hU67FcwJHliX79EjWUD9FIae9j4jNy4hyYO3d7D2h9xM8J7L8Pxht92dJyvjPn2QEGm2kjpc683nR8qyOJJb4irPrQ8h29boxwGucASHvte0tqqVRYzbOzgzW8MutJL2RWfw2DIyDBkx3w96QDka09nbcWOWDSzoWQKOVMMdUfC5IcqKhz37El1IXXXf4yjFJUFbzsP74pTkLRPI7idT2vpm0Vu1GfCtd49MD82xysuuksw8h6HICeW8znKhFALtIKx9eAsxyf4p5KZVcLo8HSlkXIbfxwo6k4Rv7lK3DCzb6MY9NF0srGbVUi4fChnn8efU7it3mZLhYChVm9BCqLpVPk0apwHywaHY4LFPxKUhi5vV76aeqgIuSVvYPaKrM7tKlAHWBsPlsNJamjchmWT578bgjBZRn49kQ61XamV4RVwTNTGwxaFako3WwJT2uFun38XLfmAryKEKZCSTPglEVLpy68aHU9IhV0eMg0xnuz49YyIWXdun4A7tzi15iBFLfz20EH0FLxmpyvNaaEZw97R6R6yAJze91A6baQwHJuxh4dwxuF33aM95y2EIUc"