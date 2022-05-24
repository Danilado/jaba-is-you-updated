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

"aoRALfcvLtXF1PAJpWkKw9ZYZ0bMqSv7jtFrAZi4i8JRFO8vyL1kxgpXVVg3VBQuq8isnvl4hlUGZgqSGyhJQLKkmTIlcvxogR7Bly67jq7lxFaQNuA3Q6mHMwpTzuMopn16T4o548rPbY6e3WjOBJciyMcKxk4JtnKTtfy8KvXlV4x2CKQA3TK8sZ2ZjGJnfSqSZtcqJLAdZZum26EsNZO0I00FigphzGKJlR3QnjT4uNUyNACH6xfuncVihLM6QM4kQgNmNYPl9EeTbyID8AEHyOkJoHJYQUt8bh25gzaY6VLEJKETbW5mG8E9DGlcXPQ7ABIc0Xu1evNtW3wiljM1mXJWo7zImjFfnIB2dlJL5v3pxwAguSEfnLV47lYt4UTkZN5VbnVHaegcqrHXskXHVQdK1D2RuPIybuijnHYMAerd49Sw5QzP0ek0Yl0ldgE77XRDpk6QAdpSurBHwiiWNd342dm7LWEQAiTieOYO3qyMHhMcCnnWgJ7GCaTHQJ0dUnt5mR7NBizeOwAQoG6gDCLfgiX8g5KpYWgx1gvw2PDH9VsBP9RRSygyUnvmbUkuEEP4HABlMGt1Rt3vxuo7h7O7T52PSikx2K2OFvRvHABCra0toMtvjAp14C3mX2Vjzb1cqRapzZsZ7ubzIg3nelnvqrm4isDd3cJItWUzy0swwWJEaJ6yIu3ce5ZP54mWRenlG9juapjszRi3DSiujM0ETfZvxDNTs74az7UKAVFr9O7WUlm1fDs1ae9LGbtfhCkTBoSqnPn3X58pKQujSAxtIdRDs0WdxupWUv9mBjeoGd5h8rfN2bChorUWboxM9gyTriC9ABWa0VmgXj5ZfA0GcBCcDPt3MAUFnFkuT3pjydySwIZw148dsAdTUJ9uQ2nuzCdTuRNRhCOnandtAqNav2BXDWc92trN2DAI2GGCCN0JkJdDrxVp1O9GhZ7ECTQzEDGoIFfHIF1hlCQYWZfGrbJeiap55WPxolWnvTxbhE7JBTyVgKx5LpZEtN8W3M2V1DVmRKuZz9LkfoEp2ANlIB6McYx4xPYarRdZkN0nQOWXJVuEcQ2bO5F4hESXTg8WyZa2x46fyhq0psNed6RJ9XwfcPEJ2pSauju9AsN8eM5KR5nxMVN3H19Naz9CmbkMEQWXbI0dyLHVWCwmy3UieSeJ05M4p52zUwkVDcKs0QIIkAJLnInxi2dcsokZJM1jLcWtHL8anvVoGNhcnffQXsdcaXw5vkzczSPIz7gCmrEyJIKXPauN6De1mzz5bJ8vLpoYbDa4Bu8lwJtxse355yNmAwotPgFDqvCNHwittql0rYug1XwhrEVZBbBO5V1ks4sPhMJUIbmisAELXFws0xqyGnTsbQKWxsLEPfBjTn6S0x62ucH35TDFAoXww4i61CqxSrCpM4yHigPcTEau3fiUX0hbNsDxMReFw5UEXhmCmG8NLCIjmxjNpXAzloPIiPsYj84FeHEqegDn1ywVA00kylF4zyLJcZhiKYwDjoUw6KaP4EMh7dIq8xh0jNLAjSN5XqgOhb69WtqEDKDGqvJ2okYN0y8NTnDC8vI9jfWLCQKmVhTSEH70NhXf7sNmY8403I7pfIQ6FtwzAiFi48YVSVoJn1a0yfzPbv4Xx0rHJn5Zt4oyvkp6s6IWT02W6R9ly2qsHY77Tb69vDZmAKz5RY4ocroOiPA27p2pLuD86YJwQAru75p4psgNt4hZbtdL0styABfT8IyKpogeoR8Y1kDnsgZmgMU0GFbXvoEAHgXJiRo6oGfG7VCXH2seuUVVC8a2qdbKQ8QrzjylPjWl9iXTuf9zAvEMPWirHRFTu6vZAK3MVoeVGT3RQH4PEF4gNF4MjzrkOILHYSNYZZDFuXwMqkAtnqdXJqIL7wujZsGvkfuZ3SGwgkhfLYudqx"