import time
import pygame

import settings
pygame.init()
pygame.mixer.init()

in_game = 0 


def main_menu():
    text_color = (200,) * 3
    text_font = pygame.font.SysFont("segoeuisemibold", 32)
    try:
        global background_file
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

            for i in range(settings.resolution[0]//50):
                for j in range(settings.resolution[1]//50):
                    pygame.draw.rect(main_screen, (255, 255, 255), (i*50, j*50, 50, 50), 1)  
            
            
            pygame.display.flip()
            clock.tick(60)
            pygame.time.wait(60)
        pygame.quit()
    except KeyboardInterrupt:
        pass