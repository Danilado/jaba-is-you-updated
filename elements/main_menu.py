import time
import pygame
import settings

pygame.init()
pygame.mixer.init()

in_game = 0


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moves = []
        self.status_of_rotate = 0  # 0 - вправо, 1 - вверх, 2 - влево, 3 - вниз
        self.turning_side = -1
        self.status_cancel = 0

    def move(self):
        if self.turning_side == 0:
            self.move_right()
        if self.turning_side == 1:
            self.move_up()
        if self.turning_side == 2:
            self.move_left()
        if self.turning_side == 3:
            self.move_down()

    def cancel_move(self):
        if self.status_cancel == 1:
            self.move_back()

    def move_up(self):
        if self.y > 0:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 1
            self.y -= 1

    def move_down(self):
        if self.y < settings.resolution[1] // 50 - 1:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 3
            self.y += 1

    def move_left(self):
        if self.x > 0:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 2
            self.x -= 1

    def move_right(self):
        if self.x < settings.resolution[0] // 50 - 1:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 0
            self.x += 1

    def move_back(self):
        if len(self.moves) != 0:
            self.x = self.moves[-1][0]
            self.y = self.moves[-1][1]
            self.status_of_rotate = self.moves[-1][2]
            self.moves = self.moves[0:len(self.moves) - 1]

    def draw(self, screen):
        if self.status_of_rotate == 0:
            img = pygame.image.load(f'./elements/textures/jaba_rotate_right.png').convert_alpha()
        if self.status_of_rotate == 1:
            img = pygame.image.load(f'./elements/textures/jaba_rotate_up.png').convert_alpha()
        if self.status_of_rotate == 2:
            img = pygame.image.load(f'./elements/textures/jaba_rotate_left.png').convert_alpha()
        if self.status_of_rotate == 3:
            img = pygame.image.load(f'./elements/textures/jaba_rotate_down.png').convert_alpha()
        img = pygame.transform.scale(img, (50, 50))
        screen.blit(img, (self.x * 50, self.y * 50))


white = (255, 255, 255)


def main_menu():
    text_color = (200,) * 3
    text_font = pygame.font.SysFont("segoeuisemibold", 32)
    jaba = Player(0, 0)
    try:
        global background_file
        main_screen = pygame.display.set_mode(settings.resolution)
        clock = pygame.time.Clock()
        timeout = 0
        while not in_game:
            pygame.draw.rect(main_screen, (0, 0, 0), (0, 0, settings.resolution[0], settings.resolution[1]))
            timeout += 1
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    if event.key == pygame.K_w:
                        jaba.turning_side = 1
                    if event.key == pygame.K_s:
                        jaba.turning_side = 3
                    if event.key == pygame.K_d:
                        jaba.turning_side = 0
                    if event.key == pygame.K_a:
                        jaba.turning_side = 2
                    if event.key == pygame.K_z:
                        jaba.status_cancel = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        jaba.turning_side = -1
                    if event.key == pygame.K_s:
                        jaba.turning_side = -1
                    if event.key == pygame.K_d:
                        jaba.turning_side = -1
                    if event.key == pygame.K_a:
                        jaba.turning_side = -1
                    if event.key == pygame.K_z:
                        jaba.status_cancel = 0



            if in_game:
                break

            for i in range(settings.resolution[0] // 50):
                for j in range(settings.resolution[1] // 50):
                    pygame.draw.rect(main_screen, white, (i * 50, j * 50, 50, 50), 1)

            #pygame.draw.rect(main_screen, white, (jaba.x * 50, jaba.y * 50, 50, 50))
            jaba.move()
            jaba.cancel_move()
            jaba.draw(main_screen)
            pygame.display.flip()
            clock.tick(60)
            pygame.time.wait(60)
        pygame.quit()
    except KeyboardInterrupt:
        pass
