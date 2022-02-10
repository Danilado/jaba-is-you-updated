import pygame

from elements.game import game
from elements.global_classes import GuiSettings
from classes.button import Button
from elements.editor import edit
import settings

pygame.init()
pygame.mixer.init()

in_game = False


def exit_game():
    global in_game
    in_game = True
    print('click!')


white = (255, 255, 255)


def main_menu():
    try:
        #   Button(x, y, width, height, outline, settings, text="", action=None)
        main_screen = pygame.display.set_mode(settings.resolution)
        buttons = [
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2-120, 400, 50, (0, 0, 0), GuiSettings(), "Начать играть", lambda: game(main_screen)),
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2-60 , 400, 50, (0, 0, 0), GuiSettings(), "Мультиплеер"),
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2    , 400, 50, (0, 0, 0), GuiSettings(), "Редактор уровней", edit),
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2+60 , 400, 50, (0, 0, 0), GuiSettings(), "Уровни"),
            Button(settings.resolution[0] // 2 - 200, settings.resolution[1] // 2 + 120, 400, 50, (0, 0, 0), GuiSettings(), "Выйти", exit_game),
        ]
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

            if in_game:
                break

            for button in buttons:
                button.draw(main_screen)

            for button in buttons:
                if not in_game and button.update(events) and button.action is exit_game:
                    break

            pygame.display.flip()
            clock.tick(60)
            pygame.time.wait(60)
        pygame.quit()
    except KeyboardInterrupt:
        pass
