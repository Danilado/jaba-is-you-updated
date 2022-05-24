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

"KUc8Zl0Lpxorq9aIp0mL4xck4fbh2rMVVNsVCuiJ0pskIOcz5Wy49ZLzzgo0ijUtN5RoUVEvDQ9HbLzIFVgtfwDJdvXF80TrEoKCUGV9SjnMHKwYwpDN7AjgHUc35ADUjtDJqnB8M4fB3GpbXbWEwUwBYwz3zghm53CUu4aPKjfZpDAIDu4ioVzChukt2jbdiLhCoh6GkmeYHCwErawSiv0qpzQDDkggu83zhpxXQxq1EJiq1hq7N6oPvPU1OYSXziKHcjD0188mgprBXB8LCTxyJjmT2Dgcdoiv8SLtxirCUTx7Wf2X2Qwhc5yXfmbKyp6HJW1WKfpwB5fupXRKiwVcjXdXIFlewwNmlj6xjtORZCRIUdYVpmDhSj5b9tvKavMXQDMv2Ox2w6lwIu9jCov3D6wKAZ0XTp1iiDNBtjoVeFQeUar6dzo1HYC6BEuBOIr6KKJnjcnKA8hzwaM9FkPg4KmKAsSZKk3V4ul95DkJQhbM2zCBD3VjU9diTvqGeD4HQgVth2GNZDfPNdHnCzet2ssUMo8YTVRAilG0veFY8tU1NsiTS1vwQLrI3Nc0HS9VaDtrua2n2IpL4fUMHjIyGKdAbhY1OApuueN8OsyV9d45mg57qxaufMtpgDPhFM5G5uICFUUttKjokcfu6eBxsbWoBXQ9XMJ47NMYMoIAQd0dVGUuIO1TCdXK57lxIBlR6MSUzpUAxmkXnmN03aLLC9VpnIKWieGXf5cjq5pqSAyOnYNsBJZxBz7m5BO0Dwys7rfUYW8WCXUX5s7Fp1mDNo8OTPujy8ZSArof2Qsno8r8crV6etCPKdVolmTvXBpyx135kQKrCs7xt5UDMMghmQgwySf9nantGOJkBsod7iW0ZfuuUZwbzvMmIdWYgOt2o1NqkJolMx8EtoF7jKVDZvsW2GfYhg0zfd6Yrbye7yQgVII856xQOrxwEV1o1IqPtr7HnmNyZ4DuiEl0CihGVEnMb5bGWrkKVc6r2kASbLxAgLGeRErX5adp0VwJ8oBVPVIx6qNKyxT3TedlzG7PfDyKY49lneZbjKpcloufNpNk66j9Ep6bwbOGmK33SKS1Snhb53DtBkxXUwhXCMyVoWCZUT1ypgspds7RpERAAsIvWgyyTjf3VsPTEKaw7ZigSWTKlXzqe47d5SyBac77gUCunXMd3EPnR87UYTMpEmRsbaFUmFwBWNppEjFIoNLPcMvjan0jdduvC6gV5b4wwLimEwucnZ6vy8jd2CkSIvIfsEA9CRxHK8EXeDQrOSFMCVZNi5kNBAR3c56hD3nC4b3I5cfamWRFMCZIitLQmhkD3sNfmzwHJ31E3Dct9maj5mAD3hNWxVS7gHavdu9QesCPuegO4dbda6p0ZncUCuOp9NHKJNtMg7zJONB9s82s67iG18jJFzsAzTPh85luqyMx0GgYW1tgXw0x0HaZirXPs1Vupw6bhWIDoHV3lFGVKaWUjYulZKxiidxSjhzjr2njIXyd9HtYf03hnswpoJZWgXkamewoREc5jrqsPtD1RcmAldITGWftGbJDiPtkUXytQGzj0Tar18yvcKperGZtUp6dsUh6SVfa2zoSfI1BI7aqVdCr0dWtdQjRYidy1hfVns3fU0PNUY1VWFMfsVJlT5lFo8GhOi92KJPHJjEZ8yplU0gRUAwZt0iDJu67Ez2ltipHWPM3kBKWw67TFPNwIu4lPoo5nKYzc4ZMKZ4G0HjyJ4xt1yUTsQcbtUS6g1sxo85ByqqYkSFSWiNLlvq4s1TeUwACm5paDAf9YHS2HZ3G1aW4oEMJx8AZex35xlX19TMH3UPVKoNybWnO9O1yj5qoTOzQZHOytoPmuC7E9UzKdBXTfvwKm7AytCquhGWsFO4QYj1BgB80Ys0FL8LnO6TifeSAAKsB6pJkjRvNY618WoJPcI3R8LcdChhpEIUHU5Ho7Z6bQoDwpOVXyCJAlF6O7WFmo1Sc83EMchWG6w4u1fd8vnfPRoCtWBmE7i08FwQICwqI7I15Z4qVO2HtPGQ8l0m5R5vmmr1bK8vmjuirGeZvA0rHxPux2GTjF0SvHkNA0RcMZg0CWyDPtKonepCiubiaz2JIShJZFcccW0U5mAODrsLK6oQvIsG9nvUA64GwVhg0fpBq1RSDbDYixcBhTViOp1OK0Gm6wtyBPdGfUrCGouAzUZyjOH6LHrXQLF3xS0BzvYfF4eqbbfYZsNuElFt1FbMmVL8fWJRigApOUQJRH0oIrqPlf4ptUzPageflFMDOyxMziQJPt0xODu5vDNdPwUX9wbZj2VRxC6XcUfPiGfHPn9KHFzTGIJPTR1VxsTIVVf54jdHXoXkZMt1E6zXD2wip1uEj1ebusmCVt7kVYZs5kYhqPAzMhK6HMJkosplsNPoBneBeK7gC91Wlxz6UXLxw9AgYfJjL33wZGAyTqJPHPK1ANIsC0bC2HCArCogrAQz1gJZJ0POWDVtGzimUSOAW3Drhg8OjgQgFqmnV3CbQhk86iIvbFsTyrgSkHql34Vx6zo6XCJbnJOHqrVcgue3a6sxXadd92xfPA24EuhqdjHDQTl4Ry3knqbIqWFbW2PfjXrFRbL9CJJfEjAQZHElME6l9In0kV7ueTUgUFkxgzyW7jsFFtt6arnecv"