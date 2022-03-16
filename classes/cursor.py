from typing import List

import pygame


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
        for i in range(len(matrix)):
            for j in range((len(matrix[i]))):
                for k in range(len(matrix[i][j])):
                    if k < len(matrix[i][j]) and i > 0:
                        if matrix[i][j][k].name == 'cursor' and not matrix[i][j][k].is_text:
                            if len(matrix[i - 1][j]) != 0:
                                if matrix[i - 1][j][0].name.split("_")[0] == 'line' \
                                        or matrix[i - 1][j][0].name.split("_")[0] in self.blocks:
                                    matrix[i - 1][j].append(matrix[i][j][k])
                                    matrix[i - 1][j][-1].y -= 1
                                    matrix[i - 1][j][-1].animation.position = (
                                        matrix[i - 1][j][-1].x * 50, matrix[i - 1][j][-1].y * 50)
                                    matrix[i][j].pop(k)

    def move_down(self, matrix):
        num_el = None
        x = None
        y = None
        for i in range(len(matrix)):
            for j in range((len(matrix[i]))):
                for k in range(len(matrix[i][j])):
                    if k < len(matrix[i][j]) and i < 17:
                        if matrix[i][j][k].name == 'cursor' and not matrix[i][j][k].is_text:
                            if len(matrix[i + 1][j]) != 0:
                                if matrix[i + 1][j][0].name.split("_")[0] == 'line' \
                                        or matrix[i + 1][j][0].name.split("_")[0] in self.blocks:
                                    num_el = k
                                    x = i
                                    y = j
        if num_el is not None and x is not None and y is not None:
            matrix[x + 1][y].append(matrix[x][y][num_el])
            matrix[x + 1][y][-1].y += 1
            matrix[x + 1][y][-1].animation.position = (
                matrix[x + 1][y][-1].x * 50, matrix[x + 1][y][-1].y * 50)
            matrix[x][y].pop(num_el)

    def move_left(self, matrix):
        for i in range(len(matrix)):
            for j in range((len(matrix[i]))):
                for k in range(len(matrix[i][j])):
                    if k < len(matrix[i][j]) and j > 0:
                        if matrix[i][j][k].name == 'cursor' and not matrix[i][j][k].is_text:
                            if len(matrix[i][j - 1]) != 0:
                                if matrix[i][j - 1][0].name.split("_")[0] == 'line' \
                                        or matrix[i][j - 1][0].name.split("_")[0] in self.blocks:
                                    matrix[i][j - 1].append(matrix[i][j][k])
                                    matrix[i][j - 1][-1].x -= 1
                                    matrix[i][j - 1][-1].animation.position = (
                                        matrix[i][j - 1][-1].x * 50, matrix[i][j - 1][-1].y * 50)
                                    matrix[i][j].pop(k)

    def move_right(self, matrix):
        num_el = None
        x = None
        y = None
        for i in range(len(matrix)):
            for j in range((len(matrix[i]))):
                for k in range(len(matrix[i][j])):
                    if k < len(matrix[i][j]) and j < 31:
                        if matrix[i][j][k].name == 'cursor' and not matrix[i][j][k].is_text:
                            if len(matrix[i][j + 1]) != 0:
                                if matrix[i][j + 1][0].name.split("_")[0] == 'line' \
                                        or matrix[i][j + 1][0].name.split("_")[0] in self.blocks:
                                    num_el = k
                                    x = i
                                    y = j
        if num_el is not None and x is not None and y is not None:
            matrix[x][y + 1].append(matrix[x][y][num_el])
            matrix[x][y + 1][-1].x += 1
            matrix[x][y + 1][-1].animation.position = (
                matrix[x][y + 1][-1].x * 50, matrix[x][y + 1][-1].y * 50)
            matrix[x][y].pop(num_el)

    def check_events(self, events: List[pygame.event.Event]):
        """Метод обработки событий"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.turning_side = 0

                if event.key == pygame.K_w:
                    self.turning_side = 1

                if event.key == pygame.K_a:
                    self.turning_side = 2

                if event.key == pygame.K_s:
                    self.turning_side = 3

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a]:
                    self.turning_side = -1
