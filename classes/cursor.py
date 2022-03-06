from typing import List, Tuple, Literal

import pygame

from settings import PIPES


class MoveCursor:
    def __init__(self):
        self.turning_side = -1
        self.blocks =(
    'pipe/pipe_solo', 'pipe/pipe_b', 'pipe/pipe_bf', 'pipe/pipe_br', 'pipe/pipe_brf', 'pipe/pipe_f', 'pipe/pipe_l',
    'pipe/pipe_lb', 'pipe/pipe_lbf', 'pipe/pipe_lbrf', 'pipe/pipe_lbr', 'pipe/pipe_lr',
    'pipe/pipe_lf', 'pipe/pipe_lrf', 'pipe/pipe_r', 'pipe/pipe_rf', 'words/a', 'words/b', 'words/c', 'words/d', 'words/e', 'words/f', 'words/g', 'words/f',
    'ring', 'leaf', 'medusa', 'mount_map' 'violet', 'fir-tree', 'trash', 'skull_map', 'moon', 'snow_map'
)

    def move(self, matrix):
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
                        if matrix[i][j][k].name == 'cursor' and matrix[i][j][k].text == False:
                            if len(matrix[i - 1][j]) != 0:
                                if matrix[i - 1][j][0].name in self.blocks:
                                    matrix[i - 1][j].append(matrix[i][j][k])
                                    matrix[i - 1][j][-1].y -= 1
                                    matrix[i - 1][j][-1].animation.position = (
                                        matrix[i - 1][j][-1].x * 50, matrix[i - 1][j][-1].y * 50)
                                    matrix[i][j].pop(k)

    def move_down(self, matrix):
        yk = -1
        ii = -1
        jj = -1
        for i in range(len(matrix)):
            for j in range((len(matrix[i]))):
                for k in range(len(matrix[i][j])):
                    if k < len(matrix[i][j]) and i < 17:
                        if matrix[i][j][k].name == 'cursor' and matrix[i][j][k].text == False:
                            if len(matrix[i + 1][j]) != 0:
                                if matrix[i + 1][j][0].name in self.blocks:
                                    yk = k
                                    ii = i
                                    jj = j
        if yk != -1 and ii != -1 and jj != -1:
            matrix[ii + 1][jj].append(matrix[ii][jj][yk])
            matrix[ii + 1][jj][-1].y += 1
            matrix[ii + 1][jj][-1].animation.position = (matrix[ii + 1][jj][-1].x * 50, matrix[ii + 1][jj][-1].y * 50)
            matrix[ii][jj].pop(yk)

    def move_left(self, matrix):
        for i in range(len(matrix)):
            for j in range((len(matrix[i]))):
                for k in range(len(matrix[i][j])):
                    if k < len(matrix[i][j]) and j > 0:
                        if matrix[i][j][k].name == 'cursor' and matrix[i][j][k].text == False:
                            if len(matrix[i][j - 1]) != 0:
                                if matrix[i][j - 1][0].name in self.blocks:
                                    matrix[i][j - 1].append(matrix[i][j][k])
                                    matrix[i][j - 1][-1].x -= 1
                                    matrix[i][j - 1][-1].animation.position = (
                                    matrix[i][j - 1][-1].x * 50, matrix[i][j - 1][-1].y * 50)
                                    matrix[i][j].pop(k)

    def move_right(self, matrix):
        yk = -1
        ii = -1
        jj = -1
        for i in range(len(matrix)):
            for j in range((len(matrix[i]))):
                for k in range(len(matrix[i][j])):
                    if k < len(matrix[i][j]) and j < 31:
                        if matrix[i][j][k].name == 'cursor' and matrix[i][j][k].text == False:
                            if len(matrix[i][j + 1]) != 0:
                                if matrix[i][j + 1][0].name in self.blocks:
                                    yk = k
                                    ii = i
                                    jj = j
        if yk != -1 and ii != -1 and jj != -1:
            matrix[ii][jj + 1].append(matrix[ii][jj][yk])
            matrix[ii][jj + 1][-1].x += 1
            matrix[ii][jj + 1][-1].animation.position = (matrix[ii][jj + 1][-1].x * 50, matrix[ii][jj + 1][-1].y * 50)
            matrix[ii][jj].pop(yk)

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
