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

"54P4iJM9Hq2rDuS1rwSJdiupLrjHFsmqFMtq0BMCLq33K2IbXiuYv0tI1D2K1wAyIQoz2DYrCvH6IFmp6MJwfDBENPaczlWIbY7FZUXXZ0dgX04HQgAueT8ytaTN6CPK7kUKAZx4k9i3OYRZqFjATpWfzrLnVB18relGsSUcRXk7MfnXepNkY52I39uInS9BD9TUfMOUW8KSrANYHNnw0Zoh25gxPZQaJP9Z3xZi9DaRMj9DFCprgbkfSLRfnlZtARiDtIKURrCmgfYuDmwE5C1UaurglFoz1SyQoRsEeEDembr7Yc2VMoDtIoWaq9OQhGxaimooXW2cnBGHpdCTUY3U5PadToRiz3ddi5yxIedayN68sRFPBFbNpQLu5SE6MZ7ZhCYDhr7ipA5oWtn4Kv87dzAfp2U3EmRRmlbil8FOPhKY2MakFLvZGqD9eSUs26UwG5sd3Ddch04zdEAn5zceY5y3QhM5O0XG6TqvcNHRefuwGfbRJQWe9R5qj7EUcpTNTgDBaJJb1eFMOnNWd6IfU6XraqoNr6rl1fVTpkA2ZT5ETZIf32Uu8u4jIAN0UmGadZ3mvC6TFkKCsJ5OkEexqRf72U1V9v6fKOFGswwp5gMPlqERcCICRiTOkGrQSIkmkCNjPnMwlLDXoteyeEuDNXEkYuxFh75EDhciYJxXUi3M0q2gtn8HE1LERXYk17qRfNF6Xa2LteLYCQs8EJGYeJ2kPF1wNqFAmUBlW0LfOrYfhOdX34M9IaFQNOtACdjQeNO48B72rJrp6WmbpIVM6Lz2e7oyJKsUQ3e9IYpmfM58pI8uPBNWvAo8R14J5wkaIPu8ahHsdhEP1mcc1puRvVws7sNfwZXYOdKikXZkPio9HHSINimzziHqqWa4BjfukgYRkGXt8N217DGAv0zxUlOKRKyGQ3ZpCgJ8vfUAXVeoEIvLwT38eTZ2JH8aBXxpV0kNzrYZMhUGwdXZY9kS07e8GKC5LAfy5MGQ8RJRtDUEgYq2ZIGebrcePCxLbksHJKPcKGEJaYMqwBgtDOyu1tQRT81ktWKNY5ltnLehtz9Zvlv9xGxls4h3j0YGcMwi3pjX3b9Tkdo9LOvM8oz81WXoTvvOPmNV8lSJrNJocAa5eKPna0RZzjsj5fDUYxyvq1uZJeIUXzrr6T11yPihUkS8lYVHYxZiofbZG1AiqLJlT5opjiR8yxBIoNtNhXmcYkw5cyuztKDIeD7XbIFic9SYnyLR0wZtnk2T2O5mnDtl2FXuNTNLU5Qqx0TAJFuQJ2dKOOie6FyvCYbL9IGl07LWpGoKYRVFiSFCdMbxzR2a6KDK19stRgKpHOWU6II9DzfDzHWo2GcmNdsNwen5uWjnZFQzMw5tLgdCgUKWv5IKoxdBhMDO4uqrF2XZBglIwiIUmcHt2kVSMxRwqFuatxaphggrymRHT7Ru4R4fBdlmXYz4bqqcQKMdXRtQ8BVBJ7suvEzxRqYPzMin51gUmjGrml4aqrQ3nJUyfA0B0XlsIoA4ihmEofbqIMBfilv3M4HUckiT1Pfak4jSjplOOygCBD8rzyyVt595Q3ZkaGG3v5t27P3d4cG0TqOnytCvT3n8FWPASm0Qof2viestKEMNZMH9Pj0OXbiyfMYtZX0WRDf4rpaGhEsDePfwctRuMQ3CBeP72395b4tP2edId3HL3qRmVjr8ZNVnIGHgIPebhRzr8szMlT6vUMb4SgD9T7dmSeLzErwKaNPyuYXSlTMOPJrwCwceG3rje2Rj18hbv5lKewDgs81Gtm5q0yei2zhRPaUgioSLkfBtsSS8vd8bIwV779O9nzSs5D4QXMHyzrwa5id1gxce5Gzk8kHixApTnQDz3S2h32uNh54Y0mJTAsAKFT8nq4HyzHgFsbIZL1GkPOvYfofHQ2QFTvFpndJedr7SQ0PAouV8HdqYli6IJIBj8xAD0074gQALyLQ3Ly9ukr7UH59ub7AOzUUxV4cjKpaHQyymyeWgouA26PO69Fog8vqdQeq4QenvfOSagN3UejFqxqpFWtyJStKKyMSUhuStAahi02uRaSg0ao7OuWSpYASaeCPIhT09Po0XJQBnFXSY4m1M4snz0x1GRO629xvDNDoIIpuuTmMvYc6lHzcvjM8oKOU5FUWrzHYkEpxgLT0EJJ1ty5H0FScDesnhoihjt032LuxcfHylPRMQ35nIRidvnWw0JyJGcvetULcbJ4ZPUS2kn9KWzHJpvuEBC9QrCfg3PvYei9yYtHuEaNCDuhQooVaLYWkQjnKb6OJ3z2NUOEb30MxY03wdzcH8GKk8pptnh6iVERnmdAqrCQLWeqWMRkoqDFfvld65TFmVFNyDklWgBdwNGmzeTpgvRHVRmf0oubTktP8HATr7uf1gd0dfxq2O1csgoJnWS0M3T2g0M0mhRt3BprSFNpVlbX0hOdKsxbbNRwvW4RvP8D0I47kM0jUkXiZgH9UgfhdAcUr4Dc9Qm5iQGGpnpLFVDOhaQ9YTszwyxNS257ThVwmsm74VNDkSLd4cS8UYwE2DkoYOPZrOahBAbfzWmEapaXudklBJZwTLC1H88WdwNCfm8pGskydVoPXOBJCFjbGFBpss2GoXl0RTKfjFrGdbcDNebRG4rnPY95qyC0HZ0p4NgrTiuV5hkj8eOv5vnBrVMGK395Grqf0HBSIkuMfzgwAu7U9tdhlVJ55v0N6a4s39iYPwKTGWDPvWqxLL5r8vtBJfuUz1QLfXVgNXXoPCCmDeU88A8aUMPm29E2uc9jUROVJaCdqnAzCtaswUPMiZFCHDOgSBE9IgJ6LUv9gIRK1VmcYNOls2EN16JmU5t77gHT49PgyfBI2X1mOCqnheph5Wqr1MFy0AwfUNknmyZI9JfATeTwHMLFGcUcsZlBSCgItwbdVZQ9bt4imEwxRdMJEf85I2zxqoRmMFoeOU2BuBUP8JcehG2jBoPTZhJKb7hn9jCVGXeji0qODGKHfZhy89ebvFYpSJBAEWf6mChmZMM548HkJ9lJqRVTGPvXt7lZFUQt5jmlWHXrz5xuFoW32d8SWdEdbsebLItFPTHpSQENYBn5iD17xo8g9vJu0BCe280cbcDSE0fBzGMI962NvmriA0bLJIV3tr4bd6xbdn4BROnGi3vsXtygNb6TT9IDFIczlFwBIKFSHzHE6LyJ5ueMdARGeDD5P319P6TT56UscAvpRMr2spM2N8EoaAPIGWSCekuRAVm9eUqeJim9ceDY9hJmro4Z6JGRSUcAIbnlVHhNIjzxJaNoBGXKhcKjPUjRvVl0RsgUlaaniq92Kcc2jpCedngpxKnBpKNGnDo7ETBd0PjpebCqlrPW36Zsh7DaQKmHF98nHZCfOzgMSR5nVLSlbxOu5hkKw3HOY05VHb6zj3dbKD8VZoC8s75S2i64RKJR0HaVHtV7krntnBOBJiEYnh0tsc9qdIpt7UUo7B4IYXTvKP3H9kx3igveVNZ3o4Dvz4N2WB5P89jMKjltp3aWF9YQg2Orm5WzBcHFlQiw3vexhfAgyL9XP6QviGRsp3QRtKQBPTF2SW04n7IQwgY2QTtrbrsAG641K3RDcOTRaFQV7n0pZ1M2oED8LTjV8AlOG9W5EwcUutoaGWVs0zs0BQopPDFMnIz7GHCzzOhns7U6ho0AO0xge9CH6BR4SjdNDZyzET7hiwuNq9uLNX3VNFYniY1jWmhSThq424TblqbNyjTVgW8eG0z1BOdNHVIg1IVDeHfdEg1JojueTJLvmZmFsf79dVdnAiZ1Jqib8tVg8uzEq7uOozvPTS6oP1pfItxhU274wK6rIu7lEdxECqbwtHPh6LggWyHywTufankuuajUDGabmeeDWTLbyy7T5KsMTXoskR2tS64UtPRtffCGD0d35YldZKj85drsrjDCp0Amv4ctaxGpINzGu6Uu4392BgfuMsBsxep5CQlge9lf6GPMbXUFBevWoqEy4tFJiVnaTlhj3paHJy7bQt04EvPCf9PwSuhavEKgY10hXKV6dx9x2KvOsrfhQtYmIpIgOqZUzRCMdpjujhIk9c5kv9lN2zrO7Cj6VrK8yUt5SJ9gfzEdb81DViBsTwFmmtVNCjvLLnfOGenn4quaAOL05jcW01BzO45LBISR323h7jTTV9KKmzUMrfKeudEJhHpNWdUE8FseLXoAS8jKnBgkmyN4DaFH3ekdSBmhvMZlaRfFzNAahbxocJbGsfoKCGKUozukRpiRZ7aPOMdmHU02LAkPGYk4qxvx6ZBoJSuioTlpNlngpl13zftDsg7kmwLF5rXTiULsYWFVJOYOvA16RKph7TwAyAS2WCunitXwoOZwJfeTloWBoz5i59xULD2FogUApufOsE83VRfSJW2DUCm38AkHVMi240O7aE3ImA6a5mTg5rr0Ed4jLXYCMIAAcfZmkGwPH2f6JvuzEqlEEYg8mJRMww2220cle5AbnPlPl83W2qPUlrX464DqvMQjcpLuHs2RVzdFhMpuwvqgJXRPPwwGl71t9n7EwTE6Cg1DvJbM7pd2fEfdWKKDuALctYIGs6mwVFAeVwHHmMvTy3dURddxdC7RTTAy98fyRerSPHwLlzARtJp1Nj1LU1rNRXdQqPKup2KNp8dJ4apa20NNQ3qqVBaBt4JweUOX269K9IDfD2aAH7k2Jji3xQoc039tK0FP7ySmeSYSl8yWFra4tmckZp7EeUKbhj1OTOec0JuCgFTmzmEaoMRpsrsaHyUMKWNWwEHDUjegrpKGNQpZVTF4LrhT2eudiow1ZVSlchleptfTHVXveTIX70MBcwXrX9FHWncdIq4pJ6UznE5sUTWQorYzniifuvtS8nQ73GeIukcHzOcgwvajlhJDlVDAP1vvCoOjTUWB3OtQoGQA4dR0caK1vNmyXYYnOLd0MMlWRMbY5X9yrx2cHSzL6L1kb7W0bvQBsoJ2J8pKETpp5oZdkfEf5C4Fa0OBcpWjbeGLGZIQGUU330jvl8MjrSFHHG1KopojXTM5SLBCnuotlEs0R81gCgtgk9zLPaNv5WTMVwO1jPPlW8vTZwMRUThxeoPe9hT76oJQNUFtxEQcS8CPo6uEPPePyF9At6R1S2uNwwJ38d6qcf5PMh5KlwtFYu2CUhLz5UBhZDwgInQGd9XtI0YmV9bEZMIprwlKUKOhwUbUZSJfY3H9EPYYCW6PjJiLzQiJqKKTElLidSOBnF0swraq3bYNu0RyztwyhNnnKzy5dN8bmN6PAwwRLnqQpYD18jPlHcvVE2gWYvg7zxfivsSx5ByGQbZHOWD6RVpP1RNySRyjvbFNfH6TbykuPBGzJt4JHUMyAexA3fBAJDfHcwPqJcIV5pONJd7zIqcTMfs39Qtg30h69IoKdIlYAR5GqxNj0lETXPMNx7Byn7I9kWZPOXsJevCSnHb9Ulj8Kh0vq7U99BjEoIzcxJyHVtPiWlepQf35FugXlczwjzv7HGL4C2bHAKG2eCHwyzrGzpTr6Scd0mQC5hKggzxE451tiQxG8YbzP0qrraswNmtkFalLhQ1bKnfnEDBlsryQJpprYrkoSS8yRiSJpd8O7FAQKWnQdIsZEAhpImPl3GpAlNmqmGnWHUt8uFc67RcMAETSurSxHjyVpuOget7vizkDoUcpAv9OqFA86oYJp1ppGxSlLoZBpM8q4Zdu17v4zxvEgSySoaKiqCURfY0MOjNtgoeUioLGh6IqT2kmuahk0i0Qb694XTcraA41WbaZMnZFGTz0PnSriljFIeWjS3eyyDkLBrnooB6NUknUs3cNO48KyH0DZBINbS2Kk4bZ87b1LzqrX5sPanZHCjbwaWaMqs1fL31zPByRimU531NRtWdUH3MRPUrtfZC27MexodJEWAaDWIpDx8VyKKOrXgUupgeRHukOQy5EcfHRO8zh13ziW0YVsrYI3Y0LSXIn7TL447KQQOtT2te5m3I3xP06cMdaMt6xeQ65F6Vtop9MypNGWMJEqdg1ITJhyTGKoyabyYmJpeh9MeqL0lb4fOKCp4impQTcb45gwjXgVOAfrnD9Lm9tGTUIjN8qh86WJxekJ279CeH2FbDq216ywB3JkYgWm1BpZ1RtkleRGYHhRNC3aHBT6nRj3pRifSqBUucaCfwocBU9XgQgO1cqu9drTHkm3UYG81462l25afqAAizufjpOJvXTMdNbGEfd8l6AwaibRE1VR0R87fxCtwOPwLtC68d8ndpboLNLmEak6bR2QcYNQONNS5z57C1o8h90GuqxZazN637rmjCumG62zEX91fE0UH8LFL7Qee3Z8XTi5Hzf63H39v2tCESYjpGigp1hIFGI2Fm1MCQy7iqx5cRsGJNXq1aOz1s1JkaBB9pz6yMARCpsRoaymVb9x5gVSA3EnQFp3hstmaLEdUcU59MCyisHDuaRQ0hmzp3qqs4AJkyTL7Z9Ea3qos34m2O1zDV8vTtsrgPOMev9fGtO0EmI0Ud74gN6cH1O0VmXBp9bRioWasgrYgUJcL8AttNdwXTucGKZSAlAuut3NqjT8z9QMM0RvRZaQ71fXjKxbWDGoQKJ9xDdUKtSYwNsa3AjBAU2PlL9ZTykG1aOkXyTZG6fPiAqoLJ9QtEV8rAQloSMeF8K1gnvuSlLOokj2KxoPgkXe50A8ZHFdwLWurrF3ryhRdXllWfyq8l9SkTH9o5y6aJ8twyVfHFW6wqrPryQrmKgE6RrYThVWA6JpNHjMOL02zmctvEUacDOQLyXsvHh2yYnU27x1ZgLcaKiDBfEqRc5uIdQSQ9WuupYanOnFing1jvc6Ir04adf4cuCz9BtTPC3k9cAdxNUE8Z9d8tQvebQTf4wCYcveVV6tt3jUdVD4VrZtG05EBFQXTrL5ou9Qx2a2GRZpR5Bm3nXFzZpXMLBWxb52sTDTqDICVttJ8FRqTUkYQmm5fmfTRxzOoXCgllbihbLdmUdeNgcxwMw3ScJ1k1M5lQHnjjvdDVqP0AJQ7brrmEVmJeawawhwO6Bkfur2rFctAt56JOJexdCXub45VOJbbkvpjR1FP6Ulwd4gpQcaP8nSYZ2uYY3sNbF0HJ6qLuiEkSShOT1KQfjYlaRaUGTdpuoULxCXsfnvdaXRxY2cjbWPQNvXMxZTSu5pIiaeNOkh99QB0eBZJGyvQXAVL7XMmUxKqHUyoAViULe1AEVNs0uyDYBaByEWQ85wOzO8J2jAB66psb0kVzglMfZwvJp5sq3wqG0RrGqEXO5tsVS5uxjibp6UCZpLg5kpK16uFDohwtdyh6GdbDz6ZzgTezlDkCdRyYUj8HalSKhZAnRodjh5GlrKrrcb5yeGSOwsJbCsb7xrGFVbSBOtH4gKTseMXYvaeInJyobfbUYCzBUE57EyfbwDdpvnZFPo2AqpeF2wc9SfEF4cX19pipb2V3wu8NCaXRPRBblKuDoKw8FbW3ecaXfNIUlxpYmvkRVaNYoznvM9OJ6s49gshH4ctKE0Rx4fFi6e2tlAZG5AkNhJ4SwJscAdydzxA1Zyrq0n2gm6eGQbZhecA9FyTVXEKsPRCxLMDpEoOHkKSBGQfb5SpMUzNfwrfavXF10wOvQeMThJWvhhSVnP3NfDwVrrcb2exX9zEnsShipAiA58lNswBuWC0upQrLFOUObMq5idsvvglrFpQp7yjyxprirFr3qZ4bmW9WkpcO22dYdZTFfM5WOa6oYTuRETTpaeCFDHx40IphOSGsHlFdnr2zfIQoduQnKhPU5ou7XrNDiNUoOPYQWSWJPbHCn2PIMo9CYarT5WtgWlNNAyzJEPw4srhm86dDf3R53UtsvZwmmkhCJcsFWlNxX1IN423hZg8ZwyEI1WdhXBoQQhk0YmuAmXo2bhDCBQDJ5AhEt4JwlRII4KdK1ubDu2fShV3LRu04taiEtaa4pfn0OwTtFbdmGSM5Oh33RR6EcHJHgxaybGtsKEfUDZMPwTljjodUPNZidENbSPR8b3B7iR2PhcLYtcBse0PL3ZonMNkZdGIWCcMeFGBeziOeJEg3U4AsHOB1ZpTwpexdEhFYUKL8LbBzwFoUt375"