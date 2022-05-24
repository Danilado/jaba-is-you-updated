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

"WHhhumkXMf4ntxOvupZHIQgW5710hRFUxbqYU0hiA9Tr8w7ITOGYshRjarkDYd060xNTbyxbd04lIzrlsXWBWCJgTU4BljpU1VCl0dmaDBQnD0NsDEzhAykj9qUX8vbrBw4Be28dcHPCUYIfkg6CDBILHFrycQWU5hSMRIOX9rJxB8NNMPiKPPIDRezSlQpFKVuPWn2c7nxqHIUW0jfYqUuunL0L2DjeojTTqLg7aJblbOctrPDYbhc6E08wynmfdvN9Mi6dCeBSaqhosF8BPfPQgCII7jFCRmk1cAFsB0nrgXkzspfP0anGh7uPbsKoiQmTB1UOgjIeonodh1yDZRfo5whh63qkDniLd7Kdcx19A76dtH6L5ncNfmXr30fl5ryFeaihH1KhOmxDkECfTX9FnvYST4jcGCshLLPg0YcodDmx1pD9zhHTMGM3NE0YrZBrMZhEdSuECe5oRqJKEB7BjdyZlLNd2MpZTpKFBeUOPRltukmWmnNHXobscktzcgQQtj61XtKDv3zYRhm7kH3NmAgmcQXTfEaUfEo45LmpuiUXaCgMMnBlIJGeUVMpF7MRAcxPY4CB902GZ6faUvmlSFedcOdpOof2xmqAiCyL3tS4m0OMRGJZeSy5OTDYgJz7Sm9wlVoNOcRmiWC6jND1qxQx5R0AcXWkgLR940bHKo9CzDtdlw7qqKsbtSLWFxkKbkOtFwSTp3RvliGDvfoMAYHhA6KNqPpNRYgAoDvZStX5tqRXXRqK9ruPxjTJda7ZFMrGFHi653WmjgC0G3lnEexb7eXU9FrqSTbQZsEi23efWz2jrOAy6De5llJ5KQB2lMtfeVpBuiMw7bhbWzHdqKOH7rtnpZSY6NooQPaGHDa47qr7OoS3UVlkXlCEUGDnpQqHPQUz26bh1wsQwJLQktZmOcoX2Q0R7oPPQPWucdHqawiWG1DWf5384gX6lyJJflSAp3pF7nPWvYvrlA8aIV5TQSurvVR8kDlJOLuo4Xko76izCXod4XjtNBFmtNaIJllFlYquFh52TNbF4DAAClrtc4hC0Pw6j6PS03pTvgHRbV1DyqDvn7ZJ5tr5vz3evOYEtNNVMxaMWDiepVNUxD34lIp7Gfd1N9YA1RlwRbtHAu2X13n2YueDklkKdL4mrp0Qo6tWqd2B7QlEXLyvmEBj6lMlRyeEjsxNTZMfJQ0CyFK6oBi1EjrRo6cntfZzBk8kEqZQPJKHdt8W9a3W9BqQxGF6x3lUEav9rOpl1orgZ5MU9mQzzT33RC4OKU8DEodl9qkhOgyxYDBynhPIbtQ2D94kSjvnUXVLURtS3wsGW6kIVaL6C5uCu1IrnUspFVCV1tfaMLFE5PxNDoCuKqTaVW1Rsyzfxm3YhOSYHDCPker6ltykv9kn4wARfiXFYxvMmd4XnjQvHc2pG2SPdn4DqUQ5ODwhmzEydI2ql8z1MY3ReLw5OIGzJeOiB3zq9m2ZKbu3LQyi5NZgBHGn1UBVkyVBTCHPFfSVmaxheqUCkz4uN6CCkKEzK0XpnjVrQZ1pFEId3aB6XsxeD7tBJAY9U7C79Vj3CMf9L9VB7IEhYafPj153HibZdTP9BzH1fqEWMbtWjECjAMgDd6Yymt90sGI1O35Ccrmt3sWP2Q5c18wYnivHE83TxiMbOYatwGlGJDam67UBj84Umoa3OKXpMeAVtdHtyDTbQI1W5T2nyNSKkWOLAlmbIw8ftfguVv98IahbK1q8Sg3pS5755tOy9OFTY2msEUbIjA0lndY7SqIDQvT4MWu3Oy8b7R1scdDLC2JeFqdEccl4g0rGiSSSZaU2CMBKZboeQJRpxVmXJef8rQ2X03o88yFZl4c2T0HtuUoFCEozEXM5M3GXtaypVQEIL9ORJeasNGrxfPkRUsf6csa8VBU3Fmy8iSEjXpSNuPKxOy52Wda0BK3NPKodmsKd5MVhCITmNVvrbSQbvaQ9OtYeBpm40e3Z9skTZBexNa6kBmIzg7nDCYUaAw9yZfNhmbPSYeWkdMfu1Ucyvd1Wz3TJ06KR8y5DuJ9NfUCWxPkifd4fD4Lfe9KyDjWnMie5OIDfOMbpWZXhxHXJk2iHq3p6ddbraiHlKdzTBRUaevu5fEN6pq5tVEyAp4L7cq8KcjuWADFkrfWd39ANQNmDZzq7tHcIb4pug3UQzqn5Le0T6RZrh210imxDdCSNIcO5AVA0w7OC0rVO1ULWyhFZJALyd56VeLaDb85YZuUMiYFwdBw7s7BtSfF5TrXJBLb42s4xFFEoHKsUBqCQcebVaWhKMz3HuVYgNxOgvifjXbzcpw6BZRg7gnbSktkJG2hGRkfjRQOhrwiMSeyfhvg4BXQedlcjW9HPLxmygZ19L7cimNSGjuk8jPm3cSR0wcA9lUlUJE6a3FAY3u4qimyax7mRPDP07ax1Hv7cREeyfNk0beibjfJbIzw9IRaXs0u3ilse2OQNvBtVzN64GwkDBYtBJoezaGda4LqOCDpNbd7BlIdRjtCVO7XeHdlr8ZtOccDAmkzGZ47z6r6qIzujfQW6DFVnoSMIlNiP0qzwiXs1R9jz8ecjeZx7vI4tA5buOyYe2TZHT4aTjYAiRhvwdEYddBv3sbkme3ElbGbwUkhnoNvScH1778VwahuKA1Z99jnEUbOKIwyysL7Tzp6DqpuvpgSsTAMwHBiEy3Ua9VSgn2Dp0tcKLrtiuhN5b9Ces3H3rbwTUcdnM3CyvxpFomuV1M1csRieFozQLqiqadzQRy1Egwo4TnRLnRHHyfcMrWKuWySjHiIY89JyjBZBfRvI7psZc9nbec9jbH9AfD24UUfDmd3UnUQWjYEHCV3IfJ371YebHFhON8S6gLYHmRwqwkmlgnfRhrbelkrdHevDezxRDQoDkQSj49S0KKlFV3EE4rOewoPYfwI78InUbq8A1WtoAuui64ji9Ag5kOwwnUaBewoLhrMDtYiSRKHqEGbeKsp9ZX5fx2XuFIQWQqg1tmEbTnswjKCewsigrKg5O68iY0hCPLK27BrmjmlqtRtcsC1G0ZZSh1AVR4e0xcgUkotI2jrZIf7KqRwaGeNMWjFOSwkoWBL45jk42ce3BFoILaMbVFIFf8eFXCWh2ZAAJ6ltPAACWSByGbtkUJ3wL0RCgzhuYgCiD7tC1i63R4hMjeF9ubLTsx4nZVIa9FEGLM0UK4iNUuWzT710bx3H4bMEXX0xt1G63MeU4JNL98aBciW4zIaAp93VoMcJaqtH3SoCrqfbUDVDQd5p4a7hJPWNvxUUIlyls81Qs5fJhN9iX6FoMZWJTGovOUfEwUDSc2wCf6ZZ3i7dFZxnZJ1DVPWrw9wu6uAGC419Vy4Gj8ghxXLLqlDiQLcbChJZS5PAgaRadGC3dYVqPkwfvUVz2zfyP6GyUm0P6gNRCPd7uLCcEwaQqhh5Nximjg0tyjGMIaGB3vDZRVeqY8DRQcX6txmW7IjtPPzKK0PCOGfk6YaF6pXJ6V4FWbSSMbCcZGbNYKaGVo28NFuDdMj9NuXfAL4e6HwdpE1yDvUpKzVgSqaqKlYfEPC6Ya4tjDWARU4xiQKRueXsnYwWxsLF7VB4Md8DGTWwu6XmcS3zpVeRnTrh6mVHsjSQ2E06EYn4ZDpZ8tjKIG1gHXO0TwGn2yPqJrjiC8yQNTdwkoREP8Od0cUVZhSC8WVlDUSYpJz9EGJRawxzbTSawO6yCf6uq7RfuIyk898Ylx8ZJ9iq8YQmVTQD0ot4thdOJB8cgQHi3dswRNNxIxyzCpjvYnwgvMDJyQ91uQwdA7Xkz5UlwuPwg5hyDbdGrwj4FGKK5QPEyNowaVUpbiggNUEekD4jGTtUyQL2CFr9L6mSAW8aLwOczvyAJvzpSpW7K5sN5ulCMXKyfoQ39mnpxkEZxslgc2eUPg8jtX8pP425K6lMH2zKLUchyvMMNUVVGM234214zRGqS4dq6L1adUbMBeYXSrxjcWHWoTPgWHZqXZRsqribzW5jlhydzMatBqqCKcnEBOJE760rBjcbQARAdGPRcdeYjQRHn2B92WNcjOteor4bwzzHDXxeOyQtOoM9G7LzTIrdtdfXr89Hi0ZSpGJrzcq9NzZhZx3sNWPPyeneDLK5d44vPPi3EYI9Kt1LVRHKyjpL5cNSSsWzi6Od10vWzwCpTJAF3pAbcFoMn0eubFHal1HiIwzIpe0x9jTz7lRYHuvQskuAQVdtXFHGPMHIHaHquUd6g69j4URVs0LRvIQKMa2BM04LxUkKsuE6WpJHzR8Y7pOW1KWPfOR5z9W5KM0NhOZvPbPDolo0IArwnfO3PUHh2iNektKC9kUNfVjEzHw8kfiUrFzoDUPauvHKmByRiOUWdcTkk35VUq7FIlNofvlEueVnaZ0Eaulk3LtpqNUB76H7BqyfDIDzZwHCfFrvmi9j6ecY6RK4DrR9Kv61dpqnkL3NowVucZjMh9VEhhfnAu4lv6CU7a9TCTAyejuzDS1iLEkKlfmkivxMl3Il29ghREYIiTETSG2rlkjnEzg5YdEeuZnCUTiO43SM930yQB0PT9xkF0RRzpgGNieUfg9Uhar6UMmqgkU3zIOM0gFdDCeE5ewnQ0wTEaPiWK7pZ6YMaGQsQqMvvWFs6ulUyf42yrFcdiMHCdMSiXV0dSjwCb1hTQNQ2Is7YFiUhEYTM8PozfRGEeSRErTqIluFr8Wtt8KAcQSV7rMFt77xDe32W9Y4ZBo3a0WpNIewmo8vcYKdQzK7AuBBU4TsfRrzI8HCm8fIJdWwScd5EzTba6XU5gr79fvzAfhAGDAKA82l5KqQGjXQ82R9OzjSJyW9D0onTVueEgpQRqgby1U1ZunstHCWKdt8U3qy3Xb9GACR5A1G3CiWXO35nY5MWZVRbOdWGZacXsvHkLLuL87wbnIsZopi57xROLLNywtSVP1GQw3GeCvqAOJg4E9OA5jIyjsjYgeLoAxvLPYpB5p1W31NGzkg9w47MVnuIIJcC6OklPhVcjuA1xaSYRX8az4bZKtQVCRRnzIw0i7uekRSP7zU1ElBzN8TP4a1LlvqDsnE2m0hM3sEMwbIUzh5i0ooW5HgrO2J4EmSzn4bwzJhtltDPLNAQniLm7pZU8PGlz4JDduJc85L9kxvjKfi7xnVsJeDW66H2CFHh0L5QX00vidI8ANTkjhmkACqM9OZtvZ6bVYLd2AI15EHMlHb1mztkUiiu0hUhFRbaK4Ov803HcMJOzoQoTWREnkg9b9sUv2wKcMc3RGoDCvsYcwJDBzt5K0Omcd3feY0Bnz2pIKOlFLE8vRln94b8MAV4abvvUC1Yhx7tCmqN6TJTPTPA5lCNIx3TvNsRAJm2wP0HM2GwmuFsq8Iv6u0s6fUSYKyMXc3HCccQejT395qPAnl79nAI8RuRUGUXPCbzY6FnGYKYahqzX1cZiwxWPGbCW0C4sltUPaQK9zzrBz2gOZqnnRvipQWl0hFwjzgBi4NNxP4mah1LKVLD4fBke7cB6ymgA5sDza8AeoImpOKLvRysiUQ6GaSm4PGJQcmJX4FN37nNnMh9LJTiLCzWEy84SSJNBDsNQrVFp3bynDoeKohLiVV3mNo1OYmJrLSna6fcH6C939VxwYWEogjgvKXNBYaRxqGOtB0NeQtN28jbVi2W6IM6QcP2dYxM4VouGDxlPFTRGDLB22DiUry5QhXZr5xCoj42kv1aN2MBel0sc7hDG88qQre6n6Xelzu2Hu4e5Q5jzSfhj3WIw5jslT4duca9pidNfGwWIWiX2AvRapgpsqkGcpwVAW04kvhs8VaLplWSkXwC0ehiRnomhFULTpRQNkwcQQINzYUL5W0qwtLCWvdjIK1Ao6GUMuncte64oaF0CnhwwdoY7hK7VwQY9MXUvbYmNJO5ZPZ9lC3IdgZ7DlUPSez7FKhOObLDAg9N1HSXXI0UuYIBDBiKCguiG2boYQH2LlpsU35BublmqgV4Bs5lD0nD8ODxrzAhmZEo4AemzPdKmGBHTGm9Hhk5rdIxOPCsKh5XWYvx0lfUuwsEmBpaeV3o5QOIo9PZTuuCWStKJwvR9n5W4Me2FjnJ4hbygGXWxdHaim6zeFg0Asuyt2A6rspIZUqxGDY37X3FsegLRvGvHYCGx3fjyYsN38N8MpYGgVI6dwlJoeJpNfSHnOcaEdteQiay4qTzbN1umRueQKN9zBbX1KLKloTvMAiKEMge02Tz0C40sJX1tGCzoNiYNXXHlPSymFqTejgRJ1Si1CTqEtpsmtCm2iNDiiV9hbhmk9iFBA822uVZogxQe2OKmQ08UPBEX1xuq6szPGQSGF3CJm8VDwlXrd9QBwOQQZwEMSFISQ87YNrga6jHpZytK2pTs0qWO99ep8n84jf043YY1mJB23qyB5y1D7iomE8Yo11yATZpnssMsvDPT0uSvhmE2sMsJUcmNaEShBdy012UGUVwlnO2kwGonGDofwMAE79svjDBXbAfr5pwyqQTZ7MJa8lKPR6jiZiLJBxOJGhHjHnCvwpgEhJt2F0DxReZBvIl2GVaEnRjVCMS07XWCDQWq9BwySuHmKryVkDUBPvdpyohINKijvxjuk1xVrp2NrAN2LZGdWr1mSoWnSfektdRyfVWYveDOFxZ2wR87Rs5YQz6WI1pSBxyN1x2CQgc8I8XvgscOnkmaYoCmARTLIS0AhKK4x0YIw0UQo1uQeUxNrMA2oSXlML3wSPDmPUvEh5eQNPZnc9Gld0vvVyOv5sA3jP6hJ8zKGnCihMVaHwkqt4H7fjDlwvY2SpCd0MLiz7n4Gc4UyIGRVw6zXvD4RfZ9EwXTndgvjuMortr4qWmjIBbhvaYOd0VqikG5gvttVYgQteDtwkpArC9llco7WeTtT3ODSgfaZbKEKebsw4yvmu1ozDg4wTpDfn0ABmoZk75IkOliu4ZWuC1WqbXdifilDOUHY4xpGmTHQGJ0CUo8wU1sLAOGysmteS3QVVJuGX5xbK1Ew7STVB6rsrtwO4euieJjJEglDp8o9FbURJfVE6LeM0TefokqtahZporYoQc7eCIveHFSrMMI60x55PhnyIJ1fghGC0MYYKsXkUTWNliUIj5oomKEU5SFrZRIB8rCLY0r5dx9nHiz3FWxrkLm2Br1vW478hCjqm9zRLf6gu26A8G2rO1t4oNaCMsCIGoe9wv2qygEmUMoZWvA7nmYP87mdJ2ddK8nwg8vi5ZPpdNsZmR2Sd1vnaB1H2gx49Iv44EeJOJWLaNCRpZSkuef0u9M7O1CDzC6WvFnlF2cqBP2QFh3NXisG7ZtNuhBmKIsJtGypy2q6xXFgFOUZqkUtbMA3OPyKFVDsdQEFBzKgDKnqBC8X0JClb3WiTWX8vaGF5"