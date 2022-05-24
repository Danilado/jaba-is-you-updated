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

"yYf29f6Q0hc7Ryyc3sROsGXoRToavEdisnToON1bEW46QtuZnF9IScn2pg88nEdSt2mq4rrz4epYZE6jJa0hu3ezdJznn4m67Hy516RgogHQLEqlojoR5BWZN5Vb0ajJDDnpOyzvIYUU4K96VLEzG9EFKB6PdPGRQWc7KYOKLwbK9L2s0ig34JC3258oCnovKVkOFUJzJpedvsN5dx2Q10TmWElYbaVvbZtV1qoUkj85KiAJlpoSAsQTWrvW4ykHwaiH5bJN0LNnw5PiXwf0aNHWnLAdaLcxcvUQItJjQCEQG5UoynY6zlvNyq9JXoqytCGbJkiLurOJfy8ZPLA8LqBcCDuyQP81z08WTEjcI8dRhRZVomQcwTUqLifTTcmMzXZEFkKHbsz9o6UiLNxKWQPDpRE88N7V8pwtBsj0Xl1hpKAfjybJM0FpBBXrmRWWoHk6dpvHxTvm3WjEEoiz2uHvus6u2Q77NJUoSO3DauCMbmvcwcRjFDZlymHB1A4CQS9ItPhthG29cWymHgJhmXjA0kRdI3IYYZVpOGrbHGVYYSoNYiDbxWDCmgO3ul1r2xKtH03xw5dHvrtiiJzXmBDWA3yut75KP3u0m1T7qwCNl31tfmo6v7vkIoceVoLNUKTk9iDY4e26fJDpBFV65zYKQiuQs3oOfdEFiz2vT30LwdioVZkoRLjXXDJKnL82LAjZHWCnhNq9N4BI82o6ChLrvNV9iHKRqcwQmQEgWl7Zds3cEOkDAMM7kxsLgCM5VHwxLvi4pOr4ljknFsyOMxnDuoBEo1rf0C3MTrPPzSMWgyI12f8uPh6Xb3VGJhR53VF1rWsnHRojXDf4aOUd0hf7mVhTm0Sgyi1AfTAqtpHhEEuEijLi9xd98n5RzNck8575mZetN9Ds6xvThwy5vxYQL9IBXSu9CGdHP5E0zfrb3DuUCYezVhWKLPM9hOA6IwVXQglh6Xg3tley8UoXFLSuutm1U3EGPSzsvgyMMINEEhQ7ATlrMTLtNzS8B1YNOEa233PoyJjbCVC4SdOK67OWi9cue1sS9GUoIMTtS8rwSdbjVb1SUHuWOE112458winRqZEGM8fdIt3Bq67tVL0cK5fbhXVJLHBZOe1rEycB6JkSimVihf2v4RC4I1NjshH51nKlsyawYNigVFA48pcbKQTq4ls2wVsqtRja7QG2KBgwgRhxIkT8xFdI4v17YTMbbWUAY6CaJvg88pMiX32aStth3ZF2QWIXY8TGXishR48sfvgGMAL2ZtzIOqaTgs6N63CSuSc4ofZ52x9arVvMfVa8Vpyy2qUwcZ1te04miGIREy4tjRjlAcTVkDAh2CTi033v8TrUY8jgjFPsraUAeWzUMraYVZTEPS07wDo8nvmauvmoQpD3J2na26BvC5VjHqQ4V2IvIR0UPJZ7eqxQ3wHHS4OcTWEmcZzA2oW0ndII4Tq90NpihHNo8vSot7T5IzmIWG49i3X6j2KDQNWlIX3GObrf8KyAewM4jPWoCjsmTuF88leUmLTA8dm8LRNuNHCMKLHCpjo3hPsvzOzCGYxEhZXNvviV2ec1IMa4c7WfH4ouZt831JXTLIHrIGSWCw7p6j0NFjVE7JYn370Ar8PR2FQiqCqCsDIhD6qVfwUozStzYfEgqRtldI7iBSAOC9nUaUT95cdUBQNZFpR7tPEkWFWzLVIJE4nZ8z22QjWfl1Brco9zbXomd7JHIReRwjoUoMxC8bSfhO9KZhx4ogZSQI2UGk21I9YNy3O5b2tw0jZV8j5ljrYcN4CzF3KYnZRJcUysrfjJARt1ZhtVfFEJXMgsl808wIB5IVb6eVQfgpDO5DsugjQZufYlMxCX5yPGpkGwSSdRb91CUGrN3P2fvGuo7pMSnPT8nAsi9hMj8FeLW4PnaW04aAVd"