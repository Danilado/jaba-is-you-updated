import pygame
import settings

from utils import get_pressed_direction


class MoveCursor:
    def __init__(self):
        self.turning_side = -1
        self.levels = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a')
        self.reference_point = ('moon', 'skull', 'pillar', 'pumpkin', 'flower',
                                'spike', 'jelly', 'sprout', 'leaf', 'tree')
        self.blocks = (*self.levels, *self.reference_point)
        self.last_time = 0

    def move(self, matrix):
        if pygame.time.get_ticks() - self.last_time > 50:
            self.last_time = pygame.time.get_ticks()
            if self.turning_side == 0:
                self.move_right(matrix)
            if self.turning_side == 1:
                self.move_up(matrix)
            if self.turning_side == 2:
                self.move_left(matrix)
            if self.turning_side == 3:
                self.move_down(matrix)

    def move_up(self, matrix):
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and i > 0 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i - 1][j]) != 0 and \
                            (matrix[i - 1][j][0].name.split("_")[0] == 'line' or
                             matrix[i - 1][j][0].name.split("_")[0] in self.blocks):
                        matrix[i - 1][j].append(element)
                        matrix[i - 1][j][-1].y -= 1
                        matrix[i - 1][j][-1].animation.position = (
                            matrix[i - 1][j][-1].x * 50 *
                            settings.WINDOW_SCALE,
                            matrix[i - 1][j][-1].y * 50 * settings.WINDOW_SCALE)
                        cell.pop(k)

    def move_down(self, matrix):
        num_el = None
        x = None
        y = None
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and i < 17 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i + 1][j]) != 0 and \
                            (matrix[i + 1][j][0].name.split("_")[0] == 'line' or
                             matrix[i + 1][j][0].name.split("_")[0] in self.blocks):
                        num_el = k
                        x = i
                        y = j

        if num_el is not None and x is not None and y is not None:
            matrix[x + 1][y].append(matrix[x][y][num_el])
            matrix[x + 1][y][-1].y += 1
            matrix[x + 1][y][-1].animation.position = (
                matrix[x + 1][y][-1].x * 50 * settings.WINDOW_SCALE,
                matrix[x + 1][y][-1].y * 50 * settings.WINDOW_SCALE)
            matrix[x][y].pop(num_el)

    def move_left(self, matrix):
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and j > 0 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i][j - 1]) != 0 and \
                            (matrix[i][j - 1][0].name.split("_")[0] == 'line' or
                             matrix[i][j - 1][0].name.split("_")[0] in self.blocks):
                        matrix[i][j - 1].append(element)
                        matrix[i][j - 1][-1].x -= 1
                        matrix[i][j - 1][-1].animation.position = (
                            matrix[i][j - 1][-1].x * 50 *
                            settings.WINDOW_SCALE,
                            matrix[i][j - 1][-1].y * 50 * settings.WINDOW_SCALE)
                        cell.pop(k)

    def move_right(self, matrix):
        num_el = None
        x = None
        y = None

        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for k, element in enumerate(cell):

                    if k < len(cell) and j < 31 and \
                            element.name == 'cursor' and not element.is_text and \
                            len(matrix[i][j + 1]) != 0 and \
                            (matrix[i][j + 1][0].name.split("_")[0] == 'line' or
                             matrix[i][j + 1][0].name.split("_")[0] in self.blocks):
                        num_el = k
                        x = i
                        y = j

        if num_el is not None and x is not None and y is not None:
            matrix[x][y + 1].append(matrix[x][y][num_el])
            matrix[x][y + 1][-1].x += 1
            matrix[x][y + 1][-1].animation.position = (
                matrix[x][y + 1][-1].x * 50 * settings.WINDOW_SCALE,
                matrix[x][y + 1][-1].y * 50 * settings.WINDOW_SCALE)
            matrix[x][y].pop(num_el)

    def check_events(self):
        """Метод обработки событий"""
        self.turning_side = get_pressed_direction()
