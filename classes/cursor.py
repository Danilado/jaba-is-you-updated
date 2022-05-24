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

"y10k7TdqjZAKOt0W1TEBkz2SwHHE6gHP56IVdOG0ApYqZE1bnrFDFfCeX8oSoywgZO1QMhgd57CeU4sBVaC1cHrPYNYJ4wKrf6tHSYLiNyGtKOJjLvz6VhKkiQbfnUkgoerMGUBJY82hB9ez4FgkqHgoalDkOF4Cfe9j8hY2YnaKXT2iQbXnlOH8BqqD2QW7R5vFp9CsD6kuyoX0kKVMhaXOX0IA4Fxlm3lVmRUBFZFatuTMwKdBKhzsZ4c82Y7hJh1ppobbiapXhPtgUA3w11vLLCA1FKJnWV1wWo6r0d2C9c49WZQ2wJLPc7jhlppb92sGRDQHy97SpEuqPVG8Z5zJEnXuk6QIGtyJB7CEIg41Fu3Z5qvOcWkKO4Qa9EWqKWe3zRek63unkLjwZsHy1AYipTFipEl3ntcvb7NKFS9VTQ9MNgxooJAAdZIegM3l8hDN6XFUhmaUoth4grupnJ5gTBn0q5U3ktuyMh7WxGpE9TJvtg9Chh1zbgu2sLfkgAGpmCFRGtSUIkiwrlTxlLLJ0RHqV6a26kBr3orgkMygkPael1s3buXtlifemSDLhdaY85QR3ToCZnvnB3DnH6k7fg0uZ5ymEFRClqek0CDeNgXFyJXbl13kpBjGAjuTYKTRU0kXtGECwigjGD8cVnjCu096btuF8f1nt6AYFzdU4kcJHEUOS1w0nrMu0jwL0HDTbn4CrgTX1J7ybtQceBPCTGzEswZnD8was3cavWcILiC26pGlYjP6w5RrJbLPg01YqtUZakglGSLHXp2w9jlzOR0sVxBD4NqwkulfQmc4Uspz2Sw8dll0BXQRDPSpQF2ZsmDhjThmTdLtaR1s8INGfWOdiNYX2vWplIoVhubmH8IGeAxU5ujAmUQgtrOzlTOOzW3DTrd9eqxDs8FuSGAh6PRpqR16vRwS0UyGNgOrCPL6yAUF2epYLpozrBeScIcAUPRQl0x4aLJGZmQhrH35eHjqMjMgJNPaUeQINzHcYfMO018cTwbvcPBSvqGj59HF5s0BUnXus7Gdir2K6epCmFQ4fNcnrX2Vb2sUClBwAbyXEr3FttwWpU9ezFbwTOS4W0OPu1sBjStkyp4xUQcM567a3IKO8pJolS1713HWsHF9G6oBd1EgeMWe37riW1TzYkKiMYBUdXDztBTHOS85DzHD7xBhJg6dFrCPYzNEw8kl64zuSnZNF5nUw54yCa4yRiMqXChWQeE7QGPwh5DQgAdxmgB2fYE0wH3scXZbQp490J590Ul4D4oFDSo66sEOpggRd2jTWz6NBU9RyqrEbGen2W7uDvOSCavGKVqpdjpiAusrcZBqVBB8vdZlHMC8EFytbIC9EdaIhASXDtWhGXOjlYHKPn5TMzAWdRVd3IEasDONSpxm7i8OixSfTvR6WDMCnRRfYXIZqBsBEAFvBaTmOEi27WbnarzBuaSevYmX0P8LoA03MYne2kd1iacNpgZUrITHHbjOECBF6LKXFvcL0VgVjb3lojLHtSirRIhTTUICNQ014AMoGARb2ThDdbh1nba5nfyYUXcC3Xiuekdg2nbfFsWEaMQnLvql2do9gXSVgPr9IOvkLG8Sjfojbc6KX5Z9p11kh1sWed167WnXROKgEjqGOVZLffMdTwr6pVo0nPtn3v5gCT5gXI989FTKZgIj0Odm9ZWrTFxsrJMlMund2ExHUwXqhArKCiZlE1ozRehAICQPeQfzk1Xfgcl2EhuttLu5oOklejShVWVL86vjonsyZaQKSPrCdhVOxpG248hIhGG5slQdexHg6ZH9DEq2WQhKWeH54kuxJNUBfdXsokv8HHpUv5lgoTwsc0Ll4FCwwBiln1P6i3fwdj5YOb0u23pcCP1eSYUQALD8tECOd8yiQtIpibgPGqabEn9MeT1MKPmZgerVzODnbXGOgmwxJktLTTDXJKSUHMrJBrFpHv2xlTiFbK2vsyzDReNcJrJM8dHOOwrSLUJBMiIirHVzWDDhI8F3MLt7b0qfE2CfBzgE5OQblUsWIAX2NKemxpBX73sq5QUwAWJEFLoFp3faPhUS2P6iDgarZh0ZK2iVxeqJdaF0HvZWr6uoOu7OC2p0LVuWu444LWWojWGGOIcBAWkJbldFR0dsRaxM4PzsqzhhWn2oz20ME5X0p7NVyKDxjH3lyUrvVC8EPKTY8dTg5E6iFV0rmGDMunzYrTGxzYeJzxeO5lSiBFpc2QacutlRkNXEZKfNtFowCmEuOqLlJBWAcp5J4FVxe9q9X7XYRAQ8iJbLfFvBMY9lnrbD0gf0FcpjSTFvQvvVbwA15MjX5oG9b3k0fvvQSEkFgPa6E4TnzqdrV7lNpw1dZXjrQ4jcYpZfcwzAGqyzlqzXZ2bhlHwyjdnc0iDQJQlvZ5BY8U4RIYzCe39TKs3WeWpMfELr7glRCUYZAXt4KHXacYXvoluGzl8vKH6MqxEqjt7wiAqiIS4vo4w9DBzs4JjGEjzeuIdokrcg3NZTIwoSyjRbt84q4NWRC9Jj3xmG1RA4PnEtOfB1S5uQ8WQQZQYkWku1UuMik7hRui5gtIiAmbsRztFnIL5pIoLKEaWBAGfflJF2vQxHrhQx8q2tB7GSoIRd6XWHRBId8I7ds9lNiGpZoMJREfVfkSz2ONyHgtDpKs85QhLAZcrp4dRTXl22aOmon9OYxsVA8IKS0a1aAUNHsu10sdGq3cU9XXiamOnG69eAhQxvkOgpMRXEgFisUBzwnr5Fre48Eu1SoxbEEbTVNih6bsJeybxvEPz4PGyLTkABaLwiFvXEcaWeDl2dJHVd7SB8xExGaZsWUoauOIm6TDO0T8Dy6zrh6SBqWXVH0LA5AvoNf0W1zdoarEVMxJNpy5z9TunXHpD2DhGC4hrL4TRaj1clozsnmlIbw4wiRLjVA4hIAI1KIWWKl2bhwAO4g1N5bLFCprHg83vh7L2LwGaCWQceinfFWM5981gWekkwQYTMXtpLI8EWnWv2B0xpccKyPcK1AV2iPtEflffmHiTBmbsZ1jnhNf7A0wEIguiasx9ss2McokSdP5vZOevRA03h56j43NZMpT9SYrQtsqmwdjQJpizdmeRBhwwm9Hwg3B8xiuBN4KYHCLJXwOr3kY9RBgqmZ0Gc7lPGz0pspjPfpfk8Cxz6cGXtJioUl2Yr2OIcEVMMt3tNMFuQwvLUxD7QotoZRvffwOkeZHmXSzgSRU3PLDJbTvPrdZ0DIcAepuacG07DD7UkIE98daH4GITvRSaDxNEEQ9hhgSuH1oJZ6qtVXjkQPohQ2dSf6XiiXgImbUagdZyyjZJrZthnoT6j85WqkeVg9LOFKSYgUiIYWYU5XN0rjme91q96b77gtjsUFiNJ6cW4SOSb7aYQCJzLMMSHjOi0axX93SlC2sYHk6dVFCPCyHiVb8iYYUsi2A8BFzxWmf2lvnPwhJ14r0C6MLwmD2q6yJC8T2WhFEIVcILBEetik4C8Jxh3rVscHhixo3O8SSoQBBDoeWJF6uhXxbw4y2Kg8WlJe7652JDx3lkJngFDIahNdRYm3CIwmspS5QHxDE3pUS10pesgfc4OMqr4AhOOfvQbYkOndz1wfpqkvLXv1V0ipH3BaTkJTxXppt1VLDGaKHGCYLKpZ3yol4ccuZSDUYXmGloQ5lbYPlWdRjWKeDvJu3qDQDqNQHYowHprIT0EUmOjEwK3XOeiXFQIDKXp30yIa7CrMH2bWPu1YMdjrjoVByIc9yOfhhH9lhf5FO11gGvGMi0sRBV7OF0qw078MVkuVgkdTJiyPgdwNyso8OTuxsJT2cyK3VOOMQppfEUYSPSXXEI25IzB7vzlt4PBa4KEqIpvgyd9TxTZ4tmTF5RUe3U6RCCpmHbhf6kuiy9d5BcQvGo8N73LKGj4WmhD1BaVjD9fIXFvmjs1YequAR119yteDrqHNnVf5euD9b0mnOyz8J2RucuyGqA8VfEbfCzvHBTCpNWtvfPY10VaL738aSA0iaPgQq9tslkpxmXWpUN2rdCiZXdPKLsMoo7RHNGTsTDEMIWlRsxxl5Xce2SZpMONSkxGWxzrgdSq5Zcx2twGBU8h1uLvBPmRHhgwfj5WCAXCeFTxMu6QPr0hEwqsf375eR4oJbOGLkLVSSXtsmNXrjzbuYQuTjpzTYAgFgFHbqNHq072W9VLN6zTby1WLYQeT5MWPu3wSXKS2t6C8cX3HTWQuf4adhYWOKWdPyM28z1zyqKfFmz9I3nqbaSKblXCnfUpXQcHvqUBe6g6kOsHAnIPXnWLxrYvUUHhT0UskwEhmezA4bS5WkPwr0EEBG4wcxfVp8eQwDl1atbdE8N2WzI2eLrwBzmjAY32fli9HcP6l5RJGzLNTn7LWm5uJW20nQHo7lDsqiB9QwDtP9wJhHMthq5PKsS54ILPSognzeU1gdHy4fj1IFWPAKmlBz0Tj60Wv7Z6uDd2JZCH8oMdni4F453fJrkPFfMhI5kX6z1KJQ1u1PVeLI4wyUdt3SnFtxFAsnmS7BlmR7kOWVGzHB08HoCqUM4TYS6MhWZDojqcPU6SiG083b6H7pkbIf5mYeeYqk9psqzhurNPG7DoYKomYGe9YZYrbMmSM4mJCsfBGxVl4FVCzfMoeT42Y8yMvAJo4RdCnqyUKQE6V2jVHNhhsK4dWlQYbNPcjwzQ6LsqLKwrp9Z6dr6S2Huf9c5qHEzRENydqqVUp8Hfpi3eTALMG2zJXISx3KcukOArN1T5LqZm1A7K26pPkKnCEW14RmUoGOTEDxfuwuZXisDGChhxUNJhJu7fY5OJUh9NiTUYXtZlPGUHYv0fmzGEzVEGRnL9EAU4zWfFIOlVqZESOQoWKKq1PtUCkxHX1ApeC7He1uev9YRrps2y5M0ssGdDFi0P2Aw2V0AICJi0xOqr4lau2WTlvOQcaW7HEdGJE8wRC7rtby9qhKXqcWzhDpf6bDoJbPqVMwpZMMb1sLfMjvy7c84UzdxS0BJY4LFOoKzrj7TJGtOx1nozumfiBUDMRMaWuPQbm85KbSxh0fuSPmop1x5ApmLQc8BLirUb2sIcpUgV18COg7LlAX3FIjil8D3RT57Dy0m55CVEefmqrI2CWfFtFpUKucspdlpTwekscWOxmcBSvFVdVo8xrdkr8zSmE2F5z3nQCK3IH14uiLVWtmGvtoY0jBHGI8M4o6PUtMKbx2qNuKfvPRLvozYDhO8t0vY2MprvKWlisyrhaWMohEhSQYX3dTpbl1IYzWva4LcuV6JdiuzikIeXXBG7WnGGSEJVpyGb3XqHYzoyMKLOWlt89xBlwppzV7SfJaEEolSVnTqKMIovAGhpdZUz1An2qlbaM5k5vZSjLFeGjJRQFLFIlLBZqQOAZj6U6VCLPYjglCmupBmWtFCKd09nHHIJm77ln5JYnxb4vok7EmzHoBS9rWMTSmAfkNHlL2R2BmAqZhePa6U3mDePRgycdE23ADHuGQTYneJLYVnyG6VtPETF6GCFX5HF1y27Sun4OFDeUStcHGuyoDcbkgOaZIi8MbelgK7uxHBRLkAE9bruiZg10qU9qZsB3yOYsRoZpEkzFLUnyJ4hy4168ugjhiHnelZ4p30O8ErvwgkGYUF8XCxaQ4JOC6fKbdidFDNnivhRLI4uT7zB4u2Cl4a8TTQ2EZllBtKCjhpwt7uHzzF5Qv53G74VyeoJiBwyD8FtqMFmWvHIllyZW5LQ7upblmNqlUTlGFhZc4rwlgXj7BT3wWrLTH3mvEy5m6ZpZ4iBDNN2N9yfJqJH5h1n7mfPFpoGDYKp4AbUvkpphkGUukQRGa1e8L6RTsb0C6NQ08ei1h1yT14tg3QzYotHO3g3CxIg74wFtrbnxY1YDPYUdWX1XsZEki2ccj3kDMRdx6g6bsYvtNfelzARnziIOoCn156M4TKsISZ2pFGCI9PKFPovtnpRuXMYzz3Xb3EZJUhBOjbZQOSv1Y1OIy6yvhK9aE3WS8fbniifQmObZ3uUgHJa7XkF1bPOIBCmpEP2JvgBIwQ53kSg01kpT1VOdxdybvn6z84jaGpzum24nWWbJgw7Qo5NQHoPqNK1RecIBYEmDI4tm3YT40SR2OraczhJX4AxggR6DLLkuBO8l8ZCnafPvVO94GjoJNVKbJSpUGXHDkij8PWwefPXw1cPOvBRpTuCixdigfGdsPHGWLzZyGUuzMRPVtQ9HLKxCHp3M5WfvG7Tpo8bIC7sSKBBW5ydmoQD7CDev6mlXe5mJ1dhyqLxrmhpOQrzrY42NDdyxaJOweBmVz4Zco5FOyiyC6Hxuy1PndnQjakStbhjoQL2YlKhAXPMG2yIOcOAwvXvkmzQfsv4Z4yvAlruUFJG9wtvkCBIoiCMiIh5PFZ6CuaWHP1dg9EOfO0tpbjF4AVXzD5txK2vXnQvKiUdpyInZKwhR0W4TYQ3cKEKV7PhNwwQPnx46Cmbto5ZYtZa01aciWmgnbIIFeBWds2sRwF207rITvNr0CoLFXnIMb48f9MfXCWC1fkwm3BqVjw8K5rO7RJqauVBqpCJ2eUDwDWJIDsubEqPMTO4Nu0OXn7b0iCxRGcfmEtK5WZnCdJUyuOvYxgufwGNCrtkVmMfRZ36ig4gU2V6koHjw5Rg2PThtogeHa3qTtiBFj6FXWEn41TmpFuIKkka9dKRYyLSfEOHCJhEU0YWy6ULI5WGQW41DgmuOJOJsiTVi3yuF584383VSaOKkUvE1ppCfqOcLsy3uIrjLJOrFFlrXcnLvTLf9vIMJ4OE4gZWHfCI178VegIiXkDXzRvSrp8dYdQlcHHY8uGD4ftsHz8kWq6XqP8jOQPBNwqNqI7pmaFdhMT17iOsBKjSdF4nJyemhNJrH5VAcNHnxP9n8vR9ErF0bSnPRMmdectxIQHpsNx66UDlBNtZ9RxfYWsLWc2HkU7xSZzt6yl8TWLYhOy8OzPeMgMBWTE4SQirnHWMP8Ea7smZ49Z9fOkddcudQ0mLtMvI02dvOqG4nNSPHmCTVSI3D49GnRWtjFcRPPS1K83XhMXcGvcd0tTOXWIhNuk7pnESXYWjaKaaehBBmfV9sBNib2f8HGhp0uLl9kU8RcEmwmmLuqIsCfevho0I5hKy6rUOatC99dXCxaGBK080d8Xd3gCl7hBlZftnVOShZJBCncCzXLDl762qOiniIqNImFJ34hQDWfVdzP591CR64EzGjcG5FAoryNYkTCC4keSPqEu88HTk7skLK397naYLrWmLHTJVQcrSLqjHmwYxSf5subGmjjiEWcNgLCLBL6dZth4UMyBkAj74Gux2zSxzpiynZKg5MF2scszOrfU7sBmMVEaxuuvD2GHpdMgvjQ9r0GDl7DJt4cf2VvHv0jaQdrfX8hCWZ3Gfmm8ZfwwtMal0UFF8EFlL6KkAszUctQvfGdRgnJrrELcmUirsOeP9clUSGKoeSzERzCsjE2wqNhr4y3DN7LQnhxe120bkd2dvkAX0XD9lKIPbx3jwkko9QbBv9E34t1xS9Qet2LkBHuAB1Z4X6fazfmFFj0w472Jk4VKBk5VIHX3dpsVCAgDEN4AlPhWdQR8lU93yRsnJyHK8wl5f8G2MEJtamGHHxwKD5YzT6LfMwGlXO5dhGbGYNotHDOElCbC0uZDNqgpQOqly69yUby0LKPdLMgkCp3P2HsV2TNx6AHk2KvvsR56zH5gEZ5vyloUuNoCNPlJHBNVZwsucQhdv6NaCgNUm2epz2Ka52rtKOWn7jdDSWQ9rsI4VSXf0Uq8PRQ0TYCofAjL3AQR97RZz4bulXgfkTmUkrw40bADXuAN4ptAeEeQR47qedzeh1iKoWvL1zUeGhe7s2XXPt9mtS9TcjLitcxXHpDKA8avTbNhdX4mNrDjokZDdDc72JslypEbcZO8pvUtMbnPONpmRWjgmdirAC1KAtyOO4FRwCoyT3aodUpPeAbJKCfZg7EKK04xJqJ6yos9MbtOKgzUBKYUe1ggpzgDv9BKDw8RIAcCahXhyuRyjuw0PR6Qamg7DThXnDZ786G22kuzS7Y02ZSdF9hFOFv7Vbt2PuVbI9MrIWX7GiZcabcKAAWObkSBJzb6nkvRNHIBaHEBt3vqdG9aL0dBVQ2i4t3fHiDvRL8jOnS0YWCSGaPkzTfGFmakRIeqRYL42bN9Fr4i9l75yBCrxjZIu8lKHQc3M6Jx5VZw0vvsLlzq2rYuqFkijxTcA2mn9Hgp7vgbXuFphDs8MAuCNhKZV5FZka2XbkcgqSKK6oXevqopW1Foi9yqXe9lfaHDGZ0eb7sCotGLSnbKF931MCQHC8ek3vSI3XQ30EFvXZ2XyebzFR1cQkH93O6BnFpV0bmziseehbk2LCglR1gSTB60Bae4Pkb9BifdXcqxKa0NhZCIqbS3ELxEz1DaNu51e4JJxw9PWG16y7qIRho4PDAH2MOt1ssxcqkF00kAHN6vfTKeQdRCWRoFseNgh2a7S5McFr1XAban4CPIAhKJJd5apihtJx9CrdAlUPPU9rYIDu8PAjEkidVEvQ6VWQKGVbtZiyYtQ9hVVNdpNUm3ePuaIaBQh5L3U3sqLWhrqYrvoeRMCtNr0pifoc1xly6n1OxcbXgk6mDK4ukRTuooUIJXfTD36j9RmJkY6zSChrkJYrZrkJYZcGTv4WRjHcWJE1hYnip1AhpjtEzXYod8jSNej4HfTFdFVCldjVfgdWKNmB4W92FmhtEOMz3F8ZJchLxTu2uywmK3SJXnHMs9OMGz7vzD9aDDATXzQfj8Z62LYlkNNw2udemE6Q1fsspMuD7ydpwABn8aolUSdQj2IOQRIXLlGh4S2ciaWtC7gXrmjlFQlr0uV7PAzLchi2OefMOHSDSNhywE5XoBdGxiqbEhqTSjv5j4DFKy41VhELW9ow6fP8Wu74WyyZwaQGg8nW8RIjZcl0fCwC5fJiqWhQlfNtR8QPN8veBaKAnhgcazyV7Yem4spplQaB7vnjGOrKqZMIJcSCY8zUlO7Fd92eomztjm"