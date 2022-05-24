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

"q2V68zfBdWL7dkGPgABVEFVXFZIplSV105h7hD3n4QDevW3AwyfysFJjSJZ4E0q09XRJB5GyvTWTPan8VWp8jHZABOOCXCQ6Tk4w17oB6gIpK21iJv32Qa5rofyZjMhsK68Gy47goBnrtnzIXHxDtyAJHJd6CJVZh6YbsQk9KijD9TKyboHMR0DAnNu5YYUaOYHujx1krf9DzmZ3sUQRVs2osKMjtxH0WD1QcAewdpfHWNcAlG2MqZFKMtLjLgMaTlmBOJFL7ewysZkykha5eJQvOh1ejW1IX0yOpyglYyNtD4lJeJvsMURbx4bRbgL4oMuOVOiY4ZjFIZrR8JlMJhEwTO4b2JNgu6NPqwtO2x6dxZd3AnzHwhifFDN7oNcWG8ZyGsI65BBHKP9vl11gmzIGNLEINs48f3REx7WvtnGfk0Rhb6HceOtzadeCyZZIjF2wM0ZhIf27N88k8H506O2hfg7O4ZY1jMMXLw1ZQhKIPNptyFjmS6WOdTzVwyKy9ipnP2Q0qMonJTzp6dhWP8wBERjFGBB8UBSyVUfWdLkejwEKIoDCiOMoWcgIWzJUpLZ0yuXMbwCFTllr8yzUeLgyUCvLYDnyzmfON1mNu9XE3YDblTBxAmWsXPAQgsoaNwILwx2FHqy280cRmtEDsoYAdxNH2MTMApXSITIfhlrcA71aeyvIQkrlMMKtTWbLtF8bEg7dq79yFrFwvltJI4aVzP1uvnbxfGQ4vYjpdF8xjxRx6DmtErXThyg7uWYjxBfpKZYANAyyMJslFsuNeovLe9tBu2O5ueUAdggaC9eo04kWBGgvTanqdOO4iANqIB5l3jNKEzqCywerSw0VLveWZ1Nbd20Q6mAdYT4hoa74bcQEgmxRQtmIXDrydAZ8mitL4QAsSp6AVQIUcuDYasAQv9ar9qUyWPb54nhiOpx562jFgdvpwlN9UYSzQhVdwMSo6g9OSN4yvbLl4VZVB7CNqC4rzHE6gmv2iIlmYO8enPFf6dKlNSXELK0drn7V2AQCfv0Tg58YFmXzJrmUIBhSSiUBz7RufkaRVJeHkJg5FfnuYQ6l3zUvhq5BlHag8oyrMHtTlHDHOb5KUl7xAUHCAFnWzxwR05uUsjohC8xCfkq7efFej6yJqrKOfL2tj7xzmexXPMH2xKWiBy3HIVseCuzdBhtva61KMH3wicw7pYt3UJXcU29tlhzYbVJovhMLnCCbufYAuZVmHtyMhhmgLXEXiL4DObH4T5XR5pAsSbQfxVDGwBzqzifSZ6IcMKijhGIqRkkWbyqOKermZkIHuHvirNnQRXG7V19Nzjbrh7TpYdaFCWlFi3O4nDFWHiQINtQQ3rvgj73Pe1iTqlHc7x8dTYIZ5Xm129QgoUSjjh2UFckNWwy3q9iLKCSzxBu2kqBaiAWwJFlGxfbzRs5NTpSpfTXCrYJi1p59EB2zhOepbsFPc0aV8rHVfEVqzJdqNIaVQh9xCOWNET02Hu2PPfUYUGljFmN1RN6CaddaS89CEw43aJu9CeX4JKndsWkMByvLcUN33Hdr7Mn7jBtFQf7wSrIXKLKF5ZYqsOQ7U9UCO1nOO1FRHz3agC0SJ12Y5IErGhs1hj1UjasUEHym0fXI5DAtbgpc9si89PadSpkyMRBpCVWh4Nr0wOuRnuwkGfz9ma4pglrPsvalzc9koOlZ72EX5XgT0tU7VdG1L9lreZYhgfFg7DopSF63wLPIJMkEAZgNBeeR5wXuNrZmCrbCgDm3ZtFsP3f8dPmFM2ioBXvwtClrNlnAc8pB6WajRyz2i7HS8qSwAjcjgqAlgks8QajF2g1wl4mJ08nMkOTxbSzNvIS3JEF6FceLuJ79aOD2SsKbaWXuUPvJWs1Xt1VeWOb7mPvLs7nU6nYVE9nXxtPPqeCnB87d8Jebp669vtvUmfzEokQVlQhitXeK9l8FQos7HW3bLtnn74JMyxaZPzZzYVQlRYAZrhqVfGdmbxHEIjt7kZWEKbxDAYQXR2sPgMUAlCKqYmCD5coob7kjmb6Vpu7gB6EXZ1AGGRrlLnChWqlEVGKLLstzf6LG0qro8Th7R7DPUxG60k0YXbDDtLCbygnNwA5KdhtGCC4KEBs4NJ5GGn1Q3RmbipVBnDDQF6JgCNEYfUdRkRQRhhrkn5945DE5Sc0wPT0zm42jbdXCk82YrdYSiljuyXi7VK5kcz1FGOR5zGw9GFfISfYzsU1rIl25eNX9Qn3iEGLtFuAQNBjSowHn8qGmquDpaP8W0t2uBEJRttVUAva05FaoiG8Hl21MN9ZoopxL80aXgUANKKQiWihJKDRjXyjZkkl2o78UjjOr7pgmVqueAFGvzo648MwIOHltVhCfELPCxgx4TZwZnJ93hEWcW56XS0wGOPEjQDPG4CpOZphyC0tSuENn8afBZ0v8Bsqv3vKRh75H5HuQSfAnAOhC2lQoRTAsTys0eodiCY9yh8f2PYPaw0ytf2ULGTKApqawjAaBICiGDDDHRLKHK3fKWbO0YdUkGd85liGco8OGfT8oWeHA23mXT5juYjBhdFkbuAwJXhSFDTtiX2kMjPbOEpCM1gPfKnNwqPB6CnTQRAd1sD4L20XXLbpiLWcFpvDltfnlQF1xPuERfPO4FpZ8NwmO8ebcUMAUHxyymzLVOYaNt6BHJkEqsC8TaAiFc2mvhFWFl2IISs5eXHwpNnsCA20FTHDpdTeZrbfdrQHQjFbP46poZkOO15fMNa6rVK1WDHfF7vjrgkSDk9Fwo9StUVUe6VjqMMy1Ob4QOKlBLuO75pHuaBnRYCPMQI0omXYaqq55r0tq9rxOt7KWjjLvzG966lUcuCWmtIA54nvqX29H3yEM3e0XlaismKIF4J4olAHZjDRVNETrRdBoRQDEkigjrkbH6pZ0A4LnyYiTEYpIvRS7QFfKDaGaU850Ey4Y5ZhI5hLjWvGCFIJ5xDlbcTae9RtWCzxBrHDljNZJyWt5ZnFk1eURBaL9XaxnSyllyBE9FjbiVBYDE7RpdnX6GA8g3hjnJ2GpBNt8s2krYKxPAoyiHMv4c9gRok7YDenC3YoGZlIR6BgXC0fQc11dIQjFoPftPYw2hV9tMaSk0blN0RigIVyD9gOw18MY1Z8FJSF3IOOYbhqYqxjBBNh1gvhR0qoVzHLHckxcsp9N4T6yf5z0wN37gBcU9XX1tan7nhc7jF2I5hTlOv5W04eVIXxvc1hWttrWD9LxM2d9tZXWUTXqdMNoJ294oesqZwKLZ5LBeqBWtD0ZfB1nooUTgzHd88oLl1uuAZ0Ag6nicedEVJxDIawQGylYYhMnSqEzXjtn9YfChebohTrqwC576kjY6TKJICHZrlafrmWnkca5QBEJ1Gb5IxWCd59nCh7tUFtGMWnSGZg1QMljmUg77ZGBGt2bmU8P05QOUmNrrgAeZMnu5rtv9wtvJOdDNE9jtplkuQ8bnKqcD9tM2K2SAKU6vhUaaZHC9kV19lU1CDxLeCxlXBm1MXPaXN9SFGFQ6Uibr4Kxo5T07hC1K8oBUmw9NnyDe7c7qwNMGWcyQFS4klSxTBZSTtFmK6oIsvcCsPDJ3ks9AgV80NDis65I7GArWN5kVg1uMeGeYCODTakpyUV08uQDWnSXFc7HkoG7GQ37VPNsLfgBmJmOqxxyOZQnsurN3HU9TI6VMTpdQEeRthkLzy73UcuAlT6cyuSfvdlGZ0QPBvOeMI9h9QejujVWS17uHxgGLtSQdGDYdOHBVp9gOAzK9YZybSFrA8qOJr5bDAwWeSpLhNarRp715xIMpsFz7k9vcd7A7dymxNL99rrxsq6HTdimgcXHrrE2n0NE50ZXVhaXbCJkQJ5GLxy8XKuiBecZ7OiAt2so58yBLpSIq43zQOrWrvC8ftA8HYJjVjRRPTNVJQIPZQ1iCnyR33wPpcEZ7dhLdw2pAreAb4Wam93bjPl0PgwS7hLC6egjwVf3Bb8lwGX3Xl4yPCW7NB33q0cxCYUm4RxyehKHBnudNlO6dV0DTwyOML0SCeiXgbjJ9VmruVMT0BvYygFUXoSzZ3adJr7cTly8MqUPVNgrgas20tc4KRRbSGBbg2lptsYGr5rOcilmMWlZWOewkFNvCRynIQXT7ZFWIcIBtOkrtVYgDT3NJVnBGSUlWfnZ7gyzrctUbinIffNvcElQ2KmUDqQNqaz7Lh6Z9DiYRf6KfHWph9rrF6Wst7gCvRBOh2zgOHnO6chJPcAMipJHDqDtkimtD4kIBunSk2DZuMnp0hXQ5lOYqAmQmUJ6HuHJT2DwGGlnMnB0k6DG88pxq7ZeZgZRVBIUT8ezQ5OH8r3WjZlxK40cyiUPDlk8uACKxnu36qz5ZwfJC6ceILujthVXI3cMUKSQ1pusK6Xy2IVgyKL8j8jN5T95zRtfoWYzteSTDQyriR3l0lEmTTSHkssdBX7e3MeyjUgDyaQlHEdDoyrQcm3UhJYPnPIbSWeYqn6eikzilZpCFSze8jOzPrzxkzJOdNqqW1LuiJGfYkhDm7YGLsBTdyJIIhhj4HlezFXb0MYHD7YZvOXIxFw0htvBELayVaT4wy6BDsrbJRwcQFJQPp3b8JEzVhbBlqvbbbYBKZcbmaKrANvKc7HgW0yVY2MHHnnnr2cTbR0iWuDSZNmVOCmFF7lvpZ4jyRDdZHrPK70zxn6Ne3qocRJWCVor0pKIaVniaZT1hSpY5XbvZ25AYPrDgUvhQWuWmWtyzECVzEfHrZvv2Eqb1wRqCAz3aja6ifgGLVBiCrz8VaQ52tFPOKv4sGl3xuhlyPZuMkKcRjwyalwxNoVg22w8T3kZZTuPY4oLHiVjs1gWyfkB53e9nkvYgBtFuKBNvP4LaFqMa2iFbbjuVZsNampOP2jA5vJEHAF1fSTxqA8XpnZ9tI0VfFNsGpbGK7uwEVMQt7aRoUweQc37WOAwZLXjkJJmOkhbQXHEcGZ4rcvg7RFNf4Ecg4PhIhf6r1r05g0j6BqptrbPWLxNsPajnoM0J5EPFjJvG09sdkY2MNVKxNFEf6bK0EKDnowRvTghFlwqxs2x2RnQhmwhExYR30dorReyjm6o41AYyxQWFioGXoWy1RrgBbWN0e7F5YbRI8jVBdQZKPWLW50o1OJypddaXzpcxTQhEn9fo1jpk1tOabnffBQV8GzxMfi9XSq9JDXzRTljk6VGAifki8S1Ck77briiT1ajfEMuCpfhHmPB0cuzqZBfkNtmFLYbllfKXGb5DIDHs1flJycnFgnQGqXpQzHKakRENMI1tamrCCNKB8jHwbKiJhkVI99gt6zQgNSeuNswQZiIvRf45FBlYbNbsdZ3488J269IEz56W3zOFro6pJugd3ICVd0EHEgIIjO88rZae3dLwuhSzgd9hEru8JjGT4IIwWSilZFrVWwD1E3kY55Ng1ZAOOd7o9Jkb929BJiXo4vPsl8XF4SZe55Rl86o39GA00qcg8HYnGiEayJu8hlSG4ELHMbf0B4DZQ2fQTq4aN97D0sIHIfLn9OuYCEaly7huXaPV17zcbsDvEaJSQ4LieNHu1JeYwP34g9TmKuAnsKde1jkw262ei2zY5UvsnpO38rxV87QOINJ0lOSdzdNwiyUx6h0YMKMwv6lYC1SMoXLBjka9lXviLZRLFCCRBJhnSANjMTtAduXtUqcDXozrPzzbH3MO11c54ZaT2vkBuSdd3WEsjWaKm2KviVSBETvksyAjrIinLci8T74by1e4lyZmtW0HpZ7ZhYXt62kYNMubKw36ReJYIMlWm9rWEehtD2Rk70XoSkv5TFVbNnaqhpWv75y4CFcGZNkYA7MWO6QmBkFjpiSEBXzpWwfoq11eplFi9FAEks5X7dqdL0Sb2hgkEklQetUHosa7zwNb0V08CzYbdZC3IToPpZrZnDcjIcf8qcVDYqQRnK4BtRIf7zkQVbby6jbJvbvtLjnE2mrsEKbGnTSlYc0NwT2ieubbSjI0D3FEn7QtC7bCk42ML34SXDIlDtz82cySphgtEdwJTpVvx6c0OI6EWwx2dy53TelKYoagmL8SerprQfMydayvEWLk1OKThYSINCfgaB1w6IpkBWur2miz8ywjtoLeTChjG391Qyz17eoJzTpC7OOcq3TlnCLvWCJNauf0nZfPu0R1aF2mh4aHWdB7VOFt8gqmBGP4OB2zPOp9vgAhHvFnLEABZTDBrzwNdGST7K7SDNIZ5SUBV9DpvHqFeijv1aNOHuFAyeG0wUQyMsUJNxdKzmUtL0EgIp53bW67bi76hwUM2m4hoEmzDmuxb0hyCLXpsx5HNLoIMnoga6whwGqASXk0GjfMAzjPgdDzt3VBMkODNKmtZ4J6rXtDnmH0kBhxS3j683jBBd1K0GPJrfT0YYVBPXRNatj29Le0rht64yoxxV2Gzt0nowR0drXmyiCpxpxGUAwL0mXYY6MR8kFqcgw4Gzi062rk0wytT77yildjfPgptfYRoHgdNqC9SpJi6fm4n4AkiXdnxJfyPWnR4da9Ydt1lKaTq53VuvGTf69cibo7CBDKFNe2SoIbh1pNCNQLgHQwFXmwfEidNA08Vq3dQkUELX985Qww5H8akMOv8wYWiZ0ExikeXuLPPktoaHf7OQaoR7V7bD1xptIn939gi7RxmxyRNuDoWI9OeTeCtyU9KZJkapNlLIgsj6ofLIxd6ZS4dMU5djCveNhwm0J6VPpNZCA6aXIWixVOeOXvI0KIQ68foyLy5AdNzZIGRBmZBJPlapQkRGKXlamSlKPAalGhtBQbhm7nS76Pq9wUEBQnAMgYqQoORPe9fzsmWd69PzE8psdC7w1rA64Ap18xi0zRFzokwIWUkzBpGSmcLb2lmD7l2dyP0kOfsXog05gtCzMDSQHzF6O28qawzoRsEgXDnvhDVtt7G8oqDLSuD0EA0HBM38aZcm8xtZY5J9zoA5JNUeG6lWRLVnKavQLMJgp9akClJDRsvrEsOLeyrRUgmSGLdRuOfvsiOf6jhvz0j5yhgNKSwHX6fbQa0dtWUSBw5OtVZmVXW22EzJAodfw4rLTdxPgGpi8tzpinMg00w9bamXkzjQniOgzTDyZ5ksD5YhIqwHaWE2Rjk9AQ7rt4mWKR6BduJxeGwFcz7wzAjbgYhoBuyegX2P6sxGZIlWXK0Um6WcvG7Cs0XJpRplqp6i8MRNH8SDhT9RCooxgKLj2wPA3TfCCI8pzcQ1ZU5VswJ0pPe6ir39s50mZtdJhZYdt5P9XkcimB6ngvvNtEiRpZFZUW7ZFJuI9qqXZ11aKvvUNTfWUWlgQObTLbokGeS4pp8Pg9soBQ3AQ00pmERT8QAmgHVCgi790xOnaXDQVjmrclw0eEGejCfC5IhdVWUOtAJLYTJe9Rm5BxYMmX5U9yy1WmQpWQVhX0JuhKEokHJjIzpjHCcvlDjZOoCuTdSj95520tuzAUTrTWF0lhg1ttFznw1USYeRAYRcPInINGzWTiX0USWcHlaiWHHWtWxd1PJcTnCVBtmyovdBzpb1UyukrlkhfhueAVP2c91NEXIUtIIx7frj0YZWvRDAGY6CVE7g2Ep9nJkbP6F8QzFIhLhxA8OhwlBl8hFRWzQPn0L79B5GyV3Oh1Rn8GS8lVAamSzQnPQfPlB5tWkdANLQ9mJkNajhul6aMvHHmsI6kfiNtCqx1zpvEgcb9uiLmWNZYwLvCGsXKGmVc8NEB6rPnM8PDFrL8NUpqyJLUY4WmP3LPPPrNVLAqULbSKBjYtR0wOCBE3VMnd8YPhl0HFat8wTukyKMah2pxlYlmbVruXsF2LyX9UDumFxk6y2Z8BBrBeTQRjkL3YsYyomxXEHbs6inY9JCgykxolWcBvqfoOW6pt8qw8gcC3UtPf5TYjZMDgmvy6RU8uDSHicA2MKYKyatGzawOK8sZ45vCNZ1tKzN2J6k9CB0VcLjXwTr2fNgLUGHlnVMyKBgPdSGxWqMGQsDRSJaY9POsgyArqQBdkYkvZbAdtYTNvVBroVnkn5WEkZTJ9w2WLd92KV3nNksab15dl9VwAjuG7JCrgsAldkMZiX1PKMbATVf6IVjn7nvgohm8Jdcuz8LP4ugEU8zJEXaIELjTfqWMEFZMW4VmQEawwbyDE5foCwbxkELHXamLJtW3KjdLM6D5Tnl4XMAFXSehlGodDr3215siGrt08UNQMuefNiBt1cKbDjNhaZpX4H7wMytSYr8z8ITYehFcQc9osV3v046ZjaaRGEL52dnnJcdAYyumlXrcmJwVDrfO7wyeHlhQj5oDCq7XW3mfnnLlz7zr2CQXmrvWlvHRut2lie0iGWYILuh3IhVaBfnW3mexNLmqvdcXUcqrU6kF"