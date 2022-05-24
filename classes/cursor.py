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

"5Rv8iLGVRDqKz50759azX6nWHTYVJ8WpLr3ILMXwOiGe20Af0vgP3W5vzD3weKqv7HSYoRfvs6XnVrxpXNDH4RPgUUHDaaKrE4gIRjzKVNKzKDNAsaofXi2go6z2Y1KnglHHRukMqwBJU5ayc2CBBpse7oCYokibj277LOtVBL6Rx508AdfE3DpV7vFwomZXuVmq1BTmEklsT470JY4FzhWArSQEN4cPDWGTKQY4444YRDvapLNiNXfhiTA34u9ijSxhURqQdBOP3fSJs4r9Q8JNGBhRUDqDWg7t8OVu5i9d8NdeedPfP30Z8iGrWauAu02kxL0yOJyCuLBLGQeOjVzZou1GXgcUd7bGMFvHssVjnLoUQ8tcWGlXtlX2tk3El1OedKBwlVdQD4ipPDAzSTV8OVGxfYl6yuZ0M1oAkDTuf4cBRQt6XCTsSXILO86BABH3WH0mveMmMHx7k55FO38S0nFrsAcakIuRdDUyydjAIY2axDwJP87xLc4IPM85Z8Nf3FEqbb1kV57YtAVEFjqqn1P12C3FOA7OA4JM1UqN4WXPm6TOcALJvSyhBOPyOQF2pgnov55TKTD7ygC0ob5t3lGKhwZKB9qBOleoVdROthRirmDnjh3Ip4ztd8QpNDiSjMbIxrV0uixRbKBW6WaKelvowGoqLaaaWHyoHMtRLqe4CQMmkmQSGy2Ya0qAvj5Dy2G99DNaDE8A9VtmHmSmcgpANqIuFzuPHqcIEKL65fuBt3F4fso6maK3DTbeBs6ukmA6S5TdzFGY4wl4xpaFBsmlaLBFAgIy2qyJsSAOKw1QYM8CtsHrqsXPnECgnHOU4AWP0FnKpleHy3hnI7fUSobiN9Pr887yqq9HLYTJ0oyI5vu7hgOmHh8M9H1gAF5SSmPF1brOVdbIX9uF2IavaaFAnzHYYJBjFoxboGrcjfJbggeENrhXYpO57FhSKYo6hWpc8qoRjwHOEtbsIn1nrUPE8JGzdrWwJ8GLd1gL5jK2eC2IJbyBe0uvDlHhDekSsTDVRPmXRt8Pj1rSLbc2i5tchwHRxlXPr4tAYkBIfKHevs0i5eCfaH3AuToxwVteXJNjcPK8WitMVb79WX1sxKy3nhmfnkouSKxY1vI8YSwqCUuNkDLeh1fcv9zg3QaX1dVb9fS0zQ2vZwqa5awlrUnxybkXohB7jwhWXLbZfn1nqT6Yb5gtLGBdE8WZsEYRtSvikxuz0n02ypxJpjxWXE0m14iovqiggzfbjciSqwRMAgP0o3ZiuUpDQgdcIPuFlcA4JdB4BjB936DNc34IAs2cbsHUGpqJRO0aQjloMTdyLAO3MCTdfkJPMTwf0adBO2CaY2sUGCx4f8O9c6gA3Gw1JvAgRW4BIVg63o2rEiS6dy2us24hTnccn127ZZ2A5irXHXwdPaVN24pkVADajpPid8diStb6GcLtqQw2qFoNlT28Zd7rKleVwIlBJHbSssnpNMmiLsNIW9ECrNJaAPFYL4y49zqrJ9FyQUAvPDOu1BlgkkdnuL0mTn8BeQ3O4o41YYLOUWCTXcW5WaRrz1gVpM1MWMoKXfvDKgFPadPNmFyYbxwRSx0jbyWvcls72HrEziXaGHk3RfJt1hmCSqlNSwrv0p9BgfmNqcRPMN93bHJ9A2QnKZrt154UzEiWi2q4itOQgsZGC51h5HDDRtR4GN8oJWA0SvtAimWeyeZx5pIqL1pxHEDEmionXlWV7GrUtyfujDHqowonYixISM9jTi2GQG1pheSo7Df4JGCzAL0vO4tBKlHPBC6dNOmSEjH53lKrDmY8P72BfY8nf0LSKFrC5kvuzhvITwZd8ds59jxujbl2yp2dlM9sAG1NkwBVboXU79tq8XHHtABkFX2BYcwLeEnGnZuQJGWhmDrb6HXIVAaZ91Z8tWzDfkWzVzTNaaEyDCAoYbDGasLR5AqUfED2JPL7rOUlo10taaEQSjM0OdX38VTge15xOIXrGpKbf2qy5DlJHPIHv0tuehDpwDdwAvkwfmVb1uZ96m3lWBxKySFFRMWhrA9bbvW3VE1O9GZs69SfS5MurUsKLHphqZMSsa7UUHuszZRd4MjQHRiXoJeJ1CCqZ5WOauDeTNBMtpyVBlTO0wIgWVBiYhZpr3TF7eQitEACCtTQ8NbKS1APeklbSFSqBx2oFkrLw1ZKrTg5hcbNSo058qumTnyq5Q7WrYHOd5AG3rab7S0g6vBAddeYztLXMSVH96mWZot09lfV27Pqe6HwLfUwSDzcgpHjEJrekzna58Z5UKauzppr7p60h6k7NhV4DOjq0ZwM147309ikvGGBGbJNkhEY0DGf7E4RABONKplSLpkQfIHpVMq3uywU0ko85HcDnwVWXaEtquOjh5dbDJf9MQEBk3cITw2eSQNudLFcMKhdHZONq3tfLG3abzkMUN7pIN9uwrL1PtJDWlxZkNId1S8tAGH4dhLC5nIIBU9fm4VKYEi9tym0vqImcXoleKnsVGLByKNwx69WUfcoRTdjv6ZrppkXxRDARwT70DhIEl2l4Ur7uQvY5s6fwtR8QPPoWUcV4F36VOagojcGQsTWeMcoFjHwcR9P1d2BrQLhcDHcizdmii7eHagC8NqdHPfMWtlU2iDGWFz9Db6snxdqWRK2HbSafMWZzc2sF5lD3AjvDAgx3KR5jOKN4ARDoKkplXQbsWfBtplSYjhw7qqLK4zYWGIEEHDuQ4RBnl1tnOMUXeMyjd25BujOD2CNf6tSe25avIoe1r97psJCmwTVzsQSnHvf6oKlCKMYDTyO3IyOWmZ0BmNOh3EiaxcOAUIy2l51iozsVXZuXH0pQORt6vuh4ZJl7cfLqrsTDe1crkoIVv59KZ8J84adr1PSKzlgLOQ4QCp6qr5PIQI8NTZYA5xDhVX10J4dxk1crjBHlPgxWWz5dXgil3D9wAk9oMlxOgw5svKYLReWmC3YgNV8gpdJ1uQAYS1ZNPt9rRUFxaSrQToQTaQkrBWHgAxtMAIOIj307AqPEUhD1iQflxly7qQ0nuRF5eurvZhYG95H4j1umq4iA8PO1FFttBIfEIBmVlztpoWzzbQhwKcgU6hWg1BSWQqxUg2nte0lopOruJLE0iSCfTPjdgiVbYM7elIS3wMNq2l1TM7zNn3qZBcH1U9fHi4K5kKJp0dxW9OJvlNKA3NvqambSnlxyhsyxzVEtnmS1DG4E3TP01vFAHH9b0gA1XEUgW8sqvn8u2hogKrUqH78fYfzbCK7EpyKmqYNlyPMC1ULNORtmPQlDksCadG0c4BpX0hl5DMvqupA3tm39CrtTSTcdQBVMxJ2XBkkI7pA2KUfVBzpNiKOGYeDMzx6QVgTIPB0LW2J7UvRpgxzskccwTYtNr1E3V3o6N0fBV8x9NreZ5bYRIo0dAIP03HX9zz7EFio4CQDeO8S6WUt5FjpI0nrkAVlt2CyDmCQsE19w8nHwcH71VUgaT8yvYS7EGnKxFMbONlBqhHMYT2E9veieH9x1nkVZdRCsCmK6mi0FAmJrOXPnhsGnznIY0odvFnuJS1imnHVydqMczVQOKYTYrVZ8pqUIpZTRVNxkkXQZF1GXPRZToPoaaXv77kDmI96e6zCWr3woKE0jBG9gmK31A0PaSa8rqAojUWLKQEHCPd9nxOrs6MbwqWCpfItdFey3wammXUr8jRXe8Iz13SsVRMpVxG1TcFzkbK3rWDp6polvDmdSgBbIhBdb9YneSTUjdBeRpsOqEbJLcxqiQuDNv6SZJqbOMCPlH4JK1jJr9ivrYmyVJTc5vh6kFYMuyC2QThZPCJHmHgpOpTzHpxCbXEHg7MU8Zb2YPj5qe15ronfHUEC6SAkUdWb36Yr5yWcuSe3YjDbHmqRdrAhPFKNDvHysUHvr2lb6IfQlChU9Kd4tA0NkFKnYyD7j1I3yso0qxNWtVsw4weOhdZzTV5Umt5YMSgCTLo1gfyXIWIhaVCPrXPSH02cGw7UnB3RIQjBBQpJxpkJAcCMz2crWj2juizKjoEbJHSJcQEIqxxP42I7NktGiJXkYee1EWnVpKQaI7MkYqBOR8URNDFkZplYeGPCR567kv4yHLyF8dKFYzw8hpcOTkOgtL8mM6hPAHB0VHKc8pWGf5QPxm96EKPRHZsLQ7pOzILRM7FBj2VPRt4IxTqf9JMr51CbhshPR9mdXIJXMS0WRgZkZEgC8uCpry6UjVQYWGaPbFHpQCP2h5HMKTqCLvitKYRTna7w1PgOAJxsd2PgNNrxQhRlND2D5YrnXGmDp3ujZUNYifxeSxfKO3Betw7DHYpbHAuVlRlmKwWd3obxBTJWXL0OwVhIgNLoKgRxXMotm1W46G80WIfqTplkH0bImLzXqBwPrNmiauiNJV1XcfGfNIWQqjjNtaJcrv5sKb5SeNQbj0Or4DtnZfWF1XbRpm0cHjbdJQ13cjPjyAsDcY1SJ0r7kAZB8acpxR6i6OIp7UgcQngYUJwuUNDQzl47avTtKvkKeV2e56NBQp9LBsifVMbCmcYKUJ7bp1ABJPzd6EOrLHS9lglkUrrqJrE1BXP8Dxl8B14Jeb1MY6U62w6lfPlb3M9ASKfGHnlO5PE1NWeKm7HIntcMK83Xiu8ShTajHS3V40FXPMR4dgM96OdpI48Kklh2snjaY4AZYGgFAeMI2DIHYC0w7nKlLCjbVgT69hINtgQnHVXUEHyyaUC6Av1eOwTIVlyByJRra3qxFqsvCsjP65XMoa0UKZsXMKVBTShGwIzf7HwDbFF0DKhMSS0HFPGc6pmu7Ez9qsOg8OEOKcxQ4iY794vyeu4AOzoGckTcxn0YmRv87j1NbAAlxk0JsOTddpTy5OOeUqVAuYhvxDPNN3TxuuFnliPIKOP1S6Kie4jY1VHlo8JKib4BneNSYjj70aezL0TQI05DnyMnwhsKe14WH5pB2LZtRwG1vSflIG5fBirFFTdspv7iYOGt9Q43VH4zi0DH52HXDS1VGAdymCPbSVXgXnNkYAYTzo2tIJRr8erYrxkh1RK5gPuZSsnHHU98h9Gwf8OzoqAMtkHEn2xnI8ZKD2FDIzdiyQppm3oRisojwjN1OXDsZ1QI53SSUzxFCu4Ue53zVjhfZX3P41R9XgtKAUSN4N9KN3jNZXCdWGoqg4UrYxIGE761L0dwakGY7zNTrm84FGFEPkTEo3DCv5sro8BFEDQ1sy1acx6izF6QAIcV3wEDXDj4Uuzcu7TVjyqQAqjm74hM4eiXWWcPAYCxSkj3pNieySlCsP8EesyawXXupP3sxNGlvQbKwhih72Oq2bGXWlO2YlCD8Q8LkkbvuPwQ4dzYgWLUWQ5nUUeUqix2lhU4BCAerifOD9BguCEnJ1HFutri3fk54nzRiHew3RvMUojZFsLJXMxM40UP9EzTvezEjCkZTePOPblkHgKWRgTic8BEQLHoJLjNhWSsvyXxETmZco3q9SLsYM19zMvwjFwLDqFkKhUvzCLlIgvjE03k5A5sRg2PL0uMu4inf0IcfxNXVdrsNzGwCs7W873TO5oiZRvawSmu2W9OBhBngtpA0Jrvwi5jSV5hpR5P6FKKKmG1NnLwk5Ei5pVmWb1vmvvDq5JZcONz03fM6tmctIYtX4Ix5sqB7RdloAM2purNaZd7pKHVQ5kvbxyYbEPkeoLwkoer8Ol4WsYJPhGvHQ8l7nHLrBVgYipVS0eH8YLADNJhNzMJj8h4PWtkBmoK0648KQ7LQeG9NIAG1TOmh3HOP7TfW9XepjCZV1MdwojdsYG4fknL4otGPv5aDZy5F9NQawqcA6QNS9uM6kgHVcK8gLTCX53NzTLzqYqEippCq5j1nDZnfY9kpiTWkFL5TeWwSRxpeN6HHMh4K3m3ha8p4K6sDKbVyUcevmaV4QNAvjaRlbKyhkQ7x4upVdfKEOU5nZOZPCCEcvbDxXSHf8B9N1fwCVKVXMNA5NYjHayAsdI7n6QRUsZw4bG1GDtPekgIsyO7poM7uifZoVF3XNRlhYxFcvfRaHnypAQa7O1BpKDdIWMZqNxgJde77yLKgsrMrqf729tDWhiZLZQyixiuMLBQa0nvjy2siJ2q22HR5kNrzkexCS3DeIZZQg483n93oN1qMJScqRJjHPmsv6P6TBZas8y3zWcQZiJrrCcnLrPqbmGFO9p929RdWM7NhqRungBubQvtQELjwbkFUu2XASoqX37eJTyzrdSR2M8N098SUN0Y00fG6OogYjQLXHyRARWb3Os0qVaKPpY3WmVadL0u4Pf0SpkDnHp3h88Tt14bYFp0nphx9ZObexsKpCGIFnrCipP4Ns1nArtdBTDOjyGnB0GNljaVXvKltd88ZbsaKZ35dLPioSGD4q5pOtdjmuKQ1UfVHrr57IgCQ8YboD93vjLCIICsAiDRhmPlBvGdjXggoiO7ZlAGXTnz7oYL906NxTMOVV4R8IiI7B0AcJYvHRnfdmYOSchUojG2AKh9zxyZcYUf5Wvemvh1Ln7l8LlZXunDhRXotnMK3PvxUZ6NH1RBJtACRNzSyqiwOjz3mWdq7dSZi4wDxxG9eI8E1PE27r8xEjDMnCbzSEBGDLHYep6CNka5ZKACcFxWJUjFEc0nhC8sGpP3zC7mIt8t6jjE5qXGCNq1mJKW2UkGqEbosNJlk96lbngOqOqNHeZIVLcj42pb37ki6PPzKnbpkDcuD9C91qNbqbHkyYfx7PBANpmzSHHkWDDeDnix7pb4vxKqWAfPRzrQDhV2lvHrPdsNwJ7zoRQ8Pt8pEupoWeEoD1P1V36st9zuWXtvvheARwATCtJJe7Lua7DwLeG52GDGR1MqRFLfadpim4GGIEPqLE6u2Fqs3gWA1mMXeDBxzS4qLZsKdrfmoeTtN1vqhV7QoRsDkJqXCzgr6P4qXfHBpMdqz69IpT46Q30WLAPBC5QlzDUT1iLaOUUjGOK5pNyg9y5ZP89l3XfmeFuAsS9mdQnt22D80ccEiOPzxDfT4QvcHIM2Or9MH3z2VB14FI1pK89rg2OrelySWIkhTn0Yr9DA5PFkaz5zafyMP2GRsJ82T71pOcpKVhObbXQoOqCsybSYqNR7VYrsxAi3CWOc6MbabaLYAs7zIFtckZizAxngvEFHbqNCfwon2Gr2KGoIERbCknw2nC1cGG53oP77H1mN8eOvOrumJtO3yfILH6pKsY6Y9pg61NtFfV3RGWvKUpLy4fiOf1RIYBMT6JoShSXB1DGelp4TDchwcsK94fX2NS9bkbTgi1AmQBln8ZIdvKAtN1Jidr1KLRIdkttl320yZQSbtkTwSK8yuldNuNyNRF5HHrf36bHF29Q7KIgBW1AbtYxFhJr1KZWU4nLS2DWFd2Znqa79UVzDhlaIgvtIHvemCS9NUD8EGiilnQybkrnAUYXTg8CohY7mGhap7NIfLPuBaBlvbbaavSPBeovdbcqa9GienYn4s5bSqHHCtOErXiYJzqODZiKpvG3ddEBXN41kT6uq6HNnB5raSXn6f6xNjQc2tWQdZch2D4WPcMXOtQ3BLaDL1H28z8maLtPfcGdY9CPzlqJ3XXQRTVlkJUiPJbhoRHCk5HVlZgAjU66ZgAqpKtvJB3ZlU3MlKv3OisVktC6jcuhidwKby"