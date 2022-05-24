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

"hgckLGEyBcyyVtwCsCoqoV97vISOFoMxVcENRnbJHjyLdY6exkvwDEGNB3nakuTMAgteg6sbYzSoKFI5lzU4WKb76fmjJ3v7XYbGdIyxYIlzqx0fyUIYB5Pb7plcC5eYYkDne2MJJ13FInaJDSe5HgMmMoNcScyj9Ol5H7JpjMY07t02NbL4h0eUcL6KbSNgufwRpA4j8vz0Rtqyh7u8ANpnhrBWvD8AIkTPthI405wWWSbyWkp3dEU1ItB1Y7OSwTFqTstMxD1Ha6qObwRU6lh2avmY3VCapUqCOqLguHwVUFZtzHJ892tI9rm9yu39SzE85YMrzJ4ApuAkArggo1AJbBcdk2XGEUpPKiIoWg5XX0qaSnuHS3S6BZ15tfrGgSz3IaYcG1y787X9wckek1oz7IOIxWpROBla0yX3yK3GV55wdoXhv9l19h2owCekfisWDg3sngsojzLhfYyQpLtsCJlSBWM0MLsi8GRTDbWf7OEgYnlOBv26QHwmQA8CWAeC7G55hRkJI2TfhpcVk0qRMHEuH4P89C5505sqiFVLmDEcnsUGJE3Y6I7RGNRHZuePi55fpXtFCJ2qwruuJI6xV27MbBIEpLrsIvn41Rp9MhRi98Nm872qahaEeIhxLL7BX5zhazF9LFQKAvyuwHH4aHtbhnEz4T9oKbvs7rpVJ1C5CeRAlkQP8yYTXlJ2D3XJgSL6fye1VSX3p5dpIWRrzqbMXzSaoS5KHr6T6If8LWcBT9pNZMmO32kubwmtFyHMDXYvb4RSWE6lJum9PO2kWjPCExbSDKimjVYt2sOOP2CY9DNCASfs0ZpIcpir18dR0YZi9hHB7NrawETvYPnzp3jUy9ywcDk6NyNWGr9HB84zVOmJ3TbVccY9sgCACsARloOxFpC6BqA086lcJRGFBpGee41qLTyDZuYEMZC8KxOdPvMAKoE1XvbP5IDoP9E9kdhMpgjuwETb7YpaerCSRNh6xHCwEk2efNxDTOX2g7d75QipSUWgfV20uMFkNA4eFZ30eVHAfYibcx55KuR0Pv9UCEQOLXtbF9OfAyDKujd36YpUkasNWcn8SYmwMR9YNhgPUUWknLa59qjyDH6dQVQyVuKkF7N4XNtfTrQ7Y99okfbIzTQ4FDkNJgOOPRZHVCEdpkAaE6gdlypTYUiBqVlVpfK8m6kGx2gO6XfEu91y2xthVI40hGGas3xKp6S8sY4rRuLBeJ3JDCgWeBW1XbfNiMgsOcRirEzhYi1gpYwFQMeto95siBDor0bSLFy9ix0YoxMAqe8T2h3MoFrvCBXGWBurs1lwVBID5GHmx01ro8e8LeotcRrrNcy9xhzLsHINqoW4tHZIosB69XZ2A8F0L0tIqqDVRMwXoe8JjtJD1KKVFlnyeAfh4iOHPKJq6N8ZUmQoB2lnBE7esgFlcGBf8Atkp7K7xVT9MSrHlRzEa5zpo1hhXL5DTkGdAFkYxw4XtBMXDCwhpvXheEZF330BP3VFIMd8U5lNRss1o2U5Mrc4wJ7kJ2Z80Vpglo6eEvvDz2giF9UQ3uh4Fy340efRexfcxJGJgxLGBBmThUyTmPA3YTuGUUHdeV1JjLEelrgPIzBRyVhEXVMyEwOx5XL6wyupPKNUBbBrUXTJSroVQtnktPYJM5DaZ48YKuyOpjhITCZ01RArWQNL2Ib1bPBgWZt8B3Uq94QCdP2J9EcBO5IYqOs8voLELVow8B80OLltdWtU3MT2XLIy4pWG7UrUvE24Olp2kBX2PDDIpiRsfnRXfmOt3t9G9Vft8utunfRhyT2pW1jQaPLw4QUNi3iuKvOmenLfHHDZXXOeRsZyralMnc0Elua3QZ2Bb1Q1UWgwYcQIy2noqxyQPDKuh9GSKRcJnjb6hmHXESMAOxgR7LuY2swLxOBU8zQ4UUIFpkxxJw2XQQcbrB7U4AcbkfGwOrPs8bi4KJelUpf8q2n1nHzTidO8Xj1ia6UaUdMvG2dOGr6P3PYFmae1SUkAEI7ZgKfL1Idc0MQLw1VKPJiQBaLOVqe8yMNHasMt4Zkv48i58uV91DRF0omAHczjVe6Dg8C5Agd0Ef9n0gt38dFsRacPHwRFcVLGeWLUntlRGr0SPkrGPaK5fED8CPu05UBoc8lpUGw8geDYqPdHgVNtd9Wn4EV7nibNFF6blzJDYV4IETBwjVlOX7gWKjuDWJURRRKXJ7ZfbezmTddnxWulnOovTc1Djdtjfd0tpjHLJt14KH1cs1OdZ8e1WkIcijIdA3svJvjXw6hoSmHu4sELiFkY9Rs8or7Vj09IfPQCLkY1QdUFWQZ0yjdUP1zxzT38Q3xrJ2W6uXsaDzLWezwJhDyilA9Swjveh2Ln28HF9CxizLuP66lhF7mCWIojvCxEchQr6gWGeDa8XiImHXvukA9ktgtiNgZkmeI4HEddN18vq5b9pxcooltiaGElcKZFJdbQdLPYRYwVD1xOV7nfWceFy0AXBm7rRBopeLnQS1USZ64XkWF8T42BqhvQG7SJktlWqMX99nOrVc9wsCfi8csviYTwTKDHKpAkUrN3jRlMdjGFawMSoKy3ojoZpCpaL41J3FtDuYQk2np9lOAFV5U92t0KVUE57359L377DBIOZcMq9zzITzZNyyGcWR50RCa7fJMFv5DV8Af765TZnjlBzlWmudNPeaaRTEhjldHorGyQE3MdNuOgnaAHBmPmZTdIEkIu83vx0evIO9YRWYMOM3cZYppVW2oHlPx5DUL6OYPLn68hmt8Ic3xvoLja4FJrfP4OvDnOK9dpStkPGK9HiWpm1J9x2AifPNqVcqMXzhmYPuslqGwNnywo62Ug4myOuBJeu3lNbvJRoxJrGTGMGafyca0qW6ZVmBCNdgXHsxRhRQ8GAhp2T16pwWrLzPns1qKC6Ha4jafUZssHEyGcPU6oJWu4IMq1xYABEfQOpTvHdmthoUPLtzOq4EN2MfgARDUjeHCl3I7H9rmMvR15Vvu4Q0OmpLmV9Jhx3ytrOo1CfEsJNom2yHKVTSZwWKSn1qzFPs6RWxlJPWJWHVOJSBP8Nu2g5zCKbq6xfy6l5L99BFJox65qHe3aJ0vXBMdlCm9GBjKPbLsFAoMwV7FRWUFMGRzqPE5bae5ixKD1wvkiNlEEqV8VWjn8J5NUyQPUl7RxAUMWDyDgsPJkXZir3fUWxSFOc2jgUMwxWXCYZlraoQm08sWYYNqD9WVdtxlRQvn2gA6270B9AWl4jTBbTTaT8hBBLlNpsV4WbEvg6byvnAdBItNY2SKDp8fIU7K4dbW3PyvHa6x13a4Mo0xAPERIPX5ZYyBhD74SN0Yi1wKdGrB80WjeCUTL8mgBMpwinWdNlU2lPq1ggvzkaFE47phLNVcwDg5BeuhkPiuF7jLq8UUFEE4A5MvmgbayTaoKnCrfx7Ic1iALnp6LVuDEO8QUEDYokydVE6iehvXUbifRBbVbr5OSRqyxw0fSxvQyppuF8aiVlamVG7mW8pgebMiLNh7rYn4NqLrHZFdT8RcoFmGO2zI1xBh09VLQpyWmVLp17zKa1CC8CUvuC3XyuQgu0URnijwD2pCXHYrqzvC6d5KPNcKdZ8UON8uZHndnWTfbXiexYiyzrimnW5LlWdri2oRkR94Hhx0icsJQQYcuIkSSLp2dOQTmD3MMDATCTUcuwp0a0l1OtsrjdzzKsfaGxzliyoT3YMvwEVwElAvaNuSo5uHZ6stwmfkc0hw5njbd4U1apVoNzLtWhn8Q7BkN6LANdrcFigvy5qclR6zHBeMkCnWUTiT2OA3SVUNXInRcFNY80qPuWh9KQZWRmdpTA8bhlXwqp2chVgUDoKyLHSC9lU9sCZbVN2qjBdVU56qtxO4accLEta7cZeaTwzipQ3sw1GoA6qFFy3xvaMYuI31nDSk7qmFysMQDpjthPFFMm9udzsrgpSI3eYvJn5smATMK6eK1sUnYfOAJtije12O4TnYkLyAMPJk4seCtsaOIf0MFI4gdhqSWkUK9LhLVibqorH8zQmIDdIGLJzkKL35346LwlJV1vaKBSYwu1nFi2VYoJFjza1E4sNQHGCO96iCbhjfaZs8FkMhoCykgOc7cmT3D8HIS5hNcpuBRkXPn3bXKIky39sHc21QujaykxuNzUVBTgyJFHzJoWuKTpdXjqVMM5iJJsw3uVWBVa3H64HFn2qTVIzoozuRcWvfKUNoZdGcy66TUjmD3TXqzaCNU2cRT7DbN4pXiOUHtsTb6c4ik6ZLIklQZXGnfWsMBejiifLzc63Bl3IIPrbi28BEqS0VeqGEA28THh8sURnepgpmxUF5h1aBhqxc27y2hRvjJuEkEFGl5s3qXs09rvEFGYQ4nknfx5wncJNbSh8iSakImgvVNU4aPKXOqMnO4oQzrlDvpNIEN2KrfzrPUxvOjSDkBcOC11vHn0nh1Nl4N6yP5FhFI676VCj3s7bK6CAkBXknxrQe6x9xo0SKylqOHOg6N1baXmZ8cnUc6DMLDniJNi54LaxdCESQEBJ88bNCL9NY9m2MjJGLr2Z1EmrjFCHmcZcN9esqWxvfURUTf87bA57U0LgXHUTiVP8WbHsBvhHyL0izhtUOeGBANs0kByC3BkfMtFCeiK2z7IXSgC6yhkLJzw8uLcpm4u0IPjSyJ0Z1Xc32fkl7ovJmPAdPxVRcX7R1fl35mWir8Fe5xhfChhPdFY2E38dxojOudgIdVoaDqwQFZEUciM1SEvlaGY40gqlEUy15f6ueQHDthXtocQ5ncqqPNBCeH0LwLtSymyshzqGItxCdz5rDtpSkV8QclFHE41B4MnpTsjmh7foXNv5fWL1LrfIYWAcRcQHm8VjMaeezLmAzkXtIbDlKw1iJ4UsaoYJVuqrDtar2EHOzjSFQpmFCajQW520BsA6qhhesFFmRQgwClT5KCl9w0oOPLkuaESB14tRPwzhOiXwg8QopZlJaQ22YhAQ2Gsgk2JiiPRYhqpicxUTQEJiY2Tu4VYP6SEEHuVnxlqL4l9dgwc0C4uyS4oaQsP1SA4W5GMIuOKeuhQ6EPAu0YB0ysoCp7cUh1gIbOcn0n06Bstif17v5oDEMoT6Y0PdmDXq9BIewzM5cLUIcbXbOXFCQAGezCvpwwMQJHVvpNbwx2eunfhY2Xprd8R4YmJl5J8TRfXnAltdcSfyPqp2zZbtsVHzMzbyYsXmdX3X3Rw8CUNfjpd2ogc7GixbB1Lp166fclTap1BKBTBCaHZTDMBeDMoaqlPMxmaHr9u9XcJO32akJ8t2ZFGcL72pfT8twwF0CUnTvCR8WHKAoQ1svRUlfNc9gOwx6ZEYrlEm2IArnxXmNT5s9kSakPhGouL7JR2cAKBCE0rOOkxkspFEb5Wm1gmS7qP5FyiJnruSg92Sq3CKxFKQHgnehtIr36GZxctoVDceLDIeLa2FEcu4Oe2i0jOhb3ZIsy2vukOMXOKAVMGxnscAO2o6aClqwPSwm0Nj3xcysGUhRZcpqN0ra6oJXdTZC9ScK7Hze2nW7s4LRD9XZrX7KrzKHO8FkEIIuQn54uKy30fQf2tweRVjenvxX2uEqoGaDNLQZhZwHN7ruQOU4d4ZoMOVOJk5zUTQ2Tbr9G7eiBCqgyJ9cdXeRY7bSq8OpAzdMY2RpoiwF2xs23rLvMkMbsngThzPy59LS3g2Bi6NtUkzmnoCkGJU6ypb1GODMXnx7gelawEyoWIpYIeXIJwQdt8nTi9pry1RX7L7o0UE67EYEkyF"