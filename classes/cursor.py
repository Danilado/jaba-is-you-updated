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

"bf3Aemo8Z9PRqKgCrhTkvNthwrA0fLoBmrX9dEscooHlttqxnIhZPTNHqynFUDwWjMMZ3s4mQ0srtG37gbkhcUJHXNeYUvH6lj3PUl4LwM1ZHGYTyVxFMBs5mMyx2G1A9sEDejDKs2n1X5jBYsqQJ76Yj6djPKTn948Z9RmdzYuBt3WMruxG74200TuQjsQ8YG242Sr70NKBgbY5Q3MUN4HIzoKGW9ei2gt8pL3FwxxVp433FwYgrfAwmkQn4JEZPHbfl2W3rI0aoRoLUQGQPEAxTEzlcuCYP0bpZPcv3SZOqwnoVgBUT4PZNCl0Ve9NqYgdkAiTwvOCHpOrrp2ZCnwgKINBFZ4Os3uWoZi5nPFJdIAkdbiFvrAMGYIL2xIoektNN34faD9Tf6ZosrKuKtRjzQ7MlYTWeQk8Sw24u84Q8tmyiJ3sNMGmBa9xCLJJjdNnJrF14s58TYXP6mO3jiCYCFHwF869SnCpwF19pV8284i2bif0nWcMLoLltEwKp1Nt4QdO3Gg7RilLZLBopj3DziBZ5zjeJfX2mIsxEx8rsw9UrEEqoMWiLu2glXUwOlyL9aEhhEPSjohEIMtVRg6CGGx1CJ5kJWjU99uSdDIf309ZxhjMyqa6bbBIHbfT9W2AcKUGfUyb8oLslsu1frWhursCJZOM33QK2K2F15sizShrDgTlA5Of8VPu2h3PBMUYcrllIWO1HOdWu5IWOzlYPC3lFPFMa1XF2dRp33ZP4llq8dxPsJ8NtTsjbi0cHepkA4S6tmb2iFDlWRNFX44rEjUmjW6EZ9q7TPVehzGrUKpocHMTCWsc2ipXaPNzePXLzk4jYSayupbyqQEYAM4CjdLFJ70Dtf4PP4GKKWlDN0pm15X09ArhmKXtLTzua7OSFDUmOp8DfRa2jBoJgOcR8lXEB3pl081Sod5uVeNU5SskcCAl6RHbbJxyiyEAlvMksQadp7oI1Sb5hHCEUYCAjNEoxtPKNBg6PxAWizkuOhtbsjO9bFgSiJjM0pbyEfVteNdvbETSy7EiMrat5XxEv7tuLnFd1P4gLSIUdC66DvtEq4bqQvAAOJF14kJDpL78gAx2QaMfdZYml7Iko8YbB35Ej1JVpU4Q7hWHI1S4YDOavce309AT3xLWFPbFq3wdlELpWkUt7bBPfW4HTz7ubdIl9wqcfvSql2pQDYQ6eKy5wdhwvUBksyNAxGESCtJPw8yEpMderLXMZrRXgCkYKXEX102NXD3MmmeKAiwPagPVoawQj4eNwrT0TDnDUBl8Cs8kDF5KVtE6AOH0kFBDL1j8yHon0yIi7N0EyULAirOIZ5Rj8miuggdfi7EeeWWhmwmZA0Ak9bt10mElb5OYxYx7kAAuzJapnFqdS7olViIFEgepgPVsDS189lCtDz51p2xHqHALUhTuniwMY1AATTaFTDXshXwdkXJrhoP6lJFLUv3twvdB2iPyKylTBryWu1gHXRNwj13p2pPcu7x2gD6cz8VJ6306JmmB4PWJPFDYzmcIVsuHOaZEGd6NMegWcbjKO1xVvbclx0hAmRzdkoLoOoQgtzQnldSJrmLxW1U5XLQgGT1J7itnLcoKBtIiZyaNuLJYtGdOZY8ttMhwmsZLH3FMU1MMR38tyWQBUsp5Tca9VSd2t5uRC9PnxkMkuMvWLmsTeyjkd95nxRZJZi8EuYoFrPz4kKn0IwL9PBTg9VGuIfiffcPR4jYz1wPWRof7tMwLDsnma8shiCbUP47a8ixhRxgcrLy7L4Gz41odFlxOEX7K4FYpwfuLU6caDgzYdUANtwWOSTR9fx2ve5NH3Br596ZzIQfaOVaI9T2tKlaIZ3j23I8dW1DTrM1mO6R02Sowj07WTWgiQx8sEErEKLOW8J8QYptcmhat6E3FGTfNEUKnxmEjSGguRmAqM5iXdUx9UtXJoWHfn71heRY66TSE5PQIaf5wj9Gc3aF82VVSyLdd9qofb4jJoWAwkMk1mYli8bu0geQflBVMfcs6wKcs337jRqkFDSILAf8ndkzAvXcT2EgZqEVsIz0qunnV3wFJq2GN2FOZ3Ju73iy3NWpSjoU7pfz56ygGovZ5ITmMmaJjANiMXoZPMxWCSI5xozGhO92eEoOHSfkZGrJgCc18Ix4DSmJS99JnL2je7c5lXuSjoqzCrSAZln4pr7ZQjbQOeTBOgzFBN5pVJomaQqgXZp3AbMpAs9o0cTn46YYe0w277CoqsNmAuQKtTopWjdkqTj0oNtzvwGcJZiDGJvdoNNiJYzPc59MHSuVxNr19phTi3RghXinjI00tM5T51YfbyKIrb66gSaNAtNXjqnBpLHvz50g3nRMS8Nzh9aGUkvLaK4nwFTmgVlfkIJwLQ1Ryw4OvPIiHStPWeHcwAQ18MnETb17x2JrFJmxWByxQqCRF58rNUOpJAw3o2oUzXCyrGonVYCxq2h63WbbXhG6AJTmrkvr0SxgBV84v1db6d0f1IOSTNmTxfcvmjBkRi9A2hhzcPVme8F1AQjqbHgdL1CSHPjlImqupqDsptJVLcUpvSB3pzUPVfibfo4OdPi6GQzcabqyvErnX7OwG1Xb1FipCqm1rKXs6GBC3QgzTNkNIrlr8bQAWEhCQhw4kp2Of8NwLlXw2Zyso7vW6kmKQP8Ex8WRlZHOrwcE04mtBhFTf5izY3ZDpMK1RsbsTZaMBPrut10ppccTMNsi2FoNT8AngtPhjcrKNXVGbjzfG9zEYeOaDS47R8f8bloyt3OhvZjldcXrmSL20QWlSlYKC09C5hdt4aT4FXe0olyRNYA8jxV7mq2YBICmgByZhfUgXTHaFjVS61PYDhny31xgRPU14EdZi0QKjercCuLuxg6tKxEuFyy0icNfIX1iTxd9TfDIfzDCsBAgiOH7DGc08qIKIrlLGusROK3oI4UJrjNlUZiktsAml05Ni4CyU3iEwC7XRFATeMj33QfHfa6CTBvUa2iZMtNkF3NV2IedFPkbpvgSB8E3MBNLpbY9wPLgRlG8bVi8yMQhj1hmUVCSfumkb5WcBf015JbYmPukznINU3juSHonJUsJlpssruZhN4D3FPyTOFwXbFTepFZbpY0gts1Ah9OywwBpu3pKMV363hEoPpmJPxQZlSCn4zu3jWz3MxTTmbYh0fFqaGoUGR8LtjY99WnBXSIp27xr3CffNDOhI7oQW4pY27w8yJbBh84Hgk4tKPioRq3iC0iZb62Bw5CaY75izPgUPAhQPrbRC1CGynjnKtiPZuhSWVNc8ChdVSXFOSbzq7lC1GVh4EfW5nQ3AtjcsTTk8Eti61I2Y6ILx3cXYTKhNmJjdROgUIxoWMkKUikdBzRu1pPPNJrZuPApQbu4VlJANixFzdQfYssuKcFkJw3SgaT2vpmSPx0CEcMDQVEY2Rao9tWh7ZX9tzfYDPWIOXumfHv7ZVKcmPaRXuu3GrEfAL0WlRioWvHuzjcBrIOzC9R73wKsHBFlIJbCR3q3NFWFOGvfm45MDVY2sNTh729HiRS067cL4ikALTGOOVc3cYEi3dfU2LTsF1UI8MYOzpEOo5KTEizcx7AYdPHWjA89H3uOfIBVp5fUv697vClOx4PWnQoNDYzyNTHeKFGRUZnuRkJCfKLuvg7Fsp3xJfkFqUgotgaurlpG3BwXB6siIz5JsQSm0DcahbpeuIT8Up6wcCZzVc0vpZhfJZNNOEXWNCbA6IKAH3MnEMUSpST1ZyAus1AWrNMYYhWACwhLVqDRSEe0PjEuOTqgr1jWzHCniQlxrLrJcZLqzOoKBaMztJCcA9cUFvHcOalaKHiz6gTfls5f9oMCf03l2MbphCToW6KI9gTLA5vKj9kG49JKZBLvZ7cMhp6Vgoer6o5ycrq7YO7gSW29FhSDvnZZEQTpHlybU8ZEFq3N1cXs7G9zgDTBhYydWRDdSxkZdTTFThLd3v4nPD25xFHD2G5ysTQFV3VefOn77mGW23ty9c6u9eE8MPYXU3TFzMWMa94WZWv3Ku4erLY80vxScruFnNzEsNmekN6z4xRI3CuDSxgs54XcpflDCZlMoFUN9HkFIJ0qlJ7HFWPAskKPAkIDgPqeKiEUJdxgCzQgL4BqvREPrhyS8pmbgEPopt9fvgnR4sKWvzgk3wldfxxetJ0nNhTCRA0IuEFS6QjfFNwFVAMdNwDmnyvE4wNCP6FarljqlcMArs1TtztIaeiTTSa6ApxzvFdXh00ZxUWT6rzqvX8UGsRSw0T3vdUT6KGxPqq9YJryHo41RZ2DfmpeV8MKcHCGE2FvnRJTFPH0jzn9wsfT3DHy7PMSMdw6RXeuNxgtUAeL4bo4rZSxRicdjLgR333jZx3Vwf6ZAWlPUNa2M8x0X71NXWkKRskTxxeJbLiy5TpQY7gMlieXQ2Wpvm20Rke78VaCOLcpBSqh3aMxiKeCLsUcz5OZyYlCsaII0fG38U2ANVGHG31Ek1l2dKDcKQtIbgjV1GrA1TM2bGdTG8jGWdDq3yTV7GiYQr9ZaiAreEnVDRX7eoSsoWFVChgHWcnEZRO1pI1UCUdK55UIbTqYeAyW97D4DD3AisQKiO8QOIz21lEZikX9XmdXuURobGUPGL2odv14WWO9z93psRIjEXFpW3XYZ003zhHW7yYkAPUCj0UIYbU2SMfQiFWF9xZHDvP8laypiTxQiiCSM35BM9QqL21GbppXClA3iWkoPmYBBtVwxRluiqTvomKYDU1nKbmCVdRVW1H4EnoEUllIgfMLgQ5wGDtlMZiFNRNOxxwKCzyjBtG0BSuQ7drYtHQipmHRg78pA1YUtXyldExlqYE6j8K7ffRsqIiEvP9VNzIOwokjEXjoLesiz9gHKFiQIAHH9z3Qz6cEsfLIQGtT103fZ0q4cheKiQf3MsDdXAlydGg2ZPNyrohRDxMHfwwi3O3gTijGhtecdtawqsior5lsnAsnu9wB1Icgb0Z2rkLldo6J4f6AVY8No1yufixsXHJFYLWPaZis1ITMW6iNgP70fvTZCp0f32HQiW39YZjNm9of4MIVHw6pAp5dPf0cgQePmrxZp7k8mQQbwrC73iaCHVqGKjhsiaVWvEFdPxfa5xo7ODerQDW8lYT9lXRmfLrjNxi9onVz4ifDalHp3v7o4kBZQpphLnPBLgLtmad4F2HRJTjvsLbAvMklGFnIVPeY2Pl3SbuK3BnXlif1UMtyBdCBvTG9vg9rZwf4v2D3rQFEVUsEbYesHiZKBH2SKys2on5QmKOOd3HLueUfHyyJTCElbrVIcz55PfGZP8Sl0kY35asIA5gMbhmZ6o5pQIJ79hzvNBuU1mdywciGO1aJY4lWk3jnYaDVHfhavreUGRHBZXqSDPp1d6yKRMlVX7lBDNU2VOMrTX1TGKH2LrWcXnUFlO18ilY7u0Vs5WqJHN75YfjH9MawP6nlFt9uPD2BpLFnUdUVEG5ReSpRssxRDjYZgLfCGREiSyO6ksMgNpbz5GkeQBUN5RvtAg7JjvucA9PeOUIoCWoN7DtApZC0S9s503T2pCI2v0cZ938E6ibaWTiDtUNR6FufElXuwIwJFdlP5mNcT5XV5lPqyQNbYSPpgPdhA9f5iZuuwvmGJQD9V1o3omhoiuAiHSV2Q1JMknibZsDpdZoHVdUnR84UXPmBsBAyzPa0ed6msN6e7fPNNU4ZcCk4gG5AIvt2VAS6uepOGIvpkrN6DhoYhojPAokbbAcgNZMNFSjoTM3cGbocEGpjXkEVMiZiQELdyxQa5BonZXNsQtRBV24NAsqnq4xKEEexXmVA79WutEy6S9XHuHZCkOR0TTNC4Ut1GgvD4xEnLj6fwkc7e8IrrVDNVHHXreElyyIPv7cyxQVdwH7sOOnH6enkWYZiCQltaPJujleVESoAB47ra6OxzVHgDJbQX8Ey38gFkBZ2cEWP4bRMEL0I24KWVV5iT5y4ontNlV7E1d6xZUAaUZdjwfQwq5aBGsn1XcVAFxE7USQ8SMiNbSZDBRhku8F9ErrqvIoqFIlNRz3KHmmhueBoXMow7JmVCq5ofRARTsnizKCXMx7eFHyfo3iGM9u0NEB7sZ5CJZV36EA326ayuMgKAFhidITnKnyPLjIMnTvLka1aEcfcFWorfVxhr7ybmG1wTgYZ27hqxypovokqrPj2hnKyS5nFHIfstcgV7XGfS7CJFNXZtQEJpheiZxX5Q3NTErOz"