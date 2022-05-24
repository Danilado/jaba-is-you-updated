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

"t3yjwlBNeTWy1jYLiqewQyerA7yb1ZYRCo3pDX0EG2GclpM5RvmJ4zzLugHCaahKkl6MLZeFIl6A1SVKnuCUzN0fgVpmfT2HTV7cf6R8Mir2hywazY3Ad34PTU7z8mdGZXazYqsC3ffQrvfKk7HsL8TIZzCYv8WoWtnI7d4jtIon0nKHd0tkwNK7ZhAlqTJHfNQmNrtWqvXUYisZk4rTthbPTNjXrGn6Iy7de3dotiGRtKkcLGqGMHG840iOrTJTmCLuObJC4aWVJETbrRFaJRPC9L0qfiOouwAsR3hoXQ6PJYxseRE7WfDLOqJZeGYa3FTTCbq3wrZir0H3uwMOflK4aLVqf6C9MTuc8Hj2kJJEBute7t9kPYjLvaKZSGAg3It70dolCSDDB6VUINckwWlDZ8P8mPValHsnh7c5Hl6ehEuXJOkzykSS7KvPzWQahUGfsaFpDODhIfGhiH2DHoxI7pIzHs9x3sUMDyLYRi5jihvAsUlMaNKwXoHbiRyaMBM8PIa9ZDYA3LVb7b2RIAvSztoeXQL8j8pa8YI1INqymIUIRV9HXzMhuD0Prn9cWqjbemrJKkbkbqsQwkb2ACfg8LRi2N2idPsmXBHYo6o1D0Cy6THgRko6AcPIcYsyLCoocLcV6TeCV3MOICNz7BWPnYodfbj674BNyhCYdFmeFRIlAP2acRGQT1gYYdq0rLjjWsGCrYhrddtF6Iz2v6g3xHjVI5r7He6h6QzwRwyclfmDfLk9QKwhCiyJPw4iWlpTEmcJsyU0rhLkZHxd6W1dWRvAEM8EyB4mpb4lh4JXKGdmkq0NsbfOBu2eICNel8GMTQz3vblouDqLWqfcIQVkrgL7LHz3wiZ7mLWErt4Kqo6i6nAcWsXqSa5y6csrqui1rmro7fz0TIxrEgQY0V7FIikkhGLKI4n2BdGpttPwCGhugL1AwfOuQDIgXuiDkaNZmna2q0DG67XeNwsw4c2S4oIzelIXfuHuOQ05k8yQjQOaZqveO3erCv8I9s2NZB64ZrNLquineTNok9PkNMb5y1kmOYr0sGFqHGbddGHgpoXVNZvzTOgbFwAS5LDOtHYhO8hyRSyR6J9VFuvqnZXqwXixeqrtVZpE5vGJQuvZCh49To0sO4ain4JSBGefPxzahEdXKlgF6jCY9ymb9sSgrWfyaJ6XunCx4nbpxrkjAaXcEkrqWgRfj7gceqk7221H26qnXBfxnIq74ePmCxYxVeBEXR4ecCh6M1QIM9fAkxDY1c8tuk4RyVSumG9Y3wsKYbAJZB2FSaVSnB6d5HudsuHkGHHlnn4C6aA7slD35NK4nuIIgPe2CLb7viP553ADDlYDSSkO7TerekvvpVuGwHS18H8IqweNrbjAAxpUCHTSE7Ec1qHqcGlYjMIUW3q4DDfZs5BvNN4TJ3zSA9mH6RzQT4l6e3Z75uUFDu7fz60sHS6SfYJHurWYS1oZR0HZxdx1KvLdRh9kSwIEnWbptWR2Sa1OTQsHk9FF9t0Ig1KJmZy74aCeZJwX42bFvEf7xGyuMU3B29X09quGihlvtAwIUaWKpeoBWz7UPBk4qKngCWPx3k0Z7jUaIzAZxebYNTELYIYQV9YcDciCC7BBu9cgJhpe0FaDKfZo3UEB9eGdPwBevY3TCymCguJo1ZC5KpHXFRGjqicPvqylXIEa0juJFDZbWSYlnzSqARZjXwgoPOAaZPghNTio1Mj9UR94BfmY7DZqo0ksEFlCkAyDqORCawA9LukcjdV0HIxlxdGNplI0BwZpVLJadNaux82e4WM6Prsqzt5qntYxOSxx3PuAnXpKMTK9ZIsUfEm3l65hGsuYaxfOkRmtD4dcnYdi"