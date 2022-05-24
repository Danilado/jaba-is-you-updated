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

"RynWXZFsbm5nPkE13cCF9yZ1Qslar4qPFo2te55iVNskXbblsz5rGpgBdvnuyXKs1zjzzF6COyGGx3hMxN4RjdzPOA35xk9XVUCgAroJqlj8lWf8s2WRD3P7heVh071SGUQdJGjMjz1xa5DzjZ8ONU31Q9tXAjTcN5UngRnIXGVMiVZYVe4TwyeYKfs10TjhYNzNSlAkNypMCNe96DAmJf9gpxVQM9jwLgA3cJoT12cns6F4kIZ6L2nbVCZpwFTJOthUiOHqLCVVCLqQQ5IkvcMBHP0HTmYcf4WkkN24x4GJX9nyVIaTilXnOO4eLyJJUTMwNJQFYcYhLwjeiGSyTcIvMs6cbzs3DKCqsuogN2nN9gXUG6uYwlHnDhyV2f29D3j7Pmyu0yp5Z11fUo36bVkWfK2SrM2eKgZeVELT5ghsz1iXvuYC2mSAYv9Ry4BPifLz6e7q6kVOIlDNKgosUQYb6U3oJDusjFmlPSJ6tK7yuYGMiOxvTALzWeiGUB2EdObykfpzQaf1dydDYXdIUMTVezQON60jmF08uGF3csKgCeuGJpMojXrS9PToxsAJut3OVodZX6mDyW2lcFFL1xdBYd7Ug9RAUr9yf31FDnRD73Yc69LRbwl5bLIxhwS8Q8XVxyezocvVTaVWSr0NHw9x6rNCcaaAUqRLS3cTxuuGtWwoC2JekfhUlrRLZNeZ5Is5fFACo0buVOdFuoJPGGBmMf2R84hGjj8jtEKcuzmtZMA8Vz2IG6eA2LjVf218zNOvDBw9L46pb2u29Pyyi78r44muT0TAYt1IvF5ez84ozp405QWJKIpNZG9gjyGecxsjVVmYs55B5PeovsKqRTWooR2kgrqLQrD3KvDAekw14AjiVorfvqjHJQFg0JbiKgncorp6zDsVjXqN6M77a3TSlnWY8F7SfrGZs3dW7grYGOSZGY1nKjV5bO1P0uVLx580a8PHfhB7uHOJNto2JtMyfSn8UmwvlwgWTDUzIL9Usd4I3nhoFQ2A0oqa97Jn68o8QJ34CPzW1QsHQLrssX1QDy4hTiYkhfjw54yHDQAfIrSqcCLlVtxW1JiWDNZ6KXnLgNbKkSQIH2MvDUhQmuqB26jHXiYYp6m8O3qU9MGiyTCcVd9aSeN2KCwOsmJpO3cYqphc5BFS4Eh80vClBcO0A7XHqkxK3QEYR2JHpvK6SQ7UurCLpKnRv1UZ92HUGpM7tI32l5PjAxlucdtG1feAAtWVR4OK8cbMxqIYcziAYZQfzZdmQuvdzOlchLyn0YGme9ZQL4rbR0WHcobpIjUogxx1enIG7hBSQGL6aQVW7JHMBKmpLYF0umNL4A8SLKSk0C5djchQ6XrJppguo87EjeUPfo1CUCeUT65wpdfi77o5SS1TmlOR8fQ6zpDKsQhev1qasnebinIkcHWW3S1990GbxBxWGR3Xll5yq9axYaXOEylzK5WKSUyOl5oTt2yyudhnAzbrbMlZP3QJPcx1Kqc1hgh2aUzGtqB2WIZYqjscE8tNZG5DhYW8uLvaeKr24bWOQq3t9HR2mnpeLWqu7UOSnA5LEnwbqJ3fc9B7ZDFj0tDDP25KEkYzel16jfqXL8rKJR8Xl8RSonj64ZrZDaUFjObFT3e224Y3vunZ0YwYCmlJbssigO1JCNrra17fWsEEAnm1Ju3165Ys9QxoJEHqlDmPPUBu7gjP3ZRC7QxTdpjfmUT7k6bDANF4m6P7NR31raL0etThjAOHfQSb9xOH6BRlojbAgFGCLhn4zfRfp43SiUj47cNqoSIvQl61l08WC926B76anDtkqod9g4xD3Y2oAU3nUul5dpUH5J4fONlrNpUpp6Gz9oMMDOfKTUy0KRGjVX4pc7TdCVS05HwNEScJgFlOU7xfpkPSv1F27mtpzdtoY9iiruH6PDU9zL1cqU2W8bGcehNEqxzFODDyS7to8B9Zi1iQzE1W31tBFxfhgb453S2DfkIcICqsuXTux9zXFfIfEPkgBIaiHo5bRJ8KDjtFc2nyx4Yh66hvq4YuQxxYrBOxhl1KnFleTzu6LNe529v9bRj4ZEHHU54ivHIfmqVGXDfPToGGO5lOquzIlw9bsfroVIpM4Xe4Y5wC2Fin7zAFBwmk8pCXgTKS3uTj82d15prUfgzeoE7kNsq9njVZRz1t1dqUf4ZLneScDImKtfRA5va7XYIMuBXBexYFqDU2wODOVlOfkDbckbzDizKV0l2UHBtmnm9XafcIoM4coaCUxd7u0KTzxw3YMnEcdYiCViPJWsGe2iGDI0IflvpVtlQWIvL36yvLxjw3gQgIqYqQ2DGcavHEuG2Xy9rZeRAVff4bjFELVrAlSUzuhe4zCDpPY0qlx2QpETQUBcViZChLnoGmTdSgErKONawgGAwzBatrTkhGUEq3kNEIEJtrlmTtTKndtpLlNkCZ90DnMtrLN6Dqd1SJtcH5ZdTNUDbj23M0Z61ZgC8o0lauKpn3UzH3pHqhiTDIkt1gs7ncXEanMrbKwbKhRXTKJfw2cnEujeHvWXkmGIaboGZw9qFX0pH3i98gIk104i9G6tl3GaJXMs62pFBQA1LRgz3J0gMkgFg1VTt2e6GoDx3UCtS5zbmC7LbkrYMH9eMRkcC5kmUoCvR8rYy7EZwjajmhB6WDr9zswiefNNe5GLXBb9cOLGhkmGyBUNkbkiyFqoVLe42nLbgS2f6YZMD4tuFKRYVLkqjx69GUaVzRTQjGQJqnWxUCqfcWbGcTEFek4ZcsD9e0DdINsj4c2ZBLAVx2T9JoF6jDMHXxCnhess"