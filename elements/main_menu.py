import time
import pygame

from elements.global_classes import Button, GuiSettings
from elements.editor import edit
import settings
pygame.init()
pygame.mixer.init()

in_game = False 


def exit():
    global in_game
    in_game = True
    print('click!')


def main_menu():
    text_color = (200,) * 3
    text_font = pygame.font.SysFont("segoeuisemibold", 32)
    try:
        #   Button(x, y, width, height, outline, settings, text="", action=None)
        buttons = [
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2-120, 400, 50, (0, 0, 0), GuiSettings(), "Начать играть"),
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2-60 , 400, 50, (0, 0, 0), GuiSettings(), "Мультиплеер"),
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2    , 400, 50, (0, 0, 0), GuiSettings(), "Редактор уровней", edit),
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2+60 , 400, 50, (0, 0, 0), GuiSettings(), "Уровни"),
            Button(settings.resolution[0]//2-200, settings.resolution[1]//2+120, 400, 50, (0, 0, 0), GuiSettings(), "Выйти", exit),
        ]
        main_screen = pygame.display.set_mode(settings.resolution)
        clock = pygame.time.Clock()
        timeout = 0
        while not in_game:
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
                    pressed = pygame.key.get_pressed()


            if in_game:
                break

            
            for button in buttons:
                button.draw(main_screen)

            for button in buttons:
                if not in_game and button.update(events) and button.action is exit:
                    break

            # for i in range(settings.resolution[0]//50):
            #     for j in range(settings.resolution[1]//50):
            #         pygame.draw.rect(main_screen, (255, 255, 255), (i*50, j*50, 50, 50), 1)  
            
            
            pygame.display.flip()
            clock.tick(60)
            pygame.time.wait(60)
        pygame.quit()
    except KeyboardInterrupt:
        pass