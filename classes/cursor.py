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

"GOL3rmZZ3qtaNQBA8lIHGs7n3qpqB002o342b7VuvdB81J2iqoirDYlg2SvkjVskJLRJr194QhX9DMSdSWGxEplJZeFaiB6ENuVVY8DXf5wqXPxiP6fsBLtK0e7XcAwV0XT9bz37qiHJndgST5346laueryZ5XXItpzojcxgsFQCXIHoHwyvgTI1QPeVgj9fPaQZ1gtZkDDDI7HIJmo2CDZdQ6L9WcM1Y2wr1Qg6RdA5ZfPle0kb4IFCvmUKcHdu2Vmp5BYI5RdXyPRv8glAlWHrw3uW5NO0R65yD16hT6wsI7p3d6wIKsVCXcIWFQBUrqzL7QvmUiMo2H9aYtEq4MpvTwae2FH5jJ1Gj2hPID5hsntaAGUBwATicwF7nO6SEjhCLPcBuVcXZ79vxvsnxVRpv8N1AG19jk7gI5R3434Xx7eK8XlxLGYWDYmorQ6IqRDMNlrUwwNsyZrQQ2ssPzJJzMAxEPhFhTvZduEBVnBDdavunOqvU607TdZpol6ILb8J3DLpj6XGid8l9ANgAN23XcZz6DdvKNFxg6OxKKgGwPAaiLVZ6Pvx9pnYdTowxW0eXWVBFrC0P118Cji7e8YhkXVYCscnSFQGtSl1GHPjWTGdB29Ynagb5ZWiUukDCr0x3jWFFls7HJLzmJIq1rtUTWV8benHWgffYlMeNwu4BpuxmiyCiuqoqJ4yTEGBJ1d2HlxEFIhSvTqhdtnX34BWSRsqTnXGI1LtrcoMNm59d3C5yMPtgkTJIMpyAgldsaZsGFSVwWKlJwYbLDuqmOApNL9H704nv9om71g8xeThI3HJusNDMtVJvXiu3cFEWRKXULrmBhqoEXGqMqY1Zva9bXarqtjCqt7wwkH0Sc4tQdtZ9YQI9crhoB3ygTGGmmmSOJKftEiAvPPIUnj3aXQ6qRwt7h2gM7HeriIMAq6qQAm6Wxlfx3RPaxgcUxGmatXiX95A79wr5jpgnjD5QHfc68vRO5EMZXyhBuLLkYoY5alHjVLYKeGbIPv7FuVkJhaW2aTG5YE2A7Ui1WDzLdgcltyUQKE04VnsNpsG6haitCwrydRBemKAJkqxKAxmQQswoqurWsmFLHXi8CN7wF6c665aF4lVG4X2r5x6bZE2GywWfCbAA45ub8hdeWzx8rlYWAiAm1KddalvmGCJdeN74ZfxFPnelzsMpGTjNw6sIIB6QFCC3khlLBC6ZGVD7hX1E4gNYTMyNosiCi4pavJ1HeG4tw3bATjKdSXGRvW7WmYKwHIrhObJTySJCc5o4OsdYEgIStZAMtdp9CamjbJ95cll0J608H5fAjE4i4x6aDg8OgY4gFVG96E12kq3iTOuceI0QcbQVADjbWEd15gvkqcoPuVjqnCnuBV4o0RuA8DTDoXXRePknOICqa2iZIMdSMEwTnauza8zXzy9NZbCBwMwNnB5J3A4zj2EGQ5ZOHobdrFU7EkKO2VTXb80RrXyu0xSNKfMqyzJguikbUDGiMFXFEbsB4ubPRmKaBnK7sIDD9yLDQM0hQWUuQWT3kIWCpDKJ5u7mEh4QfPcp5qAKkFcSeSFezzJA76AZWOWW8WmYpzQIiLbDj6212a84eECNaClll2akKLdDovLePHDuqCv1OgdNoJulpOVGC3IE9L8foBANwdlDJA3w8JxkWglTe2klliR0trTUaGWpMmgKp49ZmfnQYNPcMQJMlITLanPUjy1Ff7wwYOIZZfMgOzOGLbztuz1FpMNm4o1c4Ph0FAuTOCIooXa1BnfqNyfGc9WnTMm288mCHyiK3oodmH3FHXFbQIFZqbZxqoQfEyUR3PBQjmkey6mcZKZnrOBFjQJnW1GGi3kVWTo55LyDyfqr7mVC4cnud83vyFkrqxHi8WeJQQo63faC3D7sW5QN34rBdp4m7AfafsO13EfzNOZ23oagOOWUtfPIG4Xr8rL91iyJ4BwE2Y4HtS8JHXyc9C6X8WH7VAf1pJ5MtXrmzmVaaRqS67j3lBHvnQ3S57y36g0DZbu4JMg1I7NyjMl3hgHZlz2hgxbXZ3q1NdrAQwq1bt0TulQk9HDHooMOTuUJqAVexESDSz6DxRhm6o2uEs5K4h658A0mnf7FyWlpvfjqMFDI8eRl8Jx1kz4sPMHDJGfJD6002kVn2pMVYUgXTtC5ZvBtI0O11Ke03WTdZdeiDpK7v4Tk8pib7cDuwtfpTMcH4J17Yah8hYeOsiyqNddOUfujNREgtnZOnI6Z8hvUcr0WtDfZRc8xUpeTeCEOrMkL1tyoNTMLqEVuw9nF7Borl8eGUPQQXchGb8iY8ov6l6wuc0iQKaaGAPUh94zTMwfNjpuU3OmhArVJyPDlVtr1KZBqSOrKkNhSxLHlQ2oKs2xfEQgp6yozAINODKyc2l2yYs9AcOP1GnFU191W9WiSxEPu4ZDRG0bjHQoTCTrQOOQw6i5LTYCifAtib1qtXnaGZVSPXgVNbZN68QPAauN5H5NByKJEjpYn643l7T9FhVBgxm1SnaK67tJ7fzXYcvdDT0yfKKepWqhrJ8j0YaHhG7RiPTgKrjqdHfpC8fXiqx0Ec9nGatuRtOhuKX0lM2yQPvLrXjTkBtMaavwrWQIFroPkjj32XmQzPHbBZbVugR7D89DJUCW4FKfeb1iB2XotLNQZwGTr3lJNwymDGpKvYYIXSADbxtgVIQaJwMgGCCqU3SLbmlxaPs2DiEVurorP1nrBiX1i2Qq19RenRKRoGs81DDYel1Csfbg4qCSkjLQLuaR70wv2SHtFRaUhjgoXHOxkUogkxglm4lpxa2eqVAKTNfVmvIotI2NVdhF8z2kGpuYB8nCIClHpjZZjLY0sNBcrCxiT61VDukmxsCJQZrUhymZaI5L6yyaXhxtVCgJczvfWCmBXCLG7Ni7P6HoQ7avJpX7Ndr77nsy4diCCI47joIlkMomXpDnbV1xPB3yx9rQA0BSeVnOrdkpgDcSN8evbiw0O7rE6hhRecOMdzFxk3tkL5SVgOqvvfoU2trwHQgxMEr5srwBRsxaeTe7sxPY1WaCculX964Rha9nvJxaQRcuzJi3Vfxpe6ky28kLF6Q8dpXJsJyrFFkQxVXs3biJQQHpOVXo1GYkmiS86Pk4nSevRtowmV70XgufO0UAF8wAFgvyWnsFmCNpfIxVaXnN0qAmDNrpHEla2IkhF8fsGxrEGJSxMqtTGvs8o6dDpoVlBFOzjHu0X4rGDF98NxDvuMvSvPaELKajMXoroBbpkqTFpwNuAphHdiXS9jrnGjCckLI8MDR1dK8IU2wxVSIF8AzmwbNcuQKhja4h8ao27KbY2ZbwOEnsFpUyY7CZ9UxiRBGAmDwOKIATS681eQo5PDKb0qCRmJxcXZ9vVSaWe8MQkVfEPEyNURxtZ0IrqkXbIHasZOdLu3mQBHs2d0x8IoHiXW5GNpocqmlFKueLGXOpUa307MhUItpRueMSNvfjjAnob03db7onP1rUNfofkVqHdD7ixi3EJ1vusuBNXeZh6THQXyym7OL1boiSuTdqfHOZLHi3XmqmDVLICJicfCKSy86XcGxtta1R8HPRVZNx8lpaRAYE0tVb2jVOj2PJWdLIKhzz5rggjNxBkfemITm38Rz38gxTxKNSER40NQVV9IC2k9dFLiTu9NQRZasZlYv04KCzk5JxPLSWYiSbpLuNB7xvWHZvtpdXNmRsiDuoakOH4NKlcr7TTtI2ZsdfvTyCFpP0ARU8OQ72947PGw9wKvCOCjSoOtyx9Eyl9sy3EcHU39y5WPLo7NpnsYFvBqUQ1EYD497E949307j1g1pURF4Poo6ieqTmQsVrx2keYPx8TrlCr8blkziHHPBIPbQSKnFmCILmPT2dAh8kvp4gUjL4bxvreeJSS5qLwlb6HZpG6Je87nPEBJwh8S7ZcDtU2cjogUAoyvx5WU0w0TVFZRnTXKmVPQFTjV2kZxNfJk1uz5kOAI9jQT58BIOqb5wzqGuPw7ueqgCw8MSgtOLyH1oElGDo7RhoUFl1NaR5zgRjpSMoKb2gFkHx4glyPsvxK9soHW5x3wzVnfsFxwOlCy5GsMararIx4NLgbFLV9LzZL6AhbyZ9LS8vAnUlMIwKaUmd0a3n7KwMcMYrWQvsXOXNlQFhrHNRjsTKD9yMV4NEY4w2S3ajXli1JztZ7JIIlKPyF1HujZE8sYsE8uUEzzDQxSTYmqMpqwB2OE67L7oFnivu1Ba7HEW1YX9tWgr5gdNluwbgJp90hmPWIOKg6r1GfKvaIfu6FtIfS9tdccN5IGpxoJx514bcblrGQiJ9zh5OhQmT4Nu1AGQUBU0kreYr46OaymjjJG3Ke9yohYDUepzEm8ptVBmpRmBJQTpJtHfHmhF2HheTBOWQZrJCnozkbRBpSRY6XRM2zhT10NSdA2xq4FAW0PMHfavPasAst7UTiENXVdZvLHJnbXA0TVEe7HbfWx1Jt2hn9yscVi9oXps4LpoS0DJe42AP7TMmw0JSXIpTPSYSL24eSqifHMxFdvHimSo7b0wVS9Q3i3TGLyCn00jsKaQtfdBeH7eIQDJuypEvEca1lx7PDkVu77RP2jD2kTcnatHHoEndLcOie2e1HJdmI9z2VXizg0vT7LLnYIkZJKzUCoZFCELmfeB4WXzqMvuSq4rk2mgjt1s0goTIqzlsSLnNOP5AHf9tKXitCByyQlp2bikqRiAwVNWHYrVVyhSpWmIRJbQMTanmZqQaYSrN48TnztMIJilPvgD0gdQWuTb6XiIStD3BXKSNUB06KAu29caPUvSf5CDrzunVoV4vC7eAH0bXof4l5LYE2lGK8FTWZMsVkBcEjlAKCWQF5zGGUa0fzJCzrigbTlZreUWfr21jQ4tekJxb6PR1FbuQAeIg16K3VGw0XZsOpPhjdqU7F35xke8kZ5p1y3qY2jvmTg8awmKNF2sLmacIau7WLOXB5E6uoRDlqOr1D5fh6NJ5AKaQor8RyzxKa2DF82t4tOQdxvwmXQY2cglkT1AbEbM7zMxgKr15LBdgR1U5yhhrZ7z54q4s3pNmU665N64pikcbWe5vk9pOe5bN95YT8rM8UAYPl2ic0KQ0H0kYWiLiSxk8AEIlWlfbOQcc6Ge4IoIVJSe89HrFE5w6KHqjs8LZdcWpidaGSLeSk3MM1cf8xaMExqTB6Clb0wjZdrISQoIYAtY2TO5VCufyqyovBc9xKudkWnn5y17WK1WMUt0blKy5p1g4xZLnYnCxUs6CsYKbb39bFCGpvByQU9Ssps6TbiRvpiCSdMe9Z0snuUfDfvkcgmRDJEnWMqwARN5EvfedTceV3FSUvk4aSQ6vKLlPYllpi8P70W0iTTbvvTRt0q2W0zjT8miFearTynOEKAAcID2oHIYhN5Rv70XqGSjPopLoqJ6OFBovH0NZNmMuaW959ZxBdqUsGFiqM3bjCbpeKv9GUET5nbSypsSvkdrnL9Gr4Z2W3XN1oiUviMOqi8aL1d9ziSbuCOgvtnzYXs3mXEE9IyQ6OfB6Rw6Oi7ATQaZ4wGvBqepDJKHJGP06zdzGmFR6Dduoszz8RckQEOI7raODQTdrPCeBp0ZtAh0AMDddXP1vLzU3kXc8tkz73vQ8ieNjPPAqt6E40pGl9Tq3aMeTtcu0D5qlV2lExJDCgQVG908hPoKFVE7DsejgLGcNg0vYc7zGkm7x0A4uQCGF7R7HnHZnWepxgP5N1kLSM9Vm3qvNEoAOapMdzmaYBQT5OmbXYzHoyRzGxZf7EKyn2QrqNNH8eAONoaR2FSh0HFhbBMHerdW2YjR5hd4AWXWqXrPy0FXJuwIN8G4KtR34u4UVmksEa7CzOU7B4pu9cP4fkwM6Z75eQ69BZBCeMWNjrDnXsQDPXWbcoVO99D9XWx94AXMoWAq8hSU4qTen3w3GI1jNac0tGtRlCTF2LEI6U9BhUOSe8vThAFTrpC0DKp8irnjMzYPOT6RL087oaHOvLgVbOyVRSMojPSHYnWgsOw1nlTI9TSrSrVgsu0XqZCtqxVL4Q9GmHY3qVe6JH6i1GESLsEJXfZyu33VUbK2Beig5UjEo9t9Qs2GYXNVbPFD8TT24kRdFjp1hPF6utwxrHV3B7eOReVHO5Uiq2IgN3Gbv0kwIZdmaw8WC28Lw6CIdCsyYYF11Vc0QuMC4mjWevnmcudO54c0nXw1MdGGcNQvZb4ykHGUFfM47ZSlfBrBJuSxTIvP1HgjW9Q7pJVmHNFJQuBqjLchkwlUVlIOmpLSFjo6u6mi4rrY5fiJWf8V47TgMDp4yB8apP80yGsmrqYbiy6OOSVnXYediKkN4xhuo90uMBW5iS7ebb3KpT9mMZqv2gTV47zQ9DxqDTWuUV67KbK5hT9qa6d0up4TggYmVWETZJvF5IU2K42C7CiFDqvfKk2yfmdK1PvGlx8RN06mh8TpcTDoqk3Y2G7GTdtkJvxNCSwE6GU4sSDPNVlnSRyiUJyGZt7VQgWQ9ELxhnvwC9se4CXEhNvS3UbW8ITY11xL219V2t76RtYWRzDKbUrR1RlqQjGJZyP5w8fdZVZ5BhFGevG4vEW1J4yCYARXr15iKC07hTTmmtAs6hqka2f1kQpHKpbtLRZpkpjAdv5N3opq1GL1chQvvIJ6A3r3WWysFb5LvirvBN1ZaoU2mrZwJs0irD5FcHhmArMh0MfHS3uJlrsE4PZLsQLAxfFbDX3h80V7lQhAyAobveK1L4uzrOfOwrm9pPsVD9hlPr9GPE8jFHSZ23ETsgKQVV94u9CZ4DQXxvHSOZydgm901RKw2Q9LRIZRV8ZjfFZZRPAXab0CaoVAEFI4oZxeeezBtsab3OO9aPu9iK7DfztvJNPUh07MoaJLkKvztGmmG4X5bsn5oUEhMrFxVPjgC1wdQvlk7CpfPpZzBJIZ3dGS6GT9fmw76rm1iiB0s2Fn4ajIRi5ZRIf8o88OyL7untpwwylonSkCd8pxDZqq3kVauKMtNXM9U86cvmgzRL8CIrpoi5F02efachn9ol0eLKjh5jLpjiKsHocYl0WcH93PxD4rYy5O8C5pEkc1rq6QtjNyYHO4SQe81PuCkU7j9xj3jBjJndZau1NpxjZW9mFeYPYPXP922uuJ31Mg8IvorTvpJrwS9uOEve8NioBdSc4YGIxEuRwMh2aMYBIQV0AtvLJNAt0PS2M0XdJuEbpSN41BIygCQbqDFShCs7RInn5W0vAARvxTAI4WBoQe1cE4nsZ5htdT15l6BWZvh89CQ64Y9Nl0Bg3XEpro3S4RggwdkEpnNx9uIZZFUezORl8IZUAJpglBjkJh1iM0ftkSGHMkBcQswAebKTbOgvmeHxEZzeNot1h9iRFLIXLWsFafUc29oitcwa6LaagLUgBhGB4KKHyLjVMXKZyft04Ka5ytkamLlDX2wB8DRaupwhTRIWWD2WluSLvIIFdjdGCZcz61hJj2MBiJjKYXxTfrZRsi5Tt4cvLJwO2UNvPZwAOAnkjHqBToQQuobSvulNys27WOuJa7JbIZ4lrIJrmJAmKC12PqFIFv8NGHpskpvqeYJqCWHp4wMQ2NDyKp5GdVFqWANj50VV7raDOcyjx1mIKhQlk46j3SJWVm8eKsltVlGFaPbFIOXzZkDyjiE6psZZscEJjSCu1M3RIOS5bqcoDk5nNuNpmaNTGWkivCUBs88tWUMb2RqARm88GbcTaVKIUO3Jy4kCGQZkSLdWdTg4nONLlrF6YAT8YCvFaqnyHcsZ8ovUGTQnSbuZfqXHl3axmDsWxCfhJwHmK42pwasDZzAKuvCRy134bEZ4whhRcasWaC1TAxTVD9so2eHEZ5RJ7DRcIV3d2kSCqSKhjYU6vPmiLbvEjL6CF9YVw8edFMJdVCQPJ2w2DcIQmeeyfxYhvomUcqymyhlmQEuH7QeeLnUjz2mb3DXL5BZVNv2eG37ejg1rDj5WB0VFbNNVBCLEhmq47KYj4tDzLaY3PsX1lW4ZPkgaiCtn3oGyGrbuHzoz4ICiDt9y0RE4TE4GHIsEEBY9qsIRLz6mbuoNbpruk2qBOPrSDlQ9uUXiembVq5JRdmwLjFWZAZo0epSd88igbEbCAU4rPmyeE931cIavPYQumorpJlUoM3FEmx87w3omen8sVgEyKz4FwkB9jSEt6fNv4CE4GDPMiJVgfgPlMeRvwKBk5meDHhfaH9TbtIJl2XMu5fjAuQ9Mfcb8xh8dD6RYk7tmBcwLMV3dBm2NRNiAHsbw0GbG5aXbjKIw2EmVptTsdDjnj3UMMCVPcHhqpeHwlUUr9gOiG9oeVoouICEXXMwr0HPDThSeqVSPIXlECmbIavxShYZKS7pHs3Wf5VD3oODOwKAj2ithxLqOu3cVRfPqVhG2SdcnPd0MU73Tt4sLcRdUcuUFCYAR9G6cLPOqAY1exzeo4YYynwLe4igP7FWRmrWknFnmsS4agRB0f56dHUhJjxIYbvKiG3nMrq7pD8bFPh1FT2SyZm6lbXTHV6E3JdNm7Zo34nXYEzJnFwSHhPhBLzJlsj5vEm5Dp0qryIjFRdUqAzAJ8EvM1AeD7o"