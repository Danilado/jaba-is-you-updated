import pygame

from classes.player import Player
from settings import show_grid, resolution


def game(main_screen: pygame.Surface):
    jaba = Player(0, 0)
    running = True
    while running:
        try:
            events = pygame.event.get()
            if events:
                main_screen.fill('black')

                for event in events:
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                jaba.check_events(events)

                jaba.move()
                jaba.cancel_move()

                jaba.draw(main_screen)
                if show_grid:
                    for x in range(0, resolution[0], 50):
                        for y in range(0, resolution[0], 50):
                            pygame.draw.rect(main_screen, (255, 255, 255), (x, y, 50, 50), 1)

                pygame.display.flip()
        except KeyboardInterrupt:
            running = False
