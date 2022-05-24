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

"bBzHsIjHCPXOUw8xxejwEj4aQUZy6C8rT7QbKzU3MLdJMXo7kdCy2LKrHOmMTUbx6DXOApY3OZtHuiRYKhcG5rE9XJVcehHmssOfSrPDJIGKcoeXPJSq1hYJth0N7Iu2kOqBalI57G49Wi7s0EuvMXhygcNfWkuI9JfOO4vpxFOPNkOb2pO2SlXrcyKcKL88MUMveo3eHJl52AQjnSoV2y2DMGrAyjIS7CYaJtANBkPR3bxjMdg56cSLD3mBhLrdKVf8hoqP4dRrNJM9asm9FfzysFOhrsvbyzLdW16dgsoNXaESggCDALphmZDPoDHAu4BdWDEzI4PIxqs13nV7scamBf42F9yVUoRAN6d1X65I9IAc4fMgdeQ5NOMnIGlAgoQzVO8SSRaD3h77vqCEwGY1yJNOztRaww7p9aG04k9zuQPIzauhmxmbycCvn2JDkuVYvzwmKU1ZR1EnNzxXzhAHMzjZRaSadneZQNyb612kKhi8cnNuWGDMXnM24HhKG3dQewgXsuJkyT0RAgbGcf1RqaoQoc0lgdbbzfAi7BFNi5AIL6wNtV8WRwP5WRcbi1mUjoLXkrSgQ7722CInDi7IyrZPZh0B0tkCz6Ti2EO3xYrb9UliJggQAryChCQhHmvf6uIwswL1QPzlwNVuTo9TOCgDH6bUCoYfaOJhoZNNCXB6xUs4EWsVqYMHh9cybxC5J1rBOj5lVPxG4zyWGHlXsazgIhxQXmGDgRMdc6RUfkAIoc4S6qimxTDXB3o3Zn5YND8lxxj1n8h2MoNqz1JIbqoHBMDYI7WJjOKiemWhCx0wtGj9grElYNKinjgTclciM2OBZqk41GU4cBMnnKLg5T6lZFH1VknJoHvLjxJv7R2FCB0n4cST9cNGjKCOHPNA3R0XCHvLFttAEtCTnA9HPxAT984FAQaR3QynJEUozhVPIRKSTHdQAMTwwJcj6XDwEP11kUDRSap4jNPX4PBBiRdBettTShhU2MhBBhIQdLss0yKU02rFEXA43NmehCeq92GUHDzK34yADhedRZfYu2F6r6hhg1elDKOB6shyTSNZcbv1QCMjTCg2kb0ON9CfKcv5sAJmav5fs4nt45GFEpCkPIG9VH5WsyclsTx5KAEkj9dLNxk3DFrcgGjTPI7OOQEmbki0XcbTwUWTT5h4nUio2J8ZVfKExv0IeEvwm0Njeg4tnqEesUurDkq3Z4d8LGatft5H9EX1cDN0NRVYZMggHlxrLAeIWRsQ0mH2z6YXv9r7yHqg0FuI4tFe6OT83o9auFy3hTtliehKStXtnUxVNDZB4CDq51H6p89jK27YzGHN1y8SjOg1GVTkGon39bmClHYIo4K3y3hLtk57H86QskcO0aJu9wSjgNTf46ZT1eC7vZNXPjkTtO1wmuNfz9HiP2aFtxDLF0BnsMXudy1TXT6f87CC34c3h9vawdPA5wzrLNAZJDKlBSry1f5fJVSjJmGatFzERLHG7gGparu2mgv58qzBJwMDrTAIUJ4o41hRXI4vggWKP4vItcYtRSQ0qNTMve1VSxyt5TnYypfpF1wa3uuYdZgYb8Avq7vmJcCovbsIE5dxM0mXJSGNtxZudrgbAMlSpgKPyNS9ZwEWsUKH8KUcun5XI0baRfS6ZoP5cYOeGSfdAaT4QY8HoPHavc0QjTNZ9n9C9W0wmDCKO1kTTmg3KPkmIJtGU58j2hIoSfdEuJP8vFS0zp9ANqd053wXPJGz6rBATXc0UeQXz1nNqebGcnVZAXbY1I6ehcCyXVA0nxwq83C89DLEzXQ9PfhaGnS5c1zFBZBVPO68eOMmpPqFPGr2YVk8Yi1hvajbPorHMk8dtZRuvM0eUUT95qSqkKOLtmUd3Jsb39mWWPwBGgjGVWToD2JXG3mEgl84BGcRNnHhjWP6Etvbv8d8ialQyhwcfsUU47RuGKti4HeHOGpfcI1Myb2qgPGYybOtas11a9E5laSJFdiAahUx8y2lh1moHy1io72aa86XcNkZgAP1LUafhMVibj6gPTo6zVFLvhO7NPQR9TpkWeeV6IC3t0cngDiC2WhH638Lfsleopw89KTSUoQKqqZrjBHrtXi3ixdgBjUcv3PPXR1Qkh7u4D12sVw8M1al9mMdVIcabirxnBQI9B9ZiGf5mT6Jlx9jmxK3CLENiBSoqnXBFTB76oigx80MvPWDWUeVHu04wDYwaLsrAVPsDDwScRPWQhj7UqT83xFH8nmeZODznXTcxzvu1nk8sBYqD5u2tdDkl4sZMqmq2NMMoljYg4wNUvJLpqzR7gnrMbCaS6KaiTdXBsdohikiwwx3qOI1C2M1F1xXFhcfrktGn9ifCjGX6FoWAV4JEtWJhh7yPdkdMUN2s5cnLuCO7dJVeaH0dYehy12V7ojUX2LfZMFShjqHNcguTWjEyOuQro3hKeZT2gIH9SzVji6BI3rW5jQlszGDaTWRyzC1YeW8RES7wDoNbFwnfqwlMRxlZ6fKi08HLxU8aML4HvKnsU6w9aBUATkrwfCSTKp7TQuWohvmY7mA67ZpXZMoGSKD4J4hf9su8LL5u5V84nXhpNIDjePs4UYEQUw671WyLuzFpMzGzPt3fH08iHbM4D2y5gZEpKfzq8LFmb3Sj20AoFiwQIsG7PEBVtuCH8lqI3DZQD9FYQbYSeXKzJnG38E2ZA2k2RCqPGZJ6qa2oqNiycE5ztruWUgnrrah5qut41veasIgJfkD7AtZCc8LXBWqjOOQeIbkcw5tiU8jJoZUmLKeIVPOqtji4wHe3l26Hr00MCFAxMOGg17gV32vG7EpASyLRGOnEQOgUXeDtsyNMtuN6MSvlONCP0uaoYIMfY9cjzQpEqmXSHEMHPwEWMPDvmFwAbFSYUkYud0qjWl2lxGpu855YpNyZAz8RLMJwrNs32AVuwkAnRl6KZQyOP6fkuj3LeVP07xWFo7TGvVLM5BMtOaFNzKPflij7mrVLxoVgIbqUmxzj3AZqw9871qBgtyLQpo2P8xO3jlhYwVfcFgBAYWBRG1aTW2vpTIl9vzRmcupXX6gzvDScr17hLGsa8kCbta3ttnmxQlizyWVEMalGmxo8y8oy5DlTnSrrprzz1Eo34ME5Mks9rCHBTI9AsDLc8rXRwjcF4lTjzpl5mYqAMe3DsqAqK1IPs790KdgMgnzUopkWunIGhbx3iaK2QgQOAHeHzF0HzfwusdGUDaTq0UvYveRKCNQQAtGSFG6SZ39eQkJy7VpVqXSZRKQ1NTFqlTVeT01f3qnWP6duCyEgj2hFOuK0SbJ9BQqTHC3GFoazx5TWn1o7VP3OExUcON69kfTurvtk2qa3fRr9ogoHlTGcPZ7xRFBqQIPY195dnWlE4p6TYoRNBKfzGdBSkdBh4OWPBSLdwuHNXAC21PtQH5CFLw9UvHzXwO9lrDH06vBOExLOeckYkEBhXxmzyGyBxbSQF0aaTE50a5y8GC3NLw1uqVxty4D8CqfTXl9WAHTFe6OO4lwT4cJX8PiI9DSBpvmgdtgeOqysCHkjHUkPwKEdHrRqKJ5xzIFs9xqxF0M1j6LLtdv5DPxBopiSQfhjLMo4Wybh3W0lbtGEP8B7cLI8DkO3Ec4aKG8aMGRiacM5XX0gkm4YFHCnr4DR2cB6FTDWIDmExEVahAgcKfC4iR0syB7gB3rPXDv4UZtgyQhHMqtsRSUCcquJbmrj9x9UmQwqAG4VPTCbnxy9dZrL4pkDmdpBsUtkMicYsFwXtipjt82erqQ55djMt0Dzeb7MuW5avbB1w1jB6LQvsG1apCsJO4dc40qwymYDd6PLop6u3ybP2SF6DYnbIOUQxoCZ8k6GnxvHzp9iUcZKfl2K6gytVRaTu4juF2r4oFW7iF31ofxWz6xDQ5zaxgfKzfaZFxr0BDvd6BxSFh5wLfTXn820oSpYctwgf0qgSHbqtJ1n9J98ZrtmSwpVteLlpz0NKh5j3szDGL7dCu6tE2KBeQ8EWfVjJT4XlEKmYYj86ztV23bNHRuF4XC9P1JtEWtS89b73iA1QIvJzZ7t3KdKhoUb2GiHPE9iBuKqkPXwh8HryGZQUVq0E5K9oXIx2R8aXWuND08FzBjHBrZSyCCb5L5JSbWt2bPT2j7hJQ6xk6A5BuB4RLCDMx7N24OkiEVyi6kX0Vdtskf7dIvbYONQZyAJ6JnyGgUeD4ATq7IN3Wgtz19Q7FL0ybXO9jdOJdFg4RMU6m0QZXjR2MXpTRAlX10uDJcAQsgACUrousXroat3YKz1hOeNuDnQcHpApgmMHREeqiH00X9HuWuQIwBQibIoeucRRa4nfjETST25FHSrtdrn9q8eWhQdCNOyCiTGDQeXUIEBXeqPitM10mT20YrnZQICySwzDyzY1qs78IlS2u4CtsRpEAple7uNU2VHgdOWnnjgwGr0ufShqpyyzaUk4hFmtVGFoDFGjAwYWDxDxOP2gkRgoTDiogEgECqGGcJgehdpiBo9O6anom0IqT2d2zzZN4dIQungqz6w0JSHtDQvQDQ1hWabLVdsrdxLS6jVvcsnprDVg4byHm3HM7CvPucG3Cg5IANtHCmBbXsx7xHkxselbT2ElDoTGtIOlEUzHVBV7kEXTQOmoWS3PXtDOUJ7jnKQZR71CAiwqPTzatJXt2iY1Bg3xJRJvIPJTxtEPbMcVu3wDrkHXpvkpEEzqQvr2SkskYgfHVlzLjILC69lNdqPRVnYj8GDeaI4CFQtbgOIesyYhfw7tWVtPhScMux0eZy7Jt0AueB678i04Zk9wy8MhMqfD84cyyzI8jHn7m24TtzLu8P88LJTp2wgX6O0FkbZYgssBopLBLCeGUrMgmF3e6UQMDX4QrnLZt1XQjvAB41FceQlME4cBfIsywwNA3bEP536YOO87EgmyXMGkUMlCatuLIXBokBXPwDlMBEFoh3wgmLcJXp2DoYHElFBTxDtFAj6GsgbawiPAVfpbArxnwIZhCycA9wgsQV6uoXG6bd4MfmSERrIflHvqPCUMei3ovVYmfpA0ARTWPNcEjxxUls6wMpGyCUUVCPXysrn5az6KXJXkgjrSrcJSjd8kBqIKvkM8d9cl8nI9U2e3Em1KMeuh0DA1w0GYecmXrTj4A8FzOh7T7oLXRIwinaexbOvxKw0LSfi0KLcluCjpZOpHguAjE36tpUDQJWyosLeP5IUi5Xrm3LV9Z2Yjxo7bWwOYmVO932nrcIUTa3TNy8GP8bq4oaleZ79zfS0ZqM8g2mlevJ7dReZ9F"