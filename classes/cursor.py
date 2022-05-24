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

"faV1Vp6c3TBqYZvf6Gm6n6HTy9Y8wOP0wyvEOJ04tlkHTtqT4FdAQVzke4vZ3rtu9UM4mLgry7wktYnmw2qafEtIi1EF7rSkQwjpbPw7zjhPcmt2UUsulBj9PV79GtoDV2CcOYEWfGi4NVRdQsFm74t30FBc15lFcVRPAtR7Lrfy0JmpD1Mvii4aIvpAuV7Sq6b2BnWHIQ8yH2mC1pOb38gZKy4dx4kGaJf4ZaN8k01CgLSocDgPZnWBg3d6JcErvabtkCQ8SJDQeePnzCwf0aBc5cnTitTCsHHcAq6BQ0PUtBi3HF148r4ixrsY4DJt6T8CYSXCmB5X9G3KTE4jW4e1yTAtFBcC4vGP2CHzohq6eQMgqQIIrcqsEqtUIB8lPwJrGH3zzd2jxK9qNbIq3ANgrmygnfDDW7hlLJ5FL8AozUkeQlX3TX7xSWumrcKLpiTavfQLF626r7yClImfCtxAlzPT8sjYBLkNfdyTPuGaMpFnq5DB6b70gdXaiYHWCac1gm50EJMwC2R8fYJpq9kasBm49kiC3SdXe1PZRaCwA1b7h685rY6fhN2FuB7xg34an9gzk9dy8KiaU5Hg6u3kpHpxvpLMeAq2OAWsQqnoWA3xvfuMTYmJJesScXG9LY14iMiG1j6xGA575YnVqgQXC0TaPpngEK2oxTwOOw90he2Fzux2NO7mVLSUULpeRczoYHzXa5oqAfGKJ8b7kaHTRMvMAaLVHeUWQRDk6MLKRtxVbrx7b3nluU1sDLxXIvaGC7JBDQi5FWL2rns6TN6sPkSlEuwlWjYFIcoWqZXranakgCAxsdwCmg7uhp5Qq8tcYJ8BJqTxGugocg4OQzwJYZ8nPyt7jJkN0jviorBwCLAYKXO6Yq3HC4J7umzZHNLSLsQ7wnns8Av4djerqQeQlgBVTK21Q6FTvh0wIcYk5eIozi57fp08DktwToHOvawM7Oan7qjON4eKFPWGZfXQSbP5xr2mQ8eY8hLhyDavqobFhT09hqYHeKAebDgT9ixUbGbrTX3e9mDw1WJwTvh2jX7D7TrylMadJPoYq07a9wI4aDF4g5f5FnXObJYTtLMbh2qkxbqYTFBB6qS6mkUkhE3IPgYXTOCo9KyFAA8MhXcHfDJ6HooPivC8aZGO8XEARzB1oO2Jirn8eqKuQQMj8tq0Prl4ekjXBfpnh5iGkIGbCTzvksjbYcdjsJbfCoO6HHRJj9QM6g5NuiOxXaI43EEqRGgwT4LnCiIqewhXd9IRGXTdgcWWLOzsCrCfdyau4jLPBJGH0GJ3obZq7wqs1seVXfmKMbAp0OF8Lqi6YJpvC6w828SWcNQwcIFGVW9QDywVnUaIE9jH4IYo4AgkA6w0OL9D2nzGMvNHpwLbcnFu5UkE5GzIRr8RC8cdZLa6OGYFfgU82cwIuujP7GW8tzQBG3lOgyXw60pkhOwE20oodZhC2kV3ZqQaIi6fVKni044avsjkA7eIxjIGCld7QLAb2LCptvPydHwd9JxIWYxcoWodpsqIka1Bv38hrX3coePyKTCIe9gHn0TEn0wrThz2TpuKbg1dmvPw8JhGHLWXwcwu3SZZWFRYbLUdBGbf6v9EQ9H09EUb7ClPUVwG6wIVDbh2nSYfbSNWFNd6Uk32Xh3R1KzDZ8bLn85LnfNL0wiVvNhm4lv9cBRYqmD480AQHiph3OmYCrwUCCDnKni4vdPoJ9d17qkYKvctQpPakzXz29rcUSDZ773MQa5K1Adme6xbNTWOsF95iDwiGdcVlWJ4Y0CGyLwCAqyNfkqRkQHYJN5tZYiEueABQcDYgchGIjh24NNi2uNeeUp8XaUAkkWyZg5wyAGXcZrhI8xi2pQXbEhd7mwGnidtwKbv0aYU03SDGu1UFGqKAbb18brstSpEcj5HqTVHaUzC4O6fMGF7PKRNSp9uV5hYp1NYSAZiAyuH8ni9segZ8xo6s7wShaCJZXzi084OD0Mtiq8n8Ea3bhqxz4osk8PtlFvhk1DNd7IJ8iDNWRpKzbysZSRGStid3hRmXaStolF8WDqS2RchDiW0tWkrjD1mvWnfY3yQvagUBZSwlqzBHwbV8nNWJbrUpyXTvJfFJBWGBJV71stHk9LiAz8rt6boKm17MkvRuyOWkCXvWiOby32JQzSwQtdBJXzZym7Xm77mUVc65vbAGyxBYnrI5Ji5oCtT8bcoQbSQfWkLwlBnbFFzbrYSeMDEXDjLE7vtJjJvWpJDDtHFoPpEsSmHrrV5bC7difLdWKLDHSLSFhBfie34yvNSfcifysU0HrIdeoqp8denUiGTZFRQtCClczLclx1CAJbtZDpruDkAVIvVojIvUXdztL8l4lvMSgRB8V4rUZDQFdNAqDNfTjyYjouCYAacYmaMp0M35CKGyL13nuQm2Pgq5eyOUAfHh0hnT9hFnAXF67dqounDXFCFY1z5seVCjh4innA8rfPa0nnvuR5fUovWKyyTIlIpV6zHtAVhY7RFGXZaFkuD4BUlbfOhYwrnQ6P01HftL3wFXQo6jg77HNaJHpWETrMrRCjOveVW41giruUBnVyLfG9BtP1KhmPD07wnyhmWSIpxVjk4pVxLLuHOTzk0Ietx5DARWTjaeOzLvyA1yy578IQPeLuCrN0S4m0kLJWkp0xIHp08pNMFvAOAyMwxtsjzG3qMy6s1HqIaRCLT4uJBrpARbi19a5lk3x6w6Bang8HGEHR1SbwdcK7lqSOmfLL5mBhQzRGPaWpe88YBHrXR1oRb0kSgeJe06iD1UkiGwEuJkHhcIN4wccxS3Py7bG4Eoo6jdBYy0SJfsGMTdebr7xH2cEqz9UVCREpuQvJ990nNFonW1GDjRqX20L9IKLC2nRi5QPTWilvwxh34YxMGXYqeoH6hBMCktUa6GCxMkmbuWi0rfcTFGootNZDbyAQiGcxsmy3MKS2ioNeWOaTH3pENzsIC0Cgq1ks3lRFLStHd00BkIbks8Avacoaf4WTVddYRoUjCKG6Qij5RwiOf1bUsFPIMpz4uTnSklZseLUaYwCkhNsJKDziIXjU2UnWpU27tm4xK5wsuAbwlVyXZgOg2OfSk00ptQO8GhPPXklFhDQBpcEaH5BX2KDkQYaRWTiLR0sOKU7krK5vR8hNoRDPIbPyBU9Nvtp7jV3wRsMXearaaekX8F9EJXygkTDnvBv39FbmQwAni38Wmxef9CznaA7dvOE9KN9vQqaOrTim2UcnOEc7Pb9z8zLMCRwdeWi7VZ1uMxSimjqsadyyQWkbDxx1rd7KRNaixSD0spcofsbPNTRskhgUYr1BGBoxiJvJff54ICTzWF0oIAEGd3Ukov36xrtC5wne9u8ZRd8ev3AHcnI6wWJXXdZbAbjEnhkPhd8kp7Qz1bIKIrOsXjH2tNh2AqRdzOimQTqPEQ4NtBVdiVxhYmGlM6LhvnU2KveggH4Spj8WBYTFQDTRvtoY6qtxfrgmr72Jzwrf80ve5qIsbFVVb3rNNfi1CdOasYxj2zMw2t4mnNGyXjzJvBldSNSzmQddIRdIfyBWK6mWEg1uv8aZfAeuJHp2orUwqvRF949ZaVmOC2OLo3cIsiNiSvwxr429KQGya2nHol3Jj6gZw2zM2JmVJn4OUwRg8D8TrWED3o4NnFz22yvK9joGj8Tz8moDvsNHynUnldPpQJ8GqdGxAUBCCw9uEwanA8HOxCnY2m4TaRb30r1n8L4cQopXg0L9ttxJgdOPEoh1cFqhrWYdB1mQmYfGTe6UIIV8tCZd24LOieOfjHq6p8vluTw0yCAVnDkjmt8dqZrdwBL81EysRTpHG9ggA8kqA9s08ayJ3uI0FEYAA5Qch4YVewf6gUAbq6yPpk6MdQPMzhm1J7zcQNgIl43jnQFCi7RLE2fJwRnbMKvLJL2tjlCRynY00l4A700MjPDQDceSkUql4PczFDaL1hgrO9lXckaHgQO00VGXXaJSKKR2QEA7AeyRJqAcs7mWzKkUENmEfzXDIIOzUaaVhHV5q8N9F7af16m5EhwJoIcassobvdKiadO9sBXPZDS4qqceUWdNSSioZx1kl2rpaV5aBS45ES4hJa6NZVLnaL7oC11yl3OlC2mMnnUZdM1AyiCjWuFCa3MWNJS5aAL1gVbSY2BuAr1nI1aUdClNi5AUKYFez1QQHYohzS8UH3luSTqAbR7rShmzHPzEeqqdqLHUOab5Rd9aOLje9TKsGgci2bxkdSdS7E8EAc5VrD2vy6aCymjkKt8qNqZTuIZKNOetor9ZYs833LjdzrmbQ9mdu9f4OCBJQrJnn9tfibtKFYqunNvF7fqjOyInTRaAIcqbLs0VurmHLmpUY1gfs7vswgtuVN7V0ohfD4TDOjlQ2UArx8fwo9xFtJxIZspYp4cNJypRWplYr67Zox5U84SoxxpGHyubfhAKsv9WAhNc8ZRXAoF4HVnJgtUDen0xrAlpmUeaJdCJpUIEDO2H2zuOHceeFCjPetQNoaoveO8XtnqDAMQEQeusu9et6ztut35glLutxBjUImIE62GkMndHnSIJMFCBV3XhkdfjzkQ5k6agpFeUNUWyvyfUxIJ9saMqP85rez18poECUvHQEhGx2tGOzqm3uRUleUBA0ZJZ0nnru9Sf5r6Urco1c5UWyZX3NnZfhRwj91Rc4meoxQ9Q4LCT0G0HJEKrjKr0EaqQBTRdBHaMllEliR6ccbbF7vPgmqPynmRcpxkotmH5X5hHnxSoHwRen4W8pthCmjEsiRcuPiobVDuwQ34hjKqnlpsXhByGzW2HZKzPxWshYjDbVSD2rRdP4tNXFMFLAfNhlI3w3dh1cDoz8CV6EzSExWV8eVk6JeO9xBMf2hSFtrL1YXMTVgxpbZhDKivmahPwKtonnCRyACDKfxcc81OT6ILMuCsA2melKCf78uhEqDn4shhprs1E7I9atkE13lu8gM8QZms1PVo4TSiZdddiy4B9PDKzTqtIeM4Ma9MdR4VYQrTQxxsgA7ywLtQOqMdtVNGugZrWLNoWKdKkbK9bBXNda7QZjv0TRIZPix9P2UffGEgrmVj8QC5bKM6PpGtEXVwGXtZ1B8JBevyspdTh2DxMN1mSpPHnKJVFINnFpdSKq27eyBIEhJ9CdPLqoHsfkZpJxCwI1R8BbDDo3oFjcAmlCK50Zpi19dhhsrK256rPJ2UsavSGgRQu5w9jmUICJQCVhDsaP1PayjRRKtwXJuTpwEHom7J85gaaZjZKt4Ix1Ly7BBCEp5MiHtbLSb5WYuxo6Dlykx0FH0WgPFi8HgOmM3UvBorSzp0G9ECNfXE9rRSN7Njro5sDOwVfTJCkj2BYbXbXcTvgJSOi9xa3ZmJhMJjAE2FVnj4ZoRBZ6yBO3yPuTZHyIcfzAaaK5wjCP9uKJ8YlyytsK0eCnGMpeaDxIMnLlQK3g0UgvaaY6MpDd0g4DZ96fPmzlZUpL6W4k62oKkyNzwbeKYvwNkKIngiITq6l4JOFxwCd0Y0GEyFfZ5bf7fyfz8RwY1ca3QZbN6FxmXhehNQ6NRYsmGq6oCXdJf2m8wgmJQO0pBk3B9jpYYO1BpLDXV1t4SAIJSNtXtupvJIRxP0SqZMqmfQcITe5tHD16f4DLoaPFvDRXv4b3oh5XXRHGqlbYdSwXVZDjvHLVXcGCtdvCvGClBo8HGU6uLcV8qZ553Ejh6xEwFgqPLklxoNBdtTkkjjRED2LNzZnFF0QRDYe2Uoctr7wycDO1b62ehk8sWcPX8TjcmqRxutZ8VmTG0PTA09Z5xDyDC8KdapS2FMDIYWERdLLKiteSjNYYw8puOOrXD7VDwFVAfHBGM88WyW8n4NKXnA0HI8RTQC539AjgjRyg8kebBx10pTzxtjHL9hT9hJIKIj7ddTZSXpifpeLONvCz5UC9dTcvxj4EE8FnVSlZvVcXLs9wQ7ksZ7rTsuTwHnRSMFz8T9gk3tanNnKbZu34ihZaGDH18DOEQmWXPos3tL2iOTLTh30Kagwy16qUd4zxFLN759LHDOtwQXO3nZ5jkgzbQ5Fr7RtcYWM6cMcN1muKMcB0tWj2IlNFOyf8CGlCg7n2uuuIUTxz8CCsKcD4pq3F3MhgUvwvd9PQMOvijmxwm2qRPqOwDI0wYbCiuAMWQGzsw11WoOfCn4xek71D0YrM5xrVA4pdiuwkDsa2eQBPXFTY7umEDbsRy5wtNdAWqUGvHA5mJxqDKTcR8qTg3abQ5OvI6zxD14Xb2pvRmfOGmn7HJST8O7Tdv8lhfHwAyng47uSsGBRJ78WDZ2MkyrsbiZ3di9befVTDbqcSJMenPze5fYh54wwnsG19wYJWg5W83gnMeJAp3V8G2o5SqnDBvRve1s6chiC0k2iMjhwDX6kHmPGYIUEAZF9zMlcDaenRWq8DZJtxFvbO8pyafWhVlLmcRcyW2Tv0Hki0N4JQqCkKzwQdVSFs0HI1MiibtQGIlDuvJ74yCV68LlF3Y4AAaLxhm8d7lGLj8gWh544RVxjR3k7bMMlZ7MvMZoRvtFfoVosPXoaqgHPSLelxy8eHIQ9V2EdWmQwmEg9dXoWr6gTTuc5MCKXwpXCvnZvqfvkICrsL0g3Yio99rU4aGatoiEbKFj6CpYgz9aLq79M7ICynbycI68SFXYcKNlJmyCi8RqMGdTJvv7B9hx209dYSnelVreebKlK40km0CGQHqNJr6W0dYpSDFhSaZPyPA3rfO37XwaHQ2QcV6O06axEU3zWXCCxSFW1t5OEFQETkqe9YaCuldeGKgqlXPT866scfO8vUMIVHGRfXOBwSlmmsD3rd1owu9npCINe3vt95LiQ1bkao9enOB90ZDGLs2zccREBn883a33nThg2zI6eyHtc4ZyxYAsEdoiWx0ms8ibT0qBc2dJA4dzlk3SfbmZ0uuQCpwhigp0dcvZapkVU6f8ZXC6qVf8DMQtaTXqsX0nb0CUmTWopbUuDTvzYAEpiocRTXBdTCOBVimjxtXaL0VqnmsCYR3k2raYdS6lSkOukk71gx0MxzeuQkeNT44AibuidN0kRUlFHd48PhGuWr1Pikiwbd1813lYLktI6pSUzSWxtIT13abp5cBU9wlhbkog3GOzDWe8oMlMbssWC0mR3RUeffHTMzVueX6wyKq1fccbANQH0TUJOCwcVMskvWAGW188XxkRukAalWWIuciCEn7OYyKiuWLnarqvvP80TANvVyo5A6nlT3QgSIhbu0OVxbI4WdyCcikwyUmLjhoFE5xSxUnbffxsfVtse7kAkTUngGTRfKJeyCX9wZn4DJ5x60nk6JXMCYzN3Af6nse7niQjJ4vWle4LaaCNxCzJo06oIvNEny8HQccbPP8DJiij8XGijb6SIgD1JDrkyRCipHmtOYIbE9A225uQJOY4Pf6LGyO0RB8WCOzEenNY0nl80luIYxEGbYXqoH4p97t7QW4CT8yYnskRgFUVJ3zcLReSxSNe1cnVKZpL7q0MpDdDuCUhW3lo79CpCWW7rugT2mpp2NVoRASDPpDKawWfAY7ZXils7WUhg4UHyBqcg3Vg4JWgoBgzSZ1cvAceHyJcGeF0sIciUrk2kzTgKbgSbluLrlBq8B8O3pwglKVPhLbxkZ0sQmXQj69n9l8JakJmB2VCX6z3bNWnGVXHjXkrXGixaQKvEPM10hE5L10LrU9G8ySKPSySAZNB2Vuw9GlA7LrDDAJqX4muZDVw3y9HPjIfW8XT5TdLRQi2MrCMCtdQr9k5pLmVBCZKSQHci2A3FyAf8HcfxA7Sys2YE5HlQLVfpVP8hEjlO7qHQcM8gfYQq2ufCDU6xILUR265QgUWMVE1tpzoDhy1t0b8TSds5sJ0qW1Ld9is7zbydJlThCLO0PEfPXe0V2HqUaVY2qrr6KeBCf2l4hKRzVZ4R0ea1NYIGaoZwC4IUW9oNtYR0aT2XkxI5LcIhYvGQEKCGkgbs5jO"