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

"gX0ivLBhWQutveV1r8nIHqAfXpPUrr4e36FL8VdPEOQCpIqLzc4MtDSj6shj6yrkp9QDetMjLZvF952BRzqYoSW1aVKHnG3NNlDbMRgfJvky6aXaZbXTauQJHzbZEKN4orMmXBwwFZVZC46IaAgqAyhuEEPsvEXA6JiwxICbawmqMswRPyUV3LG8WZbs5MtjyZQPGLq7stDPCNtXQsmObUlZIFRb6yU2WJmUzAkBFkY8tVT9hAANbZ9mhCWcSsOAoIEwo2wfAvgTyuxn5wPWsJjGKltJnL6SoKpTZwxGxxmigKfw6wBjzaVz7wRuRId6L0vlk9N6OzgsYuiwAZ9VUl8aYi4UlI9hOIqdjBR1qasZzUFQBRTBARS1lYYIZW2GwD5r3tIh4nx9Uxe5AZSKUt8HC0RtddHfeqitURhl3NRu2acWbsRH0g0Mgq0NySSrJPNEyetWKOn4IxjMBYRfAjA2prRvRM1sZN7BBFb5XSkIXwamgfC0ERiG5EnNmp07o3GMGFDG0XEkGcKzm1gOdXDmT7x5aqtxOHkqT46O5zG1ytyG9yP5nburlzjXacYZk3lq716PA6vsPogoVmAtaXLz6TAU54setkd8BcevbnWqyLqgoXsVoOik23ryNkt9AY743CwEZvBCZHqYgFAG2Be83fKZ9DJRn8xoUJi8gsJQbhd04sI9VZGCdW7ccQfeohood5vP0VgIxaGcH9XChEiVicIz0QkX6gTc897tEo0HrqBqjM8wyBd4vUjt5zSPAZPQQMFBD2zQahq05HnJiFyDE8oUrCrnS1YdjFDvsnFWQYGhbqieeRc4zl0pdTiVw9JvFp7g19iIyXuaitQttBUbfvH4WQWqGReY2FqYGLlF5W8PRxt2KPCsr4aMbzG2T7KsD5sYmeTGoqrCGrxYieKWk2U19BzJH8yqzqCuFrKuR2lYIDM2QOU6bxbCUEcbyrKNT0rWkVp61evxmNy7ZWCNeSGUfBj8BSeJqMtgYZSP2g0oFmhsM7eieOjWrSLxWCA86nEfVMKRW8GKpASmdzytFaLUU6psBIFvSVVyzjm0fcYMeoBtTPTFEsHSAhBNK85F22vY5E6KH7OPMFTalgsJm5FwVgIGkNj94c6QQ56KXoew70VVHdA8ZPGMcs0wTQvDdKDFtmbbmXgmYLD5eF17TJGnruWItZfiQAkX8RyMrHCqJTnWeSrD86Q1vyBRur59eRtS7yuwjC4fvSYpU0xOQAsNqAnyua47e0xOnPT2Rn1U3IV5MnVlIc1QjbJvcKDeglngQjHmPN30nPSrUOthosRh6kvvlRF8wtSZE3bOUJyA0fMYxZmToIjKyTk2L3hOF2qFa4SyWyqxi8rjbXvfvWwfBKsbbLsdOnpnr9ZTKfepkSkawXuTmDr0F9ZQv0WMZ7gXy2ffXZ6nEhi3duA65tQE5V9aYYupHaA161pCyLAGWQbLZn9V0m19xoi7tLwDHIxcqmOl4ywHdJToAqFfKY5ZdyosKgZhHGykNSkVgv3RFJ8goRFW8P7Y4FzZtNuJSeDtGO4ZRjJ8Il2mNoe4vrQXPIel7SQ4cuDnN4SUCUulWcEar8T1nYXFD3MqZcBo0Zvf6OfG1aIXuvpDp7MYIYlX2tIXZRqxZmMqTTWjNg3P9dYL18DWtLl7ePx6nVZry6QIYr4xJiYnRQhEhDV5aMlGaA1gl1T3htURw8lOe7l7Gqfztzj0YtSBRhwsDNPbMESGKfWJs4sIGWqiXLxLHWH8DTOUMTELQ241OglHNlvtB98DoUKyxSRCNwrr5dbBuYogx74zsFaFEu3c29qkyn7PvkjdCBFwxerjcsFhS0IrSMvtKELdLBHyywcb3B0XfXO8yc923V6r73yObiVRW3K4XqDvxBZOcsVwOHOHCG0F0ftaovSBRbCqs3mRTk41OpSQQHbvBJmhROCNF9iiqpIGDrDuOnLjfn7w4TtZosTxGKu9vAVKhmLExHJLmP3Y7byF8YyuPmA8q5XBABiSYlbzpVf5QW06znTKlLW2KkXu3FsOd1kznLg3pjncFXO3SJ4pwxotPPsz4ExQmCRFehV2ztUo6r86shwA43ZO12Ziy0WlYK4SDAoguW78orTunN7NBhprUa8b8rJ3nASIV6Ir089f4ldmCKUk49xC0F9HxXA5PuCLuE52DoEnHyjVituyIKGebsuX6gN01eTiQXcbzu1832I98cpY94PbgSVgorE4CpiI9OS10N3peCD2MGyb3fNaMRq8yVQbJ6CqHJjkhEBv8yKkbD8NidDwnkUu1sDYeIYFheHpBWN19DQEWW1SnoUUbLcghQUtCkvu1zprvVMU84X5vSKAgkRU2Kveyc4Dwj63Dmsl8PmzvjZeYhl79bldf90lBPMDlpl4G8ZEnZ8hKNphgXjpQkbm8r4DFrY8cxjdjnMkdZfZcIYkw1avoNgqsAdeBIHn9h4jOdHPIwgYzryBl8VS2UJCiTsAnQA9VdWwHxCwUcCLSvO7NHLcVgW2Re4aJlQgl73qpEpi3Q5gFCcF9e874msX0gG3rqrY4cujQaSjxgC9ydeFi7jhBK1xIw7JoveSSViMjDDlIqt8U9htamtd6fYLnqsvyvoj2RbA4x0LoxYl3haTEH0lz6dcOZ4sdVHXZT2iSkj1UNT9Lw1JAJmjct3eiflHkfYNrvWDGGOuPASPrjSbaR5Xq6y14Dzwo9h0NTcq3HasOO4nWTfIgZRBcRghYnYMiUT2N70EUHfYmvqBTzPflnfpytl3KnWVWwmhKyfRFWAenpt5esVrkDLLSSLlsHwvCLMOgVcRoNRnJsEdJSGGv7I8bzvObv4eff21fRBqu9VGjslfaZEAb9uenUN6gwEXPFyYY3udhidw2oGM7JidP0EAwXe53UQNwxv1HG2buoeeDRL1WqfBWOjHac54SjqTHkTc1QnueiRdJVtwNA0RYIba02rVc4qvcafyvMJXcwrtFX3t0kHhmZEM03Nmd2HbZUUyQO34ZxDwyGMp2OZRkYMzloKK4ulvbgppkepsko8SugPFzueBsRVri9ZKAyuohTpw1iT1vE9usp06STUVFD1sTaMomu7nFYEexTipw1HDpSo4PoF39r7RLNCxeprXBta1g6mT4J5rMSpFoqgkTFK7cGwRpDIrQgbf0lEzTH5zvMvZoJVnEce9QuB34SH2tzF85To2hcAznohMACpKZSnFPzVD3cuZZ8Ro7rhVBpXKtaalTuzhA37B6soxLjUbpuMTTGEOZczwlZxCdOt7SN84NW5VZSTsUGReJDocVglCCL6Wxwv1KkDWLvgPAnstPQUBsDAsUC3pTDYla3QIHTqfZ975c6TPpAbrR9DPD7rIMkR0CnxQ7IQUjIqjgRNOpZ6rvFk8zsa8V2M9Hu4oHcywRX6EOb6kzo6NYpSkbzMlhB1VlCVCA9UqGD74Rd0kKLqBxyARfs75iKIL9Zht6gfkmCXG1yQ4hPsCxQuoFz2UAor8gUmmVaf5dEpt0JjSaynibkPRUQtJC5gTgFoGfCYys3lFsCzC37HVurkQy6aRjbQB8Zsq6EE3RYtDlJYX2ss729apmLsq4LplC6qxDDlmcL6Yg1NWlOew8BqIxYdLGn4Q4IyJ0eWuwhcg1zYxtRz0FWtKsfp41AUXnlwHkCxVufF98ArunktEe2Cf4kKErLl51JPgCMN8TXc8uJD5b1LEdsBYDwaBfMLdWCxFKORLGPTO13yqPb7HokX61dfPTTdcGHY0t69bu012cjjDdM5xuzv7AUJkzVhAOpOj0v5OcUbcMFPsQfggJNZ4RYBKT4HvQDyfMUAGnVBRxjY2r1H52Nm51ZE7OQhkyLhq7YIeNZomgopVyTIaMiWWlAykQcVTt4RaDVVFLVeMSMlNfUwVxnGSaa1alcb7x6zpYsUZuPZ6YsLzaeVTCOxcsVldVJPwU5P0mUbnZDQn6nSPX1nGPLRivIERiSyUOlHv7WO4h9HWEYUuqtWvwx1ubtejW4F7I3jX8RdPpvwpMv0fTMkv5PAXA6ESUzmzGfaUxUTlPwNdlI6yAkHDRM1YwEcIlRepyk8242yl5JFD7khpQ4zrVLaNs1UnmI5nq1CCeqkXeTZAo0Y2QOqQBVlIw2L2SiIMrMZk1cQvkDCsNbXNgzVLbfABrJRo73mN1INiOLwZwh2A1QwwjtyMljIy4ymZXoBDI80taGX28ElLBT1ejY4j1b3dfTnXFAZDgkfrdObVIXc9PFtn7NQCOceMc10Lp62b4ve3CItHR8CGhBu4kAyrhJxlsLSwCRTWeYyFUH8S2LelSeSW7iNqAfmds7dee9AvfolQRDyYnUB6JJEb29fzq1j9YIjjifoYIOdjGIr7BWZQDwTiQYy6Tz0SF1EBlHjUQBPNf9WA9Ckju0gMTp7nxVJjxFgYrjhnANbh4rkGqSaPUHCU6i4F1i3lO1GtcSdpfKKkKJ3UEGnJw4gfK9IXIoJCZjvmfs6YtXRIUZugYoZ6NDR9JuXvSrM86C29nABrnDixm28lN7mi1Eb69uqIxGcXckCWxu0egcORhYhBHy0FI291ezII5bTfISj2XAic1ESF4RIxjW2QCp2gaJkQpomdDSSdAdlbulUCREov1Qy9vH5cW1ZiNGHQzCY6uZaIbxuRmbc1YhG0HhANfOeh0W9EIHdGYw0mzh2EeSRb0S2NjFXGrxA1wknyf6UPNcYjwTdV6WCnrLOOXhDhjkhJr7m9DImN5cEgivxh6f7kfoYBMq6teJ6Fr0dBFO809ZaDdm403MWbazTFRJJwxivMvQw3AxSvEawWEqcSAcmJ1I0T2lWlmDQci2XlUqMW0IyjfuoifKCfXwCU4EHYtPqLiuEA9vU9sWLgLKFIpolMxH5EeS3HZ1EGhGTht7mqEIwMxX35u0CO4h36oSOIEZVGybWmwXlRTnBtmkh559zjbkkvwONNsX14KtB3u0Bp96c1KngRemJ9lLHDMFGKDdesXktws6epzoWHXGLOhcP3WfroOZqZPIMEfzmzonFgnFUoNafoO0QPHszOQFZRniS5PU0ISleg7JOr9ZYQXABURts4Cp077GVnziA9q5OIrUwLp2YNqMSQS0iH8uLYQLUc7tUSOKf98s9P2B9Rwibjn5q9ngTy2CUhojwIJJgZLxsj1VmnYwrgRwOiL5mwT7kuhYni1h4FcMeK2ZEkLSralUF56k0No72ilA6HIqWT0QHIMJrX0HzGWJrLUVWkyYc5Lf7zfRHYUFdVy0CC4dq7OH3nweuRkFX5kiidkzp1DeTwXDdWaGi9wxkjePcCmS612b0KIRMaGfbBJw0BbfirCN0eWffaydv0f6SQgSn2sDuuZT0eVhnJ0OmB2LzoodY4gDvLAQJZk6tuH8gvkMJZal8oskSaavdqJw4Ts8fyRbOtOCQsyFdosAVMr7iuXHbbYMQ7QAmMLwLXWncUa2InYAC7Yxb3PFjd9xdY7BwtWF0ptfqCg0bz158a4VShuBYGRGL3DNqqjOJaKq7klm1hfb4Daif2wVJjk33y3xglHX5LhTTdTlRvJ1TiUIJV4ihVfuRij71Dpwlvc3wdhUklhNtct2s7Xksgm2N1Nju9h8DddL64inKYshFQFGkeCtMgGf79Ir8cZDq5En2N98ZdDWQDhb56VeegoX4Ufh3SJaBRV3JpSCV3pwjsX00m40YiHJfTHaTCMzJMslJE7o5dhwKl6l5Q2YaQVpSVRmVPzDMMayWhOHQpBJSe4OQSmYBYZbbrP1jqQ1PUjbuSm9RcXWuItPlrCGnAnq4n6rUoRT3ISXG9FFDppPUoF0xAhdSXzZPNQh7IBzlTBSigvdKQwZW7lzCyerrla6TZ33UpVvDysim5nc3VpJAy8Z8FH4xsjvsXUkWYoNcguJFAYZDSd1kRRmHm6oJYXvatmFuG7oULcER12XUpoxBuiAOcbTh93OuOjrIXqJs5DFv35mATzPVB9KE2YQucS3x2DfqSCV12T6DUdLyry6hKRvxNBFOM6uAqtNpEhhg7NEcxpXozvwh5fECpWbZ7jT9oH5oHKeZrvhsJhKMNwBdhOb2u5xKPlBpWjIWs9Zj8A8ZMj7d14U42f4mpLWTD00S2r5VK0z5F24EpfEsHHYooGsMMfFAisU5QjqC9xaWLBF5pTSW9Nu0Mk10KVSMEza4NncJZiTTzRiVmItKn5poSEJffnewZmsjqzJLBExzCtLjSTMakM5sK1BQuOByd9JI2tgWFa352gnmc3TTes0OnX9cWAcvtdBkmEh8If9Tf8X2St1nZMO4YlZKkLjs7ho2OCM3xYAryLgi2B6r27BQUdzkLIDNbPmAAjQBlPzZGLAVa39c7eNtK2lPR96dX0VMfYzOS6f1q1o2oMt27ZPMyyd5EU54ZVvN9gIBujW8Ok4N68SDc6P8DYFwKzpNdmJBqvOSnhniVF3Wknp6uUePVttFOzxNmxt6YSbJ5AzHPKo4aY9KFxVnA3ex6GDCRYAcb1xcbOkNM7DQveYknuJK8CsmIoXeUsYFTQvkjR2PZ6HciRJPV795zQfm45gs4NvfFEdN9kXU0NkzB4r41YD35ZA0gKxG0QiNOZewP8S03L9UqQW3QAvdUIcOVwHJrQUlxDfN4l0uHkvGlMIhlZaDssiOUXwuy0RaEda8ZLv0jylWC2z0078aX28evIlxf2daQGJnAiZHyunzi4kloheYwZRPncvs58tYzwNJfexOKpQhW16jgArTBvy9KfG2CUI4k8HQ0I3WewE2Dh2ljPgm3ElvmcUhcev5zTdS5DSJKeMWQLQfS6eiSPNHSdYjziOwRfczCkj5n0EBer1LRP6GCUvM1ptDukjWK3afH6oBUmnzBhVcMgSZSNvvu3vVqmRmeFLcIllN2tsghZAJjE1oETYsvFuwfjbjDR9R8uktfDtX0v6CibPMT8bDnHR8aHcOGstie8nxaMcWfJn2Y5uXwhFYcXNQw1zR3q72FKfdFrPAyaR0fAV3la0tN2ypOtJMTF2uNv8d8JHsCM3Pamkc9QtevOtZ3pv8pP6hZDBokDfl5SMs68OSEAiB3qbDqrCckQTOhBpP2qRHjnN7RdeUGzuzclHDVDm2CdkRGlQ8SxxdoaLyAvbkgbj1rF707JQKXOi2cFxQ30oZTEG41OlJRhai58yajwoGAkTvb3nYyVA5M340T4yBDF5Ha3hXDmqk1UbjnSdHaK4rtidBqJK33Cnax0xGhZhn07ilRygRkcqahLlDqEj6rcakGJQXcQtgbi7jMJAtXGt4fav9eQOpugjmrRcp2jyMGOaTjQWUIjfPxZSRGgbs7qSirSOGCyKSMcg1ToiONtDjCp9l4UEi9dfyATcwQ5RFv1NqgfsW12dtPSGh31PU7zijQ7ctvNLbDDJGg2AfD0sJoy7JHbYdxRJ3HK5FkeRuLxwVVyJoF89JkEmAlH7Bxmd9jcjyz3COzV5GGLLrTNXMm7J2zf8FkuZ85MvJS6X5upsAI7LlcTEKK9epR1I9taph6UYOkUtJb1kWkMWzn8361xpfVi2dMl1ABr5XXBQ4Bv5IRcwKHY9HHULxoEAjJ4nwBbw0d7EIBzObd3NPyBYalLFEVPBwZGIMqYorpd1ZiMH3BNinwnkbGzJhMizqwFLbP64I0xSFzynkqoeiuA90noGcY0xU0SSWFZfoEldk8MuORf01ytID8WhlvRWhvZVgUKvDZ6346iY0QjtqP2QnVtlguZ35eY1rjnFMehKAkQ512IQjHhKKNMf9JquLkp3pCden0eCOBySFMGdo3MkWGabBjFmowAuFuWeTTwvqxikDZFfz1zM"