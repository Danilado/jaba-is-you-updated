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

"QU4sTqfR2OVrAf8tnknqcRn4z6F8wbnwrgMOv6GsTBZbDpX1cd5x6qUXxmsvWUkkU6TfjUj2ue2NGGoBVcuH9xlCv5KptOZCaND7GktkG0n6gYzpPqHMdnnqc0JD3PwZh6MTO3k4QTsuYBfOGc9LeVRVukptrOZHPI2Gt5k2K480birk6KCQUKth2ou57ZMvWdUhE8SL8a7IrzPrb5nG2s8dl6Updp6HGhpO9fqXL69HtjORBy6xHKTSZgYRph9cmwXHydAXGrcNalQzjhjsVWwaJPR6XZ4WacgwIpxrJRvS1BoYm7lDd3wfKE9nZrJ7gpHgdmt8LI8L5hdYYFFTNnSF1R8w0wOOCmlRdpjUc1ooljNJxre2B3QR9E0w47XUlJBc3pxc2hS4xrI94J1TVZctdd6ifImAZ9gRyxtfM0Al6IvOVCA9ZAX8U1NAzx46MqugpKJZmVB25YWC9WUtzEpJVxNqdrIVYBrR63rLrPal7cz9hreCMlkbdEwrfiYV2rhjfIyrrs69AF29q2zHh7etvhiXUuc5b0P8Juutz6s6TpYe4vw0aTtT18zVLCCYTT47OQpjLekL8KKiQq2wAKUKjHIPUkXDaqSIT5JkL2pxIwsCqyHcdmo4wzeqrQIUcqejh5sWWs00pLM6FLwotCi6Gvy0r2kSif84ZngTh485jvcN955bfuUKVuxl7V8OynKnGcgDdvbtg91jW6gK7DdMsLpTSaIkd4oxrzEYHRUwZhq98Nv5mHZcDyDvKxW1LGlvlN4DcIgKmB6eqCiCGoxZEo8PMH6IAMgHqWqWTjXP9PXceUMK6Y9cgukdRH2BxKBjxgFAJD7pLFwZ4mxQ6g8RHvKJYoc2GQWeZ6RrjQuakqvjnIl0aCfxYkbjXtYroxORhUGFEl7BKK4DTVLpBwRKhrx2D8V2iXxQlYndKXbPKGHW0NlApLx19Qwy3kaA5t11xWitZu582jWyDtaz14687uXoeJpLrzYJeD6ZmUECzi9BLPxcyPBU1OR0BgpuSGmFInaBOvNOQpZcvsnzXiTeXSSU6OkLli0nJdumOGSzpsujgGuDIEyXIFHVlFzESvfEtk95VIMcLpk66am4p3y2v94hE32bmUOQrvw9WbNfKM57absNEKXYgJchi0P1aawGbpf9JSIPoayEb2kfnWUejMq7EW88orj0N5aWEzxtfQ581FMifwrYbMy7tZVedyUe8nmqljrm7BUJJIrG7MTWoj0voip0SXYYMZOBQIZobTcguZOPEZN9woOtVdzqu1XOEC4XNe3CDOURCYo1pIF70PXcq5Iv5h9yprrGC9wyLdgCSUUB4uYWjFC2ZKnOixiVdR5aiEEAPpyG4GXJmIn7gE4ROQosrV2KyVhAIYAai0dhMxSLhLnDmAC6s9eAKiijHZ0JeOTpgo5wSPx5dcllMniHdATHWZbHnMyewA60pKY2iGHgnh8ccXWMtsN65tiR81v75XjP5WEASp19CUKcg2cXi7EODj0OLKNvj8j4VfeLXXreABBDM5dHjVEnkVr33rPjZLvcInkBBhoxDS7oUuljoYWjj6KlUjDssAtsAQQHk8X153b5WnNA6g9oKnDBqjkCBYnDtlDeeMWg4tkE7itFYazNq5YTdGvaOMx5xuNwbiXM1ZX0H68AFxw4rteMQV3G8EpOfo0NFlFPyzamnZSmOC8y69sRfroZwfszNFmMaEXXHOfcY5u5vIaZTiAnRiqTkGpFPxddZYa4XjP6YLXFwEjrNROYXey5NKr0uSh9jlXqSMB7HGjmpjnkk2MY6PuELmiACtHeeTFkrNEaKtWjMsWo5FMk9yWLnaoM5zNchMtaLFDNzGohjZDowocjliwk0MVRapiFoKxyQfqCNvevwqy7crVWkrr254fSgWNbdsoKFxAjGMK7mLms0qBOtPaW1FxIqKE4hMFeIriMT4VExjBruLyqdXAJf9FJf2X9Uz8ioorrWGL4cmqAeaR4KM1UWhmZIOa7aoQPeDfFwSSYahqdrfCzVlNYAXKC9JdOKKgScDUxCsgp8YajwJNfVwljMBTGlZWy0ULXR7LjI8UdyEPP51f517CwrZUCnkkSYnuEqgDWlcVeXVqs0YTEQcNn0vqt9FKA7S7XgYVdukjLrPVXBSnLhQZ9MsQeUNVh0ojBassBs1UhMBOBfzQKwvQG7Q4Y5CXZQtdmHR6Jsq35sLt3TQPfB1icFVphCipUhB7CsVfjPWUxAOt9qcaG6QbcvfHDPUGkhRCD26KXnRkJ0wnEEmTJh8ITuqBuAnJWu9jGXRA4rIQo8rRLRhawtwjJ8zFnXIxHFmz53knHjrp9XhIFGeMUx7QOZfM0FIyOXiF1NDGXgifCdIJeBehZhUgavX9fUKld9RQf0MInVQueJ6oNykykFspkRl9pIgfI5t4fNKHPFBh2mjA4Af17MwJeSHCG6wF82EQCOWPjYpeKug3jRHxNL9Dg1kTddFxrjB7OMUzQdJH334s2henSKg9QYF9BS70fohIhDBiq4WnyDGkaLYHSSVwWlAIsMiDLDqMr7BBaWUVLineQQ82lnAtJ1sPCycXH4w2IBEuEzSFI8qUb5coXK0aT5bG5UcejNDVSt3Uxmvnk1osuVGqX3hGUO8gwVwxdObxkjaJyGb8nO6RRtlyWhmeXZGg9NE6GpC4qnZwbpYSiqm5892KB81IkKR0Lm7jpzfvh80t0IwxBZryKaVjoZnET2nBntHbWeeSjPPoAzH4QLBptumu0okdxIkPP5LENsmxxyyIuioyalqwaE6F1Jk9XuGjCC0US6e0lXG221wK7FNRTiSOBaqYqxwoDoIJhQnQpXF7oZ8xoGg3se9rdGUJn3D2VgWL7H6msl9vSFk8hELvdHMV8Bnf3lPXRYrBbx5BbFVAf4Tkm3yGRbs26dXLHsw8dTxZBZO6uLhR4AK2ABn9vdwtscf7TGzk8FDRnR5THc717yYvSejWW12CXLZgW9XYpOrKGqe47XYRRCNfvrnuldt1QQTEUVFpxRGraDVjlaSK0owftHuo8517lFJ8obiDx14ooYPWXXDqS2k1AIYA6BYO9RfstWRr7toAgNdE2Bciqc54WjClRjxZzLdix1lpHaARMJqwEyWbluki94yFMadwMqDGD4uuLZZHsCrToDleVXMIREVBoUMnFDvB8EWqPKhG9VigfyGab3F54exSSmD50mSTFOFV4z6ITpK8qqGWw9Hmd3Fux5hfEG2VAlcZil2G3lRJLZcZ1ASpQMdgGu8OWCn4H6haPXQPey7NlWcMv24amdfqX4EwLXKNbxxofE1fQsUf9U2zP4LqkKENRYLzbCY6oIhguej3ec0LM27qMNhhTnKZuGc3g1TdMaKoqWXwcifHW0Xa0d90r86NoPjY9WN0XyqmY0D69UD8TSoTz8iWiepzUrksKrg3NfumsuRIjy8QTLexdQ1Wwy88eg708LLY0qvEU5OL20L8FSFw5eW69gwCS1V8yeqIFwoTXr9H2XtyGUCmiL29uChi99zmWzPKxpou6AqJJEwmK0hzSA4S7Do3ftwhtFB6Rrr2C2PeBwSTsD3tOHaSWbm5HYUCYe89MqzIzpYLA1DGyiRy84IRnWohauZUeoVPxALFkcMImVP6hLUsk0OZAtNJljg9WD8lBYLLu7BNh1LPq98gf69PfnNj53IkJ9Cgv7z63aRaeH2EoVQw0BYEenhAhSNSWUePamyBKry1BFFwBVLAcPdvmP5CLEexcnN0nYkaLpy83xGUdna4lpRitgDUmMapJLl2zPCRTt7pYs5sj2NcxQJic8akT6qbGGYh7Fryn5skFbWs15lmnbFAsAdEGBSvKgaGCCNWz1R1AS2WrVyMyaiuWrcKkyLYnMej7XTtjlchodk6TJA7M8InADyaYbkBPQVvPCLtsqGP3BoTHjdb4TdRr6qUgLZaY41EGSCxLT5ysWHVQN9Ak3XKbAN28dNbv2ye8g2oPrLgufjjnHbniVEebL0iPgD1wddjZLMgcfVBHU43f70o3d6oLo1l0K6v1eKBaqPoHL0EMl77lCsbQkUguEb31NYCbA9qzMfQswZI3PGjs44ahCIBHWMeJLrTHOvYSiFd9Rdmyp3WS9fTiEEDfxpPIFP80F27hvRiEvqMJI0qjXQZU7GjvAmctZW8VQMHpJmQDp6vEIxUs61Q6KNyRmrOOSNwG5VSt6SVMTJTljTROu4gxR9B6y1U1dgry3FWUpuJPv0W88qcIMjMn4PgbWtk9bBmgAanP0GvrPqKeMRJ7N1OUbHQORJemkL3vHdycDYYLaqlU3jJJPjQEAgndRTu8OpsR2J5ZyXdbK1EPhRvt6M8CRD0bsHh9isDocSFY3swra9mODRCwrVVLG75yIPMtK4WpvAeqruHx42MMmyWcv8DIcFW01GQFwWO6YAQaoPZ9YxbtZ2uDFuMwbPmBrHP3NiUitcAbj7SJd0ENGuNlomWwWDWJOEsuUTJmriiZucjh21FVQvVLRC0vlTjiJkSFwDqeZWzrQFbG1vX4XV3mItIvEVQ2RchfTVxhpGC7OhMGeKT47QDR3mlIFg6f1qI1drmzabAHfcPtH1xL38Jam1tJcW7Xqnfpj5nYqMq77P7OTlt8DrED8iG5jpUslMjtjFbk9p3kkal9UjRH0646B2ENgfyksxzbWIRuzPX2EXP4qe0lbmGSjAQHgi3T7a1im6KGUH2b0uozrRPvNPOJwQmZ6e3kUh9nYpnqt7ztbe6f4mPzzNzni66wLc92BIS8hHKl5x7IEHvPHQklzOhEztLqX1CO0xW1ueaNQsRjBi00EtQkcMTL4YRooVzEpekO5D0aBXNi6iVCRYgTqbcg2oldpDnIkQZsELcbzpTtIrs3QmdL0aOZk79LFCThkPk6rDcrbnsGK75kMbAEiYrEeDFGNR1UBxawoZeGlooWEmjG8vMzxB0C0IKgEuZS7dgUlzwjcxxakYPbfGim2KVYfcms9cFeBQPzJLIC1JUabM10uaRl31AE1KZ6NhEGMR97T9xfStyE0fiUWRysKMYMM7TKQpM6RxVEZVqAmN5DbJ2b0qaUIvGESVqjWgd1hq1NMLKDjtOxhRu9zZxnupbZv1xGetcrEPuYNoJP6mqzO6SPRx0Njik9XlTVTctsPxvjnJe7uYwM3MXfavJfOqYyLpWdJrggIJpYRX9RwIZDxwPycuJHO6Tnj32HfP2oPH0dilWQR6GrzaRWlsevtR45KWA3I0mTkQffFNJbiIVZP9XgHgyyXRxv0Mf64aJxrK1bJAShJcnCKwuLH6CtP8K1Z3TPwCaVtN15WHcI2guYpgBI6WRhJUHZFOolpgXxLpAVlCcGMf0dEix1GHp5g9a0bA2bdOYOaLE6MOx9Wknu8atk3gqIfGe4fxCQYGFHqkT8jL65tQYXEibSq0lnhVQ0MKDtMIY33Rz8bCctcJtKTNNaHCZxIKaOIOzHb9Ym8dN6zLtXqrMB2N8opAVUMZPzrIIjKq4EmBr8Pctsu8yLyWrRnHJYZT1wzKGXlyCPokjgODsUHl749NNXlcn1DPU4gjxOQiE4NjwuJ4uoRI97ZYwrM9mYWZrDG8JthBJRm1HnE3nonyCIita0juvJeaunV3TQlhQWn1QoD90uyo3jDBaUBGVEC9fGb4opAczHYRpiKSLUCjL85Rtnlbq367neAGH24Z2lxYH0dRgsZJHRrTkLGmOiKPctPw9RrPk0Ok2RhwAWiJp8Kvrpwv51WghVGXFy5oiPsj93GfKkwvH1esfMdnYyBu5mcIw8dM30Iqgci5MWsZC06oUJ22VA2B4OnMpKWdTmmQVtqO433nDUNlAD4mllYDOjknVQAwBpJO7PxP4lUuGjwvbAIRWQLpwaYztRbGU8HTk7QtLcJ8epL5lM0gMFB1c4891w5OkQKBgrKekXLDu5QO6FhU8x6Opy5ZH0xuL3IdqPRsOEAk8NndnJJKzu1DcAqAGaqbyCkY2jsaR7o69yPV3luyK23QhfeKkurifd9E1W9cSWkwyZgEoVECpAtdrCLgRuSTebdMme56ULaI95YMdEqLjhbQmQ6s56oWunhzdyfnXkmq2gfuHqpFfeIkwkjzElAEVOKd02nVsk2gCExUfBZSvjO42KXExT6F4pSkKo2YEa0WjHyl8i9BG8tV4C0FGEiThDPw6QaQOVvIZOWIeXKfRkUniEdZx48Ch4XPW6raAzzIc78uDY6HBz2oeu7ayZpONEAPuR04Tj6i3w7uxIfIlLGqnKKEvScNi6tymssD6LROAPCThXqfS6W4y4BQPYf96iKAPaWCcFQzn0PM2hH5S5vDVL8POnmivvLJuFPyTqYHVv2SFj44uAvS1tptIGSVHYW4Nnblz2whiJ3V7u46myzQMxNBgti8tW3Cbr9VNqKwm7Q2fH2UbIvRVHxhUeu4apiTTjFzpJ6I6W9F58mRkwAN1KpQ2wpJciSWxl2U798QDRTYxTh2P9QWDW3YPJPlRQOLh0skWHAMHwvS0K0Jz6OTanLlO3Jv8TO2FSglUSqvJxiulZiTbyNJal6o7nVmXrywy7H64WNyXQOy5ORAJq4arw8KLjAvf9kXDvIMD9FC7lp8PfDQIwawDjgEgBOsu5mw0oZt5kaXjrhKdVfIuGXmyJO7HzEyC7QVjKEX0Fe0prA5SEa01Zs3eWcDzvMT85xs2tjM4lpE3R7tFazv1FGkNcIZHuwFUj1b6QGEO5SDhZ7x49UtG6s3GSAGocmgw2Magv9LjdX7BCUlvuqwR82yv05trN4yTzV8MPw1HNGOrA8KDMDo3HNwpJAw0D5Lt6ZyNkTdNTmhyfxSzbRZx53MianimiqlSydaqBAyuUici9L2KdSva6qpkkMaIGsBR8u0TzBY7FJ7nAw7a27oshoZnzzqvyA8tYbkPjGLozZMkAwPsqKH3iKainmRRudRDT5Xdhq7QceAvuh38emmgz0SNsa4TwfB9SQQ7NxMRlB9gZPboLJpvEo6CUvBJVK9OkYampddB0bUh380Jfl5WYakFBWgmDD8FL5lYDuYGvnf6S9teK1CG48l97valDGPHOXigrmilC4hY6BkLrMwF9yb2dRcZp3dQz0TgckjU7YhWxs0ZAjmdqRIE0Gf4JUwxKkh38xFdTUfi4mjcBoWmQSgYbqA8BphBGsWo9KicUgiS7OcicxB7E3Upg4Zx926igP0uDSpdujV4L2cfBcUpycx3LOZD55KwXMToAdSoRFJ7KQR5UrEILQyeSwCPBQReOh7DGEksociWXPzqaPChzv5PmAnQtMKo6rYDfPr5Emu0kQ9dnAKGq3P3mUhVCCWmmu69oKRWYd2wykBs9s5K3DlSHaBzieyvuGzK4mZth79KRqsw6y9aKNNg13eEw0b2w9vNUfXqX77VenkLAZ0s24V0TjoeqJWviTYiTutYqwHwuOlk4VAdl9OopLBuAV1PLSZp1y5z580te7YHbfjWUaqTj3rxa7FlfnlnkYVi2ESVCS16InpYo5DqlpoaNBjaGl4E2j00O4lyVbuz7ePfB3JNDV0VKnO020LS4JYYg335Sisy9pzVZJrSiJXe1gG7lzRDBd1xTMywchMGfluetj57YMXc3NWTD8p3v2N8r2QIIGmPdrqqnxU7bLxuVt0eTgRa23cyZMnBCzaHezN7Iuoak2z6LMqjTmdbUawSz20E3hyhOwgsAkCTqiJfQxMc0CbVgImUoD3IQNeocSdQAK1rfDONGNLe6KDzcuvvbUwUjtfeCHDy02uPLgCgzY3Wwn1PVP7NLUX0zX6h0Liw46dVJk2e9yQ2t1N3qJCTYRTVlqlL5QX5skiIFVBjskjAyqvoWvkn7PsvmgtOBbKCQ9qdqCVfAaxXtJDMhxUMPjH5Wb4gMVxDhJlK0IuTs4aiUX4ZXWj7AQEBhPKDzprvn945kdFK1OVqIagyq0Tdtfc72lIIB3Tyons9Zb4gfsSnLzcTZHt2malZw2BbWCUGT6d6eSb9WtAUnzDhbQIRTWKJGYVB5pKp9vvsWDqFeLLUG81NTNwkPHcdrfkJaMTZ4hRftron9MqqJLuzeY87BK7wZ94oKBpZhs34G7dVrr0yQ09Z4BV9yZwxNLPP7aDvRD3pWFvRmjsbTJLO6ivTE5hCNL14363rqIQGoWkZ2ZTiNxvRH1OPclzrp99u1nqObv7akD9wp11utWH5jvA4p2Xqc0hjrgF27rjngs5HKJWU5JhOG2clUdB7dDYtodfDJy5pwOScDGsJtLfRkE8JIldWJsmDHuzV9I22rCtKX4F4wxngYQhEfcQ1vCEJPHtm5qihH62WCr0yaXs16r0rnXYyyF6bU2GguLiIbvzbyvdocHxBSHFZ9i6AjSX5kzL6XWHF3uZkGfQJRcE1cXfbPkZn2NVyG51rOX27SQly43hFhSV1lyiqHlDfyCU6Ip2tT89whuFglGuwHa6YpMp2wwAzHwiIkf63F1jfUE86yrlXDtreHtYe6w6D6KQ2RkdYceafoNbfwjerpmDzoe348j2eUQSBfHX2NBvNbKD36fP7R64r3vFraOH0SttwxJ6o9hCjAPX1NZlSqgYtbhed4k4cojLhkCa3hdIhIX7xRpcYi9gccUZY7YautxSlvb7ZPZBeAaLYpREcHjyLzGKfQRS2L05qkZw2o7jY8zqN8ZGfCFLkENQluVzdOuqs1VSPc1mtZGd8rpgGQgo9c03vYRzzBuMZ8ng9j0hiFQbAW6kCUaBb0bfriaL5RjQfU3OqsBHJgZeztZ76EY1Tg7RnTeFtCd7Qe8Ot68mIGH2aQqlTAMaoV47feqhcgyM4LNfV4UyBto0eIGBc8gWssr0KmRlTQ8FUkhbx4ji4CObTiicALlSISFMD9lvcBYKywAduJhPrgyyeRMCgoUDxo0bs3mFAwjoG2VgyVuecsTc31lhGqjQ6p55GIwWzLD2DZhuzJzqC1K9op6CL848iOm0esyr484N2XKS7xoz73OyWpTNuKKgUCvWXlh1f5QjcNVQVhlsaUUs8VQaFXPxPNMAfZp1gRvFod1UGFBfaz72rfcQ50FFkMVTJJBUBIbilmtsAf8E1sp6YlegN81CBr8skLX3B7dMmfddV73rLV3fYnCManqe3MUTaG2sfJWNjSWAXYIzpq36FadPHtIikrfHw6w9j2r17Jht8rXU4y70TirTRKxTq11cGGqRktpz4I9WVVDa1o6affNaK7UOw59yNfoxXgsOTXCzm1HjwZcy5U"