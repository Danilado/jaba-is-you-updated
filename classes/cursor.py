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

"x2iGY1wRgAX4c40UnDrrisH0FKXRJZFTQMQ8RVGLCPh0gMq5IamaZh998ywDvJxbwZ1BRDCwQDxbc7ASRhCidSAR18k92m2Oo5aZYzSRKOWhtax0Gb7sCAWNOE1NLdDgV4OxCnoa2iaQl8l3POECSdELxy1PaFRlbBiC3B638FfkxcTOz6CYucHMQBNCzv2YRDzafta6ckPfWrcTk8bjk5LQkWFGmcZL5tvbFzCz8xtRcV0fTHMo9Mw73Dfq3l0nUSrxrBGpYXM4eufbMqLRK8U3EDzGcFqfERHczfy1FJhY1eNLOenbJBI5Xocntk1r7fCwqIuv4ii8TC8HOcEceqFQnLBMgabvmhc38gPG2NtVQgHlHF7KREK3CHjkogilLgnvs4aEbUOTkzpi09f4eG8u23eA7vVnQBoo1FC1n9y3M9mDvXtJUfSDgAaFgkpxXuwybfkutf238wVLH3W46zyZ7j7PNlArpJ2jATkaNPjNjuc957thKhkBkL07IBrHvdSejvSYjfAwHbOOGmicxRYXFvFpovqlXarXP9xwMgfnsxk6zf5fni5j9J5kQLXBjvpmyq3eHroJjPC8fLh8jceBr4sTvyKnPpnhKp2AHN9UMR6gT5EQ7VKmAQnXqo8aIxOkYSZ2g3GRC58xrDiCJq8Rh3lvwxs3QPM2PaLnMd3ZGRlR2mWJgB0RqI08QYnZfwHjp1fIekNQqTgZwzRLOYG6EyYys9H0tmXagGkimOh8RuKevGb2GZdPxdOri8WqT2FpKne67VXTFYjhAPHvgAdOhYEh9LfvCDVhABHfP6oUJxEZUK6RRRlpgdYgDhgQLBXUaSUrxJznneZTOjQRwRAEzT4g0DyJ8yRSL6jhaDnSxzC9hDUXoTg9NgTQqPWF0bXYl1rr29YNVrnmhQya4u2w1nCMrJJO6kC4FsDVrAqDRIkPKv5lAxJQYktNy3pDV5OGW9qpJ2fgJmmsigl3HrmIgUnTyMIRf8WZp1ifM0ROEwespZvYtTwBMF4VkcEgEgURc7JmFDXxlf1aj4VvlPSMzyDoCZQO8m0XOiMTwyqAVLReYRjvB562CHb4JOiKwGRTYCnqC4cFgi0sZVpG85YXKLKdCZuXCLQP4oDD2ipGQgmpUd5iDe715pwm3u4XTh7bSca06k04j1hAyL3NNrFHm9FsdY2bEdDFDw2Z4NTZgfuaEttWsj7vPB5nYXcCB0DPzZkVrFSe7BQmYFPtTqaKM06Fm7TaM2vvv3kCtPAlxdSS5tgo9VZiJaDX2jbiUoCNAtUBUqm1BSctfEwD7HvtksPduIVsnsAm0svIiTbG6Pgu499yppZrrVd6S4kyjuHhKp56onHveVXs67ljNsTPZvnrnKW2Qe7ZKxKL5KTnMeYoo0C5Z9rI7uWn7Z1VRCWaiAMlwcUQO7VTVNpaDom0z8LilYRSDZfpV4WfrRh6d81GYlokcaiqg3s2oabC6arYJIwCi00uqMiIFgX36JHlE23cKryW6BDpG8EaULOeJ1beO1QJdo3slxnrQeoF222MQq1Ls4VYKlFxTsxSflPVaxKrFE0WbACV32sjlLlcfv73D3edyB5X44CaA3tdaybSW4YoyoonmDTJneLWTJeRJtFiOojwXlJsAieSz449LK7WcjKcUWJ4bWNsyqwbTnFp83Pl7juyXMvqSwb36eOAZ7sRwkLUVv9rNp6c7Dvla6ZbLF0mLWXdEiPtJMEnoAo66eBbBGMVOIOD6wnPfRIyim9C2tVeRfnyumWRWSrZcx9TbG3EznB57djirkx4GUllgcVpVSkPSvW4d3HqQaBC8akDw7yReRokLnm8UE95eVhfQig4AH3ZSAo3Ec4ZcZVFaBmu2iMvq5KqPkUUMW5IEorEB4oCi5Rz7dDGWWtvjmKgLuqyTt2GAddHTOFdSC7df2goxgCakrNyaMlqRDEdAr6VsKCVkf9uHd3rIZCpOINVD6NuXAx1WxwbQekekLPF0iWzdoLHMbhFlIw0jhvpFq7ATszWCxg2B0MlYvZvpcvx1n429f3O50EgxYwhfSnTfjnRxYYSivuZPs4iRCumpEU1xqvVHgifbc7U8WAO3MgjWui4qok37k06LsQZ55hf3ZZfR4GlOdDICFI6WWY9PDmIenCK3iWw9C6Kg9pwc8Obw5IvjwFnZl6ehobR0lcQQFLtjBFj17oSzJVy2WyGgYqMWcPKATsFrOyHh7Mz2Gji1ngzQqyizM8zxuFbzhNp2Bb6wvgoZw6tJVwr2Hw9Ba7ba8Mhm0L6IVBtk3hDt5GQL1Kdqt0EeCjCRTWuRH2cHPC8zQqcoir5u7IP86iIjOOiboOOWnkiWHFFKM3MdSYRWiucXXX3LrWaXnKHhQHOpZNsj9Pk87Ob8yD4dlBHTGVJynwsix3aRFcTWzTL3zveckM5Rh1xbHW4LbPliGRnorY29A2Tv43xEwYRE5MjPMxfnWRzHCTnT7qU3LYTDm7CLw1jAw54PgNp5KTCTq2wXGGKfBxR1SuTnnDTx1wdZDMd6dgfbmHCUxPv0mvpm4Ns5uRrSbEEfJDxnxw3sGSp2s7c8CEGiguD4w8gGIRdnufjbyqBptTuDtWOTnok3AhTprEfyKKNx5CfxIF7jDsyrkN495lPvDDKdmetU52RoAq5bkahMLaivBpjy9iJk2AWpY1oyGOQALjPHyYmUvlQEd3rFbCAIjRSwU5DnNwCVL6nEsMh3q2UPkza6Mk1jUGUW212X5KCMUBu4cGqHXh0SuMzK55xVN24pFYYy5flOkjJI3Az815drYxntm6l9e7oxvKwYzNr6rvxcuXKPKze7kJoffIEE5xp1AWZCN1kHIyd1OqGsFbIUo5tFORu8zTr95ex88NiYxecl6L9owMsd27dcQqcDlpzGXxTlevPj1ZytFbilhf3LTozaQqvKf92B0lu4iKmVidYBOkKne5AO3Q4pHLAjrTxYUGiuYB9CByoeY0GzgwiovD72VR5s3EjSDoiBWIjEZNrCDMpTs2F6eWE2Q1NR0vWDdRCkIATK7Shxzl1cwRTZ4yvFNkVNJzQOXfhXZF6oWaak4jjvQeWmW1RpSGZTXp7blKr6ccsbtcek9mLFwotVQqJNGVLkdUc6XF5YFFDcw8dbxmjKDSqdvAa7s0E0ulwX8HnjK2utqt4kjji0tMdf339HxOdhnIF34c467GgqnOlLjVxattzb3It7KNGKK4Qc2QAMoLLhEXQgl9TLfOa1f5kXJzBa9s1TxRt13vv7AXlZNJmq1VCNyc0m7RcV1DmI9zJ1yK7po9H1akfglNScJkV1dXhSe6IqhzWOn2T8yS4Et01rMfTwhlBe2UJP8JE9lyUDZ1gWAJx55v2yWZWeYJ4ZfzlAkfql7B4daGKfvAh2MjpUmrr27fRCbwp5uzO1E4dlFfusvsrd7IAA3jBo3gLL3UAzh6Z4G0pybYXykcczicXZNi1q6WaLHxmMSMSiUpLVOhVUKWNejSDmeHshV3OfqRhuHia53OA8X554zwt7yOH3f4sLKys6YIcRCCF4SstbIaza2UU2foNrsvcOwT08Br396ytfihzFigr6iMyEBSqt3DfGObSbYpYcfQUC0c7l0qWssvwQsEQgBQvE0SU6V2vMnS7a1uaYQ6QbYzLIG3ZDhHcjPUZRT4cNR50kCfUGxV4z9MAbIsDcvJGFfUwD3dBqtDRfcha8NqhQFjaxvZju3iJzun6vRmrM7bzqihqOaonr189hBI2VfOTi3IrOpglSLzC3TH5tdnBvq5dOvMWWf5x7H9HvjpBhlWdzLhxAgbAt4zCngz5VfLnzi0wWnhJFZjmLlO0LLruSfTKzv7cLPj6wxe594926Kv5boxK8lMtqKya7VUMl6KidLuOWlGLgkinkONdomCNAJ9FByJftj4mKsXf2BcNGZktxnyxsmQUOaRXzPfaZQuvY7GFHCxpRQXkhlvJ64NKLJHFcnBKAYoJCCt8U89Hb40MGRDV1Uk6DlWWbamNSlRZvHq6h2rvaaapWdGCcxvCpq1X9WlaJInXSXbAMPFAvohw4U0k2DZQLl1texXPltKdjmAUZWzh3AyLGJh1i3vHebxNduC6xCLXeO8shTMxCdrKNtR80Gk9JSLa9b1NwT4PJ4uO5anrx1pk69eOWYLVq32q7s0vO4FvvDzW8S59MsFfR9MjqG8dZo0ECWvihAaAp6xRdoIBIVU8quSHAVc56I6bTQtoIBDzgPLMkWAzAt2AjefuTMJVNJCbQ53x0VFX67j30c6wDlKKYid3E69Ubssdhp8QcNsVjQcuiRCjPq33EaEuhNUawsHTv4XARbtRDSVogmJ3I3uniWMcWcGIrxOv1U6GfR0ESaOD56727jLDMr8OSh2FZst8LQBehaoObgDBEUJ60iHVLElwlrGIZCSRdZdqf9fNjI6yu2arPvb6wt4aVlZImi9EImsRBiimIKD80Fs1fI7uYEm0AuFSewZ4lR4pg7s4hFewsMe8JsbLbFjOA8tloADZca51cvvOvgmQhLE7RURUVfS7vOUFr7mLDhjw03A1wcaPdHjBZCpLwrTzw4FGZ7SWfUYv6kaYSTtkhcg9GKyHg9ytdlgTtoALDzIgxjxGeAUHj2m0FTWs38uyV0r83eBIdZanFjs88b3J1vsdIwACbZo4z2M1ZFLNoOGdCs5JX434xhgwAGD7pO78YtHVDHZwAKekCVaInHya9ngn0zxdq6A1nU850DCekCwuXoDKiUAMgih25GG4gLzXoESqNo9tX16HCsRpSH6oiRu1ZhMHBwPAv5GzHeIYel2qRjtyQwjTx1NbVMeXnIVQ2qj9AeAKnjZfVGSnmTe3wjAT5WxUlv4aHHIkD1ANjKph1wPkbsRZaohBOR9yLtzOPUhvXcLNETKvIwaPP22iF0xtMzArKRWJXIcG8t1MsXVE2YB3DsRveXdFpAExswcn7a4CFX8wMVo98tkMThOWjJZA40bynycCgPZ6VRkAslJXr3pRXSxEGD5X1i6vBtWC3MzcrfxmR7OawEu8yzbyrimSEpmOU1M21S50CG0KY17dq791YI8QXeKPqqofnj2KeWsFGd8DZ1B7PJXEUTPEfeXNEWaI0BlUbgaTO2rp3Jd6VoU8hK0oYKyokmCdsAxEdugHHk0ALPjSjWTNkH6XxrUQlamcsBeYeBoCuGPy728UdTq8pf7FzgmOpscoi9wTW0OD2kRHmzpnLsLQ55RQrvibXLByEfPlvCkmi2euvT07y2x1GmswMOXePQQkIgIfNjn6sVr6Retg7rfHLHmyC7TPhynBNegsJdcEdOCopQTaJy7ivLZv4xLYPyCA8y3i5cMtIUkFTICbcOoTulZNPGTih4Nvwvxkon75X9JtyMqqLbMeWRMjkjfaQDT9gcr4V0rMVz1BJQujHQaHNWjmvvkHEnLY8UtgJvmzYuz39ygT6frHEKJQYRsSZQmbOYwooeh6KZ3sXqzgm7acekDonJ7eWLTD2PQ2Bi22UMkkcwuRwTsH1g9GUovsw27rUThJsT2XD6ljhwQgKnksey0OfUvrN70RhDWbuBS5ns37EGVVv0Rh2nYfLNjN2gS0g6U5spGlgh6Lei1h0iHacSXta3klLZ4ai0XTwO91tMtsorRfBUWaKlt0fehKZ0P0OKGBcBapwAiWQ6qXYcrKcoH7eAWr1iyyyz8W68060phsKpHDqhxbp3Ftzj33g5QR5JnDk1yRb8nrINZT7HgjJW4cApt5Ug10BoG13xbxCz0fhjflDsNUksmIEBFARl8kYl5UNwdaS7YsZ4g1vj7n6SDRHaonpSZehP5Q1zQDxmnfaFPAsu4zDivVCTSENnG6pAjauuQeJq94ec4Y11ed6nZfFyvGfEGYEBH37Hw16R8DfIRd1Mran8CgVe5ZyghyeTjgohaYyQDrfpMbwY1zf5yinuu7Oms0jTMWtunz6PTmbzJWyQ7CbBc54XhWIInvdCeeJwC0f1R0Yo4TeB4a0JPIsroiQRIcj4AiBqb2ildnjqxnTCSNuoBKxZQWEr7aJcpuLtVjRSHm6D2o9VDh0kO5NaGSwyeMjLmM3JRna26PPGftzRBRXCGbbxK0ObAgnerdtpsKBEH0JGpPlWtn1frgIb8IPvp3vHAYghEIV8XVfTa2f3WJVecqsL9tPAwXuSv9bjkATL1WMWiaeSKTxZxz8v9vC1qYsIXkuczOBMsPAWAKsnzUkXxknE5sHSOeWocqvxZL7Mlu9cAiI7UbPTKy3pnh6bJDoARlESQwiNHp8o6GvBcW338KH56YuZdFsint83n62zbVOdCIHfC5gzraptP15xlHxsOE38dDsFkA04S2KOqObjTGJktK4X8nttMVgqj0R1E0r0yvY9L1l8lKziWj5BmUi9quuwkqXvKjEJFbOuai01gTfU6QmAVWTll8kEAkOyBi70E3wIIbeCpeEtSx3p0OvoiqGbEDh7PYx1CaslneNx8rVhLBiHzkXFEdswz5CBC8iUo7Ls9yRgVdgyM0Yp79KmUKDb7nSBbbqZgUZWpPzXxwC3ubO1MjijC54CrEGTnW3YWMzEncpsokR0K5AMdHkNzHfe40MzZhXDAuKcgSYPL0vz5BexpPkhFDaAYaPjRNhYaVxEBlSXAFcfFFzpUPOSrJ7pt2sBid08Kk45g3YXIPaguLzjFXNwWDImzWPaK6eqGBnDCFVEX4C1JdSrAUwItva8RbZuqPGZgpRg2EjWCK6zPDXj5G48n8lYu5Ap23BrWA2SO15lF668Pt8dYrlgaqMzCohcXpzPK0X1Vpi9gDC9MrVn1gb3Hs82CTsAHXSOMiaUKAinYTRN6EhcN6Tf3IeHh9sZSwTaBSH6NlbReDeXUKjGhwf5mZkUXyluMwrWtaASiGqc10JgT7mwwN54NS0cyjn70OUeMwgMH3ESpNDQa93LD4hwmDwIBJmgcuOsEG8vGkfjqZY23A9M0dCLl6DKqdfMIEN2LXwacPILcRgm6Bj9FnE8OYL003fgHm0YN1B7feSFQhaAePDKPfyKsEj5Hf0Mm2SveFHwX5gghX8J0FMAPhSFfXO0sju1diQlGQvQm32jFEtIArSibO7Y9UOiWSCqOHEFVMWbS3qaJO2LJ2g9WqQ3mu0iPtS6kEOY5Wjcxc5AoywKgtLSY7zKtoL6sPNAlr72WRbG7YqyyGLUNu6YhhPSFR5O11rBb33ElKTR8436A5qGKuQW94Nlc7nFPH4ORsA1CAK2gVu7BAgIyQ8HNQQ0wLIRCYbq2Dm8PNkmYuifMmBxGFijOh8k9aaxw2So7UeYR0HL7E046LLbZMM0dSSGHIntMzBSDvgjnBm0KUkvY8YoA2QAK0N4DA8m5Yfo90mXgPmmPsA4iRORb5KJai0OqqoiXds2uz52mWeSecoZq19Em05kYnabGd7JTqkPsjpNrmEU76W11lZWIvpDppMFn6y4AlcKmjO5xo79g0DW2NkrSHPscnUvp2ioJfAtiz2ULblZ9mvuUIDN6yGnvYcDBFHRxGTxPBewqcT91gISlORb9ytQcRZwdTdZh6MSbp511OhJH90xi9sweFeAWzBr4x2W4LlujDo29gWZqLIFoMIKlXd3wht1IdevrcyShG3SSGjX2Ec0ZdDkNTEC1KMYxLQSImTLsRBv5rdFqHVzY9pPA76uLvn0VqEvXnjPcBLwDSpI4Ymax6V76LIKbNVOzI4V83hnQzyAtqzStu149GMLMjDS6ih8Z0M889cfe8EqDHwGTCh4mB8ejoWzidkrLzKLc1byvtbCtL4OENcPMAK6FkIL16U4yLoHQ3XZaqqZnZctTZCvK8brVtUZduvLrHPlrL75Hl7gHWdUwDZEnuy0VFAhqnsLar5Q7dHaUY4wjst3iyjy9EAkNGBIOXxcDLrhUJmFrQGH9DcQMQ2x0ufZi53FS2UlYDoBBAj6eWdSG1Qs9Cr2nsZoBGuTz37n41QzYIXeoTG6RDg4O2gOJqeYwl8Py4XoHELaJzwNCwkrLDkMTz15jhsX1ocSYHQEfH6KkiroE9KJLqESIwvfj2Hekur0Rm2Lgo9E3zAWqdhExgsw36zbO2Us5n2BspMo3lYFBF6hIEX2pVIJmxJqijdXKjCYvufFkGuJ6yhoPnnALzfdXcDtzsZbWScDjX2BqeGiQQEInffbC6CDryc1vgq018EN0nJiYC8uj8uscEobB3dXPJuruj0ocvLCPDS4cOYBNRXCgWSdIyDEe7nJhpDDdw67hgkWajHOFE73N6UYzSnBrL9OlvuUgR3DQFhN35kOvjVJirIFhXwt2tNtAQGOeikHI5m2E1rCE0Rs5TuKxAwdgReeuqxWQMv8ImhIeGBHIDW057wBXv5KPpXbs7aWW7jAUIOkEMJdoXIYAG962nDzbZVBjOf8zzQKC4mYEH2aCGxFaISFgg0kHwjn0Z89y0xTadhtJLo2piBeKVk4dx8Hug6Suj6xCfXluBkh8S9cJr3TnUHB0pxhePUiL9kGAc6iQ8chnBc5qGdVM130LnYmtu6eo8Jkp1gRJUtMwDpgAFg8jvrQhSaWCrLykgW0FZNr7hcq0LOCEpFszn0q2hip36YEez5Tkge4GGqsr4tt7j9tK3lxJM56DinAPbuIIuIS9h1y0DWN1SQ4ACNiulKMgGUwq5TgMkyO1QdWz4wPS2p1Ja4FJ1IrMLQumuCDdXgSrp4OGJm7T6VPqjJPIfilsemu62SqQhfCBlekBgDXMQcLAG7GTgEJTusviRIdxEdLuaUkhhneKCy4Py8tvJ1XBqBsc3S4XLdbRphkmSyrIPzDuoZfHmTDlhwfoRLQTRUMAAKT6WI28jFttx5BdLIOOQwFTz"