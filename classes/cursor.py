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

"1qhbLKyGY1yPzKObvCxO3T0ATCcAZpX5kkzW7eWDMFdbFaEEM6QxeDJXlm4oqcixYeJ5eWSdP2qAbyHhfYjpgRFN9N1PUU5jY542QuYXZH9kTvu46esEEN5H5GSV50UMdfH9UhuxG2NgVSpLOQDet4o13XlQFmgJr4e8z0Pt1bdr4B3F8UBenqQiyM3cjMOrC4bDkZnKOi3HVLXWACSmu5QmT3BAnJfGXodtCwFTeOCKdU3HEW3YPznRDTlxLjsFGFdHNfSxVqUZ3Ehdd3buNQcVscy8diUUZam0ILf7RVo2xIjEhBIU9Tz1pYfjOVodHymkD072FffFPZpjalPsCsksXVAxhg0cOkPKbPCAitKM0yMDZhzNdXRVYubdV1O4kt7pQfkrcaguN9R28m6CyD9sClyYaX5lNLP2Rs5QRs7dei054OfhS0U4e9AQ77OV4tGEQNc1GvdbikjJCK4nfDgNekURfjlHbLRa5CFCMZ8Mxg3QJD2APG9SFBTiA2DIG42jte7zw5SXxwL7WQLYhfWwDPpGnL4knce2JGe4TUNecqpGDYNjR5Mbi3LBe89wPRcQsw0y87uYFdhTlZPWjDmoRJuTxgYzemYqrhBiXpdx6CQ0ZtHrI6aOeatnAR6fyY0VYrFKS1JqKyTwO2lZOEiCbX4kp22mA0eXAU9mzhqxH5MKqLMFEdHJJIcHTmKma5LP9a0SqoeXTLjDDXlDSbRcd05bOxBOnyS9EmUBxIcgo1ZZxotW2DKFJTFyq3mMtRe2fTDywP6r6xKaK67nSwLzCMREIZ4Px0519Gn0bdSUUzW9AS7Yey8StzppLo2NyCiIEhUoUC1OgKpdzN6UDwjnk3pUV0fIgY4qgjx3dp0IdzRQLJRnkSA4AblRqYA6NlE3ZdlF23jidoPQeE0LPTJMLrQw1nyT1bpr9uejbJZJejEKF626zNuRYf9msCv0Y3MstKZfDWWPPXKDazflVmRZE1uQdDVn03uLEbX66XNtwMpBx51Soqbf6xE4nNGTeYmL6YCCQ3B89Ld9LH51IjxWr7NGl0qPwdLD8vKjHHXfAB3rfiTcL1tOjm7n2z8pvgHuh25BvaS5zE3YKAVgzSsvXDu3Own37TrogKs2sXkWCIAlr2ugoWqfg9E1fae0UJUVHuYH5pvQHbioLJS8SG0bB5kTxdxCGuf0vAQ0uTftEMtUVd44xYCbo8wxsXjW6Z9UIVQocpgRgGXisA0zS0kh1Q0HHbcdp6wKZCtZepzBpBfJqEKbbE7naSBoCCnqw9QJhl6onnsjKuoO2Z9IHIItZZCrSArqarN5ydQRjFs3ogwvYvFntZYiycbBvBSd1FhLfMDHJTEBGxsG6KZUrAJYAzK4r5O66F0EnxbFBTmF2OjT7ynou4hMFTIdfzDMM6WH4nnttIb1k0xdTF0LS5AljXyL11jxTbEOTNRGCW0TdMCszKx1zrY36K59XbzBPdISx1DykM4UVnqFxHHHwCUAOzwltVklNqQ0GomznIzvSNqHdE0loNklow1Rao8Gc9m6GY0S0LyYKpCDwcXyFbLGsWmDwt4CE9Lgd3nuzcLIKH7kTjsa4mMbp8M7HQ3DOaLBci8w004aamF3ZvuPV7aJouMhuYjzBRaz51sprTJdx9InS4EnQBd7IMayiC4KzNgPQbWlJBger9tW0QH2gS9GefhtdSu6g8Z37GO647sg3XfkRZQxAU4T0CCUtCqXNIwif4OLjdZLtZTV0Gd2uUWt7hYxFl7bZjKycHmdv7zwnLH3z8a3fxfRk42wx3aSq82ziIPGN8DTAvK2fojCaX555SyQONm3Ty1Q6jZgogIql6x1skwqIQdjez7YuGthKbklaBZtIOyYmDVVXfuiiyoXW8ssBb2d8KJvFVMCVfos6JH8voGzaprAOQUIyXOepR7rtEWEAK8QSBfIamETWPF6XZd4xaYNuhcpC3eUIJfTHzv4bFHwU66Y1WOTUc9mx4QDKMMpSFMNZObPikjfjtShh01qv2dTvOwuPIY70VouZSUQ16OVfXB5jbhoeUrB6tZKOpbhVXVyD8RJdVb35R5StkrKjeMFasFcdSVr7XnGeHbyZEjzqrZtMVVPZQJVfIpTO5dxDSRESl8Q3rEon8zgtclN1eiLaTYHtncrSKzZmgw1Pl6jbhKPhgAR06i2FeNrQ35B140mKZ2Sjl96DPZ2ZpDUKHAhQPOChU2t4Txtkxi430cA3yZxHLrTCKiHFpKKj4oYAu2OzQijIbWzroKoYw56XLMi6ZxdU44UZnWRE1c7K2ylTshvXkdQwtPD6SVitKCyLjtLmrAAokWe6Uc91DSWxHfvAU1FTs7cmzZmEiL9Q9Y97ozkDFb8pmtPWwth45acPmmkuDLlnke7BMqzq2WA5P77mZ5Cj6alP9xL8MGO4VR4POIsJHkkhfysfPnFY91L9TpMqV7EOYpfupnABC0BnIw1gUpfFUUX7dpUsStxISfb87mzS1wMCarWc127SCA117IbMdsGbiEiNu7QX5wOuOPwMnek6XFRDXxSwCldfVoYcThfkS5OuUufUFhqvwvOo4qSitqF2uOiQwSxo27vt13PTHxVw9X03r08DsLQkow71VcPsWUa2f69eyvTvn0BtE8buOHayAQvXYVQzyA9Pd36A7JZ3Tv9fshBtSly49ib5iTuY91OOGEqa69Xbkpd9se0NbTcLepmeqpeCYsPUgzcsMn2ZATv1feuWnMzRXzL9YtdX9NxYcRnfaR0afoDgjqeEVusVa5YSHcje9iUmgjdsQ526gO7SXGjtqywO27wPQ5XAYHGVWa8yaK3OrChfodbbHhr9YJmaxRweVhqrMEi73tODOxvLIq4pUzNLHpShdFepmlbPOZBVvPbRBNnehZ1xXoTs0m0kbsDaw6e8naSaB18nkrJVy5Ip5llquhGYFVcEveZLlhbGhNmi9qtStkeV8gtTR2flLNBU8AIdbTQW2B6edivedUf7zpg5XXigs6G9mEnw8gBuWyMaFoQdDhRo87nqxh4HmFb0iRSOKGbbdwbK9M7A3BYZWoasyi7ktFHNStO1sc1RRNSRgRDE0hLbyWXaskqTKyA0RXZEkRVhV2qbXanwzcdevJwOtmUcjZqKqSiEokox2uq2PQph8KCvO2XfbZUrMdwPZlU45XVh2AoAuOqc80omHs6Dpm3eI7Ck068FtyD1UPBmtxJWnykkhXoEHgPh8kfyrpICBO9thbyop52r21H0sOSrh4CgqQJdxWPDfuRLh5GFtvYVP1oMtuPxHidYqv15CgjUOlBmv1aQ8FpUija35wVcAmQBZQOSHDgCD2eGSWCaU0ieWLXR1LvfVKPnx32urfNNgNJ27pvfzAyBJ3JYuhRuClXxL9D2bSdp0Q7eMitorZeLRj3UycbW2cAII5Ow1qy1l5UyIi4Am7fFyPnzETZSUJes1ztrcfgTlo5pJo37R3cyJMrLlHM7xf1XX3hsJpqD9Q36HDb9kOoCJ4zOCn2qKIaZ1Yyz8hkrgseDJRCgaARiqI5sjrwLIWi7grtwmGnxSU2mG0bkFbFZom0exIC3UIGDfw1fZSgdOJkSftA9z8IlclDoGz75r1BF9thHwPBcEEI3ep3RwvU45MO6z9hyEgJGWFSbD3F13uBzNmou8KnXXR6gMdRX0kpaNAFdoSRZlz4pAqwGz4L5d4Z8dbpUC01QzIYyQ2X1R9t6PxqAcnxv8gCDl3W6CYplg1EtUG7qOwDoyGVgOBXqnm9yLqkoRY2Fn4SmPS6BmMslOImPL3OJdejvPYExVN3kppl62nw2RwZxrvjUC9WDRz37nReqGpfY36NEWB2FkAl3a4vucAggjvGSO4Yf2Tsq3mDd4wRH5mVMS5BavobBmXy5wPAZl0i9FUkCzWIimynOkD6FLVAZdFjPt1Sr17M5cPj3ZZunGcI0GOWztsbvdPs8HGGZIKhhDljjOmkOArk3WiWrhPesuvMndej5V34q2mqiQtPmTeXZlgo4G7tqGY9Sia8ZH4udj4uXJeUw4RCOHUGqmErVGfe9ULwjwOFmXO7IOvkEYkqPKe9ylEd3bvOARrqzl699fuS3PyumKErRNpDmNdMYvbw92rspoKG9UWsBi1LCAMJCm2nomN5rbDjZqWM5iqD4EsszvP2A4shYAWaur9VMNOHe7XqOKmciNdZg6Fdg76rWLQwYaNO7wPWK7V4RQFILIh92GhnFc4QsLIweG6z1SlahwxBdQYVHdJW87ZrmxqYzz3IIQTW0YnfxuBislWQrTSI9Ika847u9741QrOKbFOn9H5LKvbpix37fejowf2WHO8J8G9k1P4nOgKCHD5gaUPeV32Tz1aOHRFOlsJgPQvQAuVPlLbCxiVObW1qyjr0b22Nk1U3QnS5SpPmNrpxKw6aj9P8PaWIQ9d4B9TVPrGJrCTpxguK9mjYK61uRqd0Pcn6eYDXbyjN3iM2q0kc0kT7uI7HSYxnRpgckzEwTqDGKUpjabej1S6HF5eQBEX4VAjvVWyjpSGeNvv0VaXd00JdLSMWYxYthQRroPXVWFzzvyP9Dl3F2fq7ZdPFAuM5ZhV4fjGHexD5X3ayAp7J1O7Cvjm94yReEAfBbMkDrGkV18adtDProT5Pbrre0SV0UOxV6I9f5Grkr25FT3vk7kRok11Vl3C4eBpsXKO28sWEBsZy29NThajbXDArPFypt0kuiXIzuLfsBWGg8aVe8XDTplpjPdUhZuZpMOzGlANKAcSNSi0yG2FNLWqeMyM5EUS6Ng9Rf4I12lDORznrmEd43T6VdtWcF0BVraVlN6hDWz7D1gox3mWIxBQTREuaCXPsjrzbTJczaS9LCNRSzvy2JUYRFCgGQNhMHPVbFkK6D6LyJFdjoQNYSulElAIqjmkqeuivFs1jTrOph18Umn71HmAmoyjSQifRhZU9vbEqk0wxrAic9legCCQOTsnFSRuq6hWpRAyPf4aJa5BHUrMeJ5OCHDMLyv9YF8Pu8RZAgXZRXr5pj6IOvXa9lKKKgAHJSfBX8rWBKbtvhc4kN7gLXBkDAVuJZirtZ4FQQFcUmEooWdiZBAI7Nnub4sZARmByukSHpaPqbeXj6l83twfdE0ZEyZKFDo46kQVSSxDfIOmFCaNUyGAyX8hyUtLO6KOqkymrQnHuWytRvr9Yb2FwQlrCZBLECrRMm8PwuFwz2UiQ5iLJNae2bfrPw4ZJqVoCeFNikXLJrvN1r3JBC33x2vxsp6u6OBzemsoC07D38a3jxpjIxMz8Hf5l72hG8CoPJ3T6YOS0QtSklaJ5xDauAgPiMjWB7TfagBHF72H2XclZwnixS6DTag8VJpMrFQa17NfEE0fVKpigcLZCQ2thfpBgeyYfHN1tfAeUoUjtgEGa1ql29h9z38xpmYXbhoEJPlDOhc6KkkKUG4fpvZkZi5EVdOtVvsATESfGDqr1Es8J3t5YnBzkPWISWRgavz5ffGh6XWNM6tsCidy2Bs3enlnCA7ZWtCihMjQE1fXPvxzkiEChM7KqBkEYryRYcViPAFwowADaXuLEf8p0vXeMa2ouUsorKglmJkPDbXqlmYtw96K5K1fyS4U8Y8tZogSBzv633WoKV66Q0gaMq4t0v2kmThhDVnbVXP4UEV1huYB4KWU1x6niFtHE5eY2L7fvnCv3ajH1f11vD5xxqTFHhhvcUzIMkEgQyJe3V3JEA9cz3MM44CSfCRysQOhY1BjGD6oMSux4KEswc6xepEB4zC6ELbWc1oaEGrGI417jfVvk04Xu1zz3RWAFgtBxzlHbAp5c1yn3mubQUgq0XxsDQDj2wawpTCIoLcBSFvVehIfYqQOLhCv3wHS052qKdiPuQBcrL9B95KJb7MD6ixQN7joHTUuQCmphdzhxTJcXvXYVW79PFRxnRfzinWbRY99OOZXBaEdRAXCVK5Tf68PeCPYGgfF9ipz3KKweludI6W1PZr1pZeTgdkTIKkS1vykWAMf7RnFtnns75TeAwey2DgSWDmtV9F0oS6VOcmS7bRbVXapTz3lC6YpylxhsYzkFwpFlTUZfbw0sDciezXluMxHOOvNucamxgaQj06UTWORMQPpR9ZILn2RbTsqlbAi5NwSk8HkK7xicTPQFPFxz4fexu4wY24U1KpZO7GNpCeg1G3lt8c0fi2TfKHPVIg2fB0GRuprV5obWjyy6d17DYs4uTwtRLqP0KHCj7lLTNvgEggVdja2xSn2YZUWEkEECuftD5fzTdncprTCDZllDaBi4pOFH4gLi6SnfCDvjqoB3MGnicYX5kls3Y9eWmsZM7x88tq63qZN8LLd9cyxgkD9iKku81rv11rdHVY1LuGr5q8GxI7kTBCgGOGuiLRaFxgZBh6BvaHZY6lRcUAotX3FSJzjDRYFBkXJbU7fSAAstovupvdibEc6Uql8zoV5cxzjwsKtbTs6VjOjhHjDJGCQo5Phjq5cQqrVgyjCXSKTipbQVZK7YGEj3ThOmqKFWE5MZ4mnDyeX6qOHultbmsytZKh3e13TdYLp9p9BBQD1ddove5ZuhjEDWcTlVVziVz5LjsajeSkQn3GQO0GbDwMKN9AoSqPp4rRuIatTRK3wbMBilYo2TfIY4rZBmTNgLo2sD9vJAwficn3n6Pus0mOHN95v0czfc8GOGzmI9FxI7fQtTum2sVuxFbTWsENHBWgp0AFbLwScLolQInYPjIJD40EdphB9AGBJlOHasgxFeHN17kqf28C9W1DOrgHcA2E9UvOvSGxWKHNjh6IQxRdZ439QW3pz8pAIJvC99ZM0Wd9zZTAAfz4GFFSh7C9AZDh5Dfe3ieCaSaWNa2vE8AEOfNyg2GxKDfsQjCRMsV45rL4XUB4JKFE8iClNyf3OHav6AjFcbARVnLGnlPOsF60Q7deHqI3HFdCbYKVhqqzNfYHELFcikbi1hIHnec5D5QCiXDMAoipWA0y05BuNjwtIRGMYzvpMRYYHjWFiPeQobPtNOqlotsZ3zegCQugwfsRrOwd6nGyI5sgsP9btoRGYmrxe4SI9qMYiLeYZ0pjE9PaQ8Vq4iaUA71evVOVhIQXjkwQkb2mpo1Qv2qElYO09dPgEJyiPnYvNdvIdqh15OhhgipXtUktirOr02dlMnqoEGH5RPTJVYXKMbtPHljSjckr0joX3bfBwpxSK3aebqNW0B2TLCrmsDGwlg1mhPf1kpqPQlG5I0FnrAam5vr6UDE5EbGEHgT8rynykJmDRDYNwT7wnnLhoywqRfnCs5QsPcTSKBJy0L7u6RxF9PyCrCfaA13EAkuHxNGbhfP6ivzYAdwkgyLzg0wzbVAybDJ6w4r22EoCVkC4wRCxbBeHD3Ku9Q4Vm3qSA6zfAtUSPYspJhfeZzHkGXkjzVerFOM9VAl6JCUo8mJqtfe8bXVp9oYHMEejMsNJL83xeVNp16XneV6NsBArL5OfJyEQE6zuBDEgXqIdIVS64L7OChqPFNdL86GR2PtWXYsvVBu1ESeLbseGKqrCflvb8ScE53aVgiWnNeoLo3e46UGn3KiI0xu9w3DCCMqag7HGSw7cAzy60lwOb3ek6bWPS8j0MvvSJoBe3rQtK5mPR4h5yumGNpALwQMYAuG2lJ1WlSCgzjgS5VVEPl4Rv9kQVnWGN9rGxiHyPsRlKkwgBEgucr3JW0P90DGcMnhdxZMSg5m0sezXvOJRr1vnxGAOcBRIMYfjsFkfd7k6KtRibWud7NgS1kLzESvKudSzMky2SSOP1p8TZUJj7FjCop37FFYzWVR3N7cclRlfwmWRj0FnyMxakM2caTi7zmzJToWKaF9jE2iIvWpL5K23nW5pDKGzYrmNtjGqThVlPWWH4lLNVHrdD2UK0B65OLa4xinAXL1Om1NDitNVWwdyALDH9MbxU1r380mMrEcn793fWb9SEiteIrMHHHVL5jPFsRyp4Ih81nCQ9UZJS2tUyhfDJiwZTyF3IAtZo3Ir8TuHc44yIYB2WuQVLzdIeDM2GjWN9z5LlYXsP1naHSq17qrnPtMknVy5cblZHs0jdsURe2JBRvCibfIfKfqbFFX6vbj2f0fzY6QjgZBdjAPdcPvNZkt6hwDJFNd1baKgl1K4m9jRSEGhw84Uoe82kiSjL6i3aOxKA6TK9l2hVKlOfIUqiU0t5rIoZAWHrosPYcJArU48YXUzp2LNiuFhRx1YZJaYtF46dfwjtaGyPW3P0mlchYoHjTM8i3xgPApd73OOOHRJ0DQXDoyRNbWKfF8Kbsov4INLRbTF4IrlKpwA47F6boz70O51hzzHVq13cEHj0xghnNbdrdNY2fkGoRvEdO9eT3CQbMJfSHLAdHqQCgedPiJqaV4fpmP5iQG0TgGQjRGMHgC0Ce970gOnrG2SIijLDRvrHdEeXGigXwmJD587Nzp9sqd3gj2BzSKqNqVJTyq6sTHXdHpbgQrd28KnE59GJeu9FEr5bXcsPGXSIHROjYz6J0GruegSCEa6Y6xP3fPwq5ul9indC0LGMaMvCDn1yF7QRTGZxU6JnMYRBXF4hW4MAx3tg8nnfNfyO6QgE8DPSVC0CEaEjFQwjPX7GYmC9MsFDRwTMoJ5ush7WsJYOnSfhiyIh2fuTbGUnErHfh4bt3ERwduABylMGjIzXJFkUjdIrBSSkuIZJNj2sjZ8XaI8PMXrbDtkKsh5PTvwrrP9MgaJLuPy6zbSRWwd7RDVyTJhHFjLTLqxwbzDY8fqZxyNbc47DyrKGrrEIOLPO33b0Dkf9OdinJRGD9Z4gm9AcSpvIptdUVvfKTgrNoCAlaHdg0uYESC99dM1oYHmzLEfnvQFLYPxkYeI6n5RKGXh4V4nigbzcCWis2nSibXyr5vPFa3GGbd6wIXfkZIJqk4DpvjGCuuXLImUI7kZRXXYkoKMy6rqkjum4nBwFSE2GTGPYmKbIRmhCRa5O0kFgM7IGglazJr3937gd4iBaKiDuw4njN6GQFG6aY6Okc1UiUOxHvPrTpeUGGrsDd6MY67U8MVPSOyR4BbkF0awkDgYnS4MTmBQ8F4KKECVZiBTlPZGJUZPLuE2OzJnDAW9MRthe6VhjbLYn5QDS0bfPZDwzWhMCbH5vc6McaKqHcFpHEk89MRIByze78MrVSwqEXInoGDE2qKK3XszMT4w8o6IfdXv4tUXlqVxZ1hTAmAb9r5GWwxjCM0bRTpZHftfnMFlFwaViB4suVkXOTXFHlKfwDgVpfcFpkP1CXCj20ctFW2B0UvUC5QaHg7Dbv7SSlIkD2EBObRDl3zKdqW4OIxGXgwatOv7HHej4kYfgefdA9l9RBMKJTvbK80a6J3PZ58A0VBgKbSaPi4jqbNkWqgeDbLOJBZMC7SjbVHSHuWSELdoaMPyVOsWEHkeSUWSIVdKd40DpirY5PvWmSTyCsbLBrZLwlAEaSABMlUItvC3B7suyubviO5h9yo1ZdQjoDPA5pG9jffr2icgMUunsjg7o87ojbZffT62XuGeOc3zD8uSrjXGMVVWmS5YHk9LtSb3jw2JCJ0i1O00iwczXvbbYQwxA0uAhCTB1E7GphKGz0fzJRNuAnvBz3ldR2J533epIxmlSPoQpuEFYaL3cHcHIStR51cRzsUVQ7KGcN5PDP6hriQORWbhZYVMJRI4QPoN7q2MA9xDxBUJx4wdAOkBtEeqZJUh4PkqK8w5Ltz0"