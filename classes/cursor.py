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

"hhg66VxuEpWMyAuxko2ih5qidKaZk2tvwnMVm9aZirMi6j90yuAtc2o0csDma1jESu67q6cB9Q12q9OMFGkucapQ5SIHyYXbYVX3zg60IxYqdEp8K3CrKdP2INPX9tczrnIQf74xRGPyEtx5ZigqUPRvcsCMvaMIurUPH6FAcIrX5NGyZjKOC0aEbysD9N9Ym3oJMyEqtcZveK0dPP37jfCIGk2YWjZQjs5WfrH51bMjmo4xm4zCxrg845N6rdp6q8dLc3TOyjd47IXbD2qxPf15JSWvKZ7xMknKIZI0pLsIQwGH5AoSjjveznU4lvo94AcbL3nMo0b3IqgikdZDbK3XUeH5Ec1zaDA2tIGfpcMilP0ri7PnI80moZVUfh0iG2F6XOgSS1WPyAE1mWH8TizDWnnCvVFpWJsCldy9WN6TaXswKKZPVLc5779RCOHnHf5gJ55Db9Emn0AGLrhNGZbzXusxaIQ0cG7PjPYJJHjCKTi2HQ5G4RyzwK3aNKWzOItnRLTYcOAOreCsGffWR4p1lIPiToirDaH0h7fkXuGDwgq1nY85d4k0O2CP81DV6R3etxX6SueboxrbCKm9y9luTpfE0r0bquMMvKaYPypbNqfnE1EspYfYSD4Pxs5uXGdujrYz6FbbPpVT4dtdjsW3jdrNqj55HfNg3qfohDhSnlSuWzHZKpAS76k57Th0cURJ0y2TivvcJ5eTuCCZRgVu0RfhHltleF9SMlqpJtVVUVSWCZK4fyGbGfxd2FG3eW53b7UesrWJYje0xoQo3SRQnBc79LqkVtQqj5mXAI379rPSJxzbdXEZJMZZFNtI5iTxMT1PLfG7xeynr4uYojQ8BHKd51NZEKxeJ5roCwrliT11ngmtS59leb2LvjuhM59wN743KnK3slcWLnHb9Bwmq00ZgKapMJvPUodlPWSnqPK7Zfx82ZknYmtfewvfC8ua6ootPXozauhDKaZ7vLPTcPDQJIRSY3WEmcDlNP9uuW3gPfdfjKYFj23VjmhokK2RmlpUhNAO25APMlTevXrnYqd2NpvH6WzhHufpczkr7UiMrAu4j3zkWwnkcBXZ1BFz7XKDUuteDoaW1EKm43ffhV1GMuyCNgRRAby0o0cQK1zNKZY3a0G8u45JnbCEEPpQ0MyCKXRzy7uGIQTDnncSErXhcKeFmoqVSiSZai1G0cQCV0i2aKN3uL4bL8wMS20lNXOpQZJIQNJAjc283f1RE5u1a60zcBoWt4pdMnlCAtZbaIa57Ev2o6k2NJkQENyShtz4rlyovAFklI9W5XJlCQMpJHm9JCAVzpHZ7dJ6X2y04VQwVbd3stoel3vJDYXp21C87texgMvbx9huYXT0XN80X0lje98wr03raraogFC1pvwW39qjTbpasuJqcSXAzqBVqCaGIHh9UkWaA0gxI35jVIjboY4HQhdYVGtARyLFoXdcXroTwertwRrlmDYyVGxqitWho2AgeFb1yoViRslrQVQr3s5tgAcMT7CwlSdeGrbKrhXXm7C2h5pzjfUegcNv2eoYQFwhJOfwQSWsXRWDHu1e0KLrPC5ljIlPkeeaBJjCKENnZDKRKbTWbbu7wH50GRe6WsRKIhaeUWphIvky6vE34Jhpv0zp5vTW2iIswaKXYOsOtnQUrdF7JC1VlzHK1mGqff3pZEMgvIrTFRQ1ui5EaOqA4sJU6VVaHmGTIRd7cyPgTUlgjNIqkZI4BeNBLxGlemiWWG5zNWmrSBSMZSElzebz618TT6FsLjjcg2bVJEo63dye9jO7Z4vaRgyyPjfC4ieehwn4QupHOt6YCJjpXAuf631hB3W2HDsIxR1jzmnX3w0Kr2TfIyIl8MW1wA5AkMJ6QkyjI8TbmFIwmZjrbGzjTbsjeVBomNIR9KNM5yDvkxlIWLbCAsJfe8ch20NTag15nmjOh2SnzPrYDIjKcVOn1bOiF2d0YOli0qgPD6O7zDiCU0gB1nmUb77dhZWLYsY5afu1DXoeW2bwkXZZG4iPovJFyepm9vB8PEGzcnjnDixFDHIyIL0CXYHCC5kSqlZsGmyYuTyuukVnUxc8yoGBlSIOZZf5LGYwpYKMvIO4A8uNdITwkUkUVFt0auFwPrHic1nt28eeJo2s4o4IiU8dwDOFiQYNr0nmer9KyxQ9MorKM0XnYO1diWKG4PryOUrARyU8l4iDy9Z5vUlyfy1pD1q7fkdQnwEJKsOfEVOdmU9XydTrNXRS00yGh2eVVJNNVTfoyCDzjdzefAXKsqQE5SowKlZw27ZzCxZac2aqj7kF4VmHxU4MUVJoGamSr4ZrIsKPu2ghfEz5KiNArLxnS86VbnobzVlt0zNOsxHk668iI16gdk8iGjvJgG2FaoQxpU8ogNZwCj5T83ZjQbch3m8TLAlDXyn7MUewGtIR0vpFhYaWjv72bTF8wXsCYGtbpMqVecBRKocbWCgaUMp9T9juPgxmgktGWQK82DYvnzRr41NqraKbhU3DQPTHGSaFmSXWM3Et3jLnJlxqQcpRj8T6FGqfak3dqZz7k6B1TLjyV63w04AYXc3mzPQa4in2RZhdxArpICyqrxR6jKghmua9PUy0dTz7QLG2jtb8HsEyl8movzvKFsaT8W7VEksHDdc6qvQu7ULJaVcuw5a0vM6v2od6G5zsbHvAblVN4OYFcyopCeWqImrEZFzTGJcnuMqYgU4lkYqPVEXV8uvx9T7auS59btoJldubL1Y5Y3dwnsL6SJZJEBBZ0DIE7f1xnO9VjF2emzdrQ5HPIQk85ulzOJTwIlhzF5W8wQbffaV2Rcy5fyYuMZ4v5uCAzjf1GCCmC3e3BYVtE6KjsWgyCTGtIKzjnIS7NrA4sHVXdBvmlynAGQ41DaPCjbb1vYDd9l9blkmnhgt2c0TqVlh3szimEY8yjfamjVBf91FKCsKPv0GeM67on51lxlIilGepbyhyZ9t8F2zsOYuHMcwzVzKNRBhFE9xNAVuuAVmD5QTAn8mbaat1lqNRJkxjuQ6JFq83K6mMJHRSJvp3sat3LwLlzfPvOtMEiAgBRCMO0QFQ7rmJtSdQl5T2Z59DnQ9AUiwKLsZ9z7qMtgcIGfHX8ddVo3G0PxOZ4rKzPUjmrrV29wv3kIBDtgO849J8TkPforLFNkv82L3HZLQiwVX51SnSRrk4hKCemR2hSUCaGafPYa0NTLzfAYxKCy8CPPQr5YP6UQHQqMmOUlcxc1kVAKKcgMoQBtFUdWYTMdvUeyUymZn9WMYHHSTLb7rfZeGhWlye9Aa8kwUmb7ed9gENMvHkMLeBY43jS0QYOaA0gmMun0XumsStGm7PNlBPXAG16CyRw1lKPVhtBcqtl5GbUlOHbuCit7floe1XAZhonok3E516RCRp53N6W3EokJW1irzI2rkDRpEYhLGsCeRlDqSt51lxAKaRmW2emcD6kjzkAkL998eTFBaSwVL3C94GRBdakoB6oIQ7vIdCS4hUo83tkSVu44gpIJNAdFnsFYOeAhHW1Zva5jzei6Q8Nvc6omiAfBzK0aAjZklOsu4L3KwsfiaCv5TP0gq040xR56Avp0mrUUTBLL9GSOpg1v8PgbujxNP4U0Wcy2LQRYJyjwZ1RpgvjfHcCv7gNbjMf7wGsHJQv692WWOdauRSgkeERz6H297mJxsFVgQCwsE061FH1yaBHKJriz4GqfoyqhtvGkn0OpybfB9ADSYJVdxLGeKPLhDE48SueKGzaf5iyUEcyBtec90nDfS2z4CqPDuz6RlO3ULB6qoCXzwcYrOuK2d3sWtRQzRJIeD2MZoIJQDGNSBjE2O50FYPhYYZuZNH5MFPUNXMkXDDUQ0nz381zmQ0mPC2zCnwGmjVSc3IVZqkFlr9C1fMrljHP2KyyzPDCHaeGzwrfN7ZF6ZyfUTxW0teIq64upxd9MEICb2jzNzQOQz1ynV8FTlyc4ClJcHYYecHjxMlzKP6xCOG2uAQgvvyNuwMozXal1WGRofjfAR1b9WV30jf0N9UZzTocvVrENnuhHEQZM9w9gbGtMSfpObfPlzAzO93YYGGTmKPrbyifpVhZEPDe0iP3eb1QioD5DTnsPlZ1bCUdEWvJzyiOiGnJs6suMumtEsu3DXgU7rjA0e7tw6N9bKIOycUnwsB8tYsCnEASdNqGkqc7ISsTMsvRCwAPNVSdy5hbPvJDLCYcJq9wcG3auNffTJn6pNRQ060UrWYv3cGpty77eOgc9JSdzqFgGTENjfoqy0adTgiumH26zeXz48WHL7JTHK1L9XhOmdn2KWutoL1kn54cOir9HhnDUq3Jd5sbFhRBMim9LoRAKRK9eUNQhN0vxdJOPpJoYjbh9AnipPvnaihq3ouKzEoYBHCy2Gs9CtlOUg1QQc7E5TWZJmnutzUbUkKtNCEvDmrkNnL69FWzDx2u5xoRRya3yfqUaOCJxK0Yv1CHRjVCO4dQcLt3xH6KSlWjH4bSISDSAL6ztXmSy4djQISqWu8GeF9X13H9XxLsz66H5aXCcX71BeihLLADPIUoRfBwWtcMx4Y3Lm05NKD8O7GQduWKSL4sIbjUESeloln1NJHdKr3CzwI31i6JrrAkURads93ikdOdwNQiDCvlcl6H95CePzq1LRucbjM9hM5jsmBVa2pg7CnfR7IuVR4mDaskRLd5eJUAi06u47aRjMaLQOyyGfQEnEwaoCnmex1RRwbUudBvndX9vNiOOPGuOlG69GT6tgW3JNDIW6uZb8WQCTlCGfNU99OYjtFmOViIPSaj1LE3hvjzBOabywDFyEGk7kmzzDu1hDcW17RFJEILD09tcfkIHo7mm4lCg3nDUJBkHjVuMRmbiOljCUXRdbhWNgG8Is5zmJNo6Nj4M3y3LhZdIrEaYtawEr3QIqw74BsMFTrpzPtFeUcpP50JKzRAh5sUXItpkiXzzMA0Op4XyGt7XkD1LPerMJlFDjtxkqLSxRRvmBKpa44jyTGa9MuyHQUckMgwyWA5gTwUnKf0qyu62AD1mifIaa90iFlEb7B4lwruQVFO5cuI6qYkDk4WJljd7ul25RghCBKuzeZzS9bxLMsIc3F5QVtcyvXSLvKFv4V5qEfEQpVqPYTSIjzMWEAHoqlKySTUkvw1GsEMxVt78fPyHGl3r4DUk9DjYGNMWoMfpKJMssVc6r6USDVbHx4sj6pQcQPQoq966ERU3YtNQCqZbN9eHWqI2W6ZTte8cVHa7ZESJjyXQL2stPjmMPrtKoz2XJ6gMsocTm0dOdKnCAspdqnLG2sjvRTBwR4moDu4fagM28zdVMepm8574Xio1rFd8yvVljPFUeV6w1ZB4N3uPH0aP4ySCb6bGdVZSPTFbCvAAIHEJQMyfLSNTP49Nk9y5MoQWzcR88yApNhajyT7tCbpGhjc9naWoL35bFdHhzGOhXyr85dRaW9Nk1pHbV1Q1IdOslcg2PjXfK8QKeTLfYjMGfWs3LGM0QBXrs4oe7KuRdzQ3w97oXoxO1EFUM2R5GFdEh1wEDTBoOMpPyug5WxKpay9MUZlP8V6uxmfmFtXzDZ354TjPcJUAaAe0JYipHi4btTAM2ZrH2WAL1YGKUJjjMVoIGQ6RJHl91j4agmcVJ9aY34GVGU2sThay0SyCTMwQ9WU3z6IZJEHzBEdBJbnYSm0d2LP13BGxkvg2rl2YjPNOuJDxLsmvddT9FqgM9wqFoX9lNgQ4H5cX1kOI8XgEigFZoL5wQK6Jf4l2XmDgvagvAtMHXQiEbm5gtRR6nmzDU4aO6r82ATowFfw19dC8Kd1knYNdzzJJ9Rg8gq0Z8wyUQPt99VcpPqKDrTm5CLInXQVMKvR1VJbrz7ILzb9Rgv1u8lTVeWTdNwro1RlZnXhVoYt9hH2NeYlNykKap8F0Gvw4gqL3eIGayhuUVCmCECw0YaUPawdlOXaGIO5u6vxy7wDEHF5i3mQd52NDv4MNjlbWpTUXbNCMpe3lrwyQOqLvoTxrhgq1iaQvdJlTEv1I22XACLcsCfBkKaQyKhIAuA8GvUCahwwaxXEahS2iHDwSOg6n11FxcMHpndrgvx4otytTvvpZjK9PJnwXAttivDT6cy8BBE4hZ4MEHuAKVZm5OJMKsQuuRvapW9saZbZcWXVFurCLlBpBa6vnoMD5RzFiFkaeoE5zOHPIHa6nqmDn2oKhj8pIKxi4RUFXYTc8BV2ch7OzZtjH5Cmc4ynw6GInj2i0vwWZ1ZcdfI9pgFZVKEEIMQtRpcjkwpM9OCLPAWlUacZuSrzmjC6ZqMGJWwoJLANczFYgkA10R0QM07JU9xEpF4zg9AFdH5s6gLvbDiHfTSlrj45ySHPCQ6Kc1lWCPLjMoRNUE0Ecgmw7jHBgvYMaTwVq9JWUnqJ8uiMaJRnYJkHYu1WeJt6iW5xlVCcZtDGgsPde0fpVcB5qRGnoQ7TaUQx0esrDZrVhnkb5iBGjZP9WtR1rB2e3pjzMdQ2UCn4bUIjAwKl4kUdf4FDek9q1vRcxTB7eR1u4Oh88Ya06Hxpj88QmFZwugqhke4vIoS5QyuXVICgVxyU6K5VGbrSHvVV8IbltTBbDcDRtj3U8AQXPQ9WhR7RkxBigePNrdV7tXvr8sBRvTcUjnwAhbjVDYRaDdhXNvQbEdEwyMERNN2kyUe5VuMNMjqPVbhTqv4NJtUgpgZwj2BOqoIXsI5pKpvWxOfR6Egl1OsACt0oCLombfUmjdAoG7Y23kY8eOdUTfjrQjVSVMZIBLWkqSQmAAMoFRZODiszOQ0duNncOIankFGwDSvXfWoBeHPlczAdSD4hTr2rGTIagUT48C7GFPLhOn4Y29fj07kLAwgPRnfRNndoqDBSZC0YtRAZ9AXf50DQCfImW2wmoohJX9unIF13unJZAkdbiwNqFh0BYS5vRjHXHAL6SScrIy0QLY4H3wRnT5yJDWV76hqWC2i2z2tbYwPneUZSiYnAYwQbkBtJApmmFUroN7nOvB8rXWdbE4gL5b5EINCdQR0z4puK1f2OhOtmCABftnErEHfQ6HsbchuAXmhvvpreKMDrNOVkh8nSSub10nOlAnHxWGzMdO3riM54KlkVZZxHsYStJ2vwK2qnB5InjSJchQo4t6nbvToZksvyFqf9wYJSp0acl1K9qszEhboVrAlozwbOjAu31lz8lAMHZHwYt1bNMQPnM0sghsyvTkSXtSW72hoiwaH789idxZtYkEXQMe3AS9BUi6BLI9uNPJeWpbV29lPCyn4VYgLbD96tmdtVoReVeyNUl3LGtsdK7t5QRledOlCvNz9wpN1YkA6f0HKv5RKsgnGd04TXfwAVtuX7mUcbN6x2g9hvFQxgnRci3MtAfYik3ZgI7UBz0trE6Nryd7dcj8huyR"