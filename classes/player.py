from typing import List

import pygame

import settings
from classes.animation import Animation
from elements.global_classes import sprite_manager


class Player:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.moves = []
        self.status_of_rotate = 0  # 0 - вправо, 1 - вверх, 2 - влево, 3 - вниз
        self.turning_side = -1
        self.status_cancel = False
        self.animation = Animation(
                [pygame.transform.scale(sprite_manager.get(f"sprites/jaba/s0{index}"), (50, 50))
                 for index in range(0, 3)],
                200, (self.x, self.y)
            )

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value
        self.animation.position = (value*50, self.animation.position[1])

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
        self.animation.position = (self.animation.position[0], value*50)

    def move(self):   # TODO: use Δt to calculate distance move
        if self.turning_side == 0:
            self.move_right()
        if self.turning_side == 1:
            self.move_up()
        if self.turning_side == 2:
            self.move_left()
        if self.turning_side == 3:
            self.move_down()

    def cancel_move(self):
        if self.status_cancel:
            self.move_back()

    def move_up(self):
        if self.y > 0:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 1
            self.y -= 1

    def move_down(self):
        if self.y < settings.RESOLUTION[1] // 50 - 1:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 3
            self.y += 1

    def move_left(self):
        if self.x > 0:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 2
            self.x -= 1

    def move_right(self):
        if self.x < settings.RESOLUTION[0] // 50 - 1:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 0
            self.x += 1

    def move_back(self):
        if len(self.moves) != 0:
            self.x = self.moves[-1][0]
            self.y = self.moves[-1][1]
            self.status_of_rotate = self.moves[-1][2]
            self.moves = self.moves[0:len(self.moves) - 1]

    def check_events(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.animation.sprites = [
                        pygame.transform.scale(sprite_manager.get(f"sprites/jaba/s0{index}"), (50, 50))
                        for index in range(0, 3)
                    ]
                    self.turning_side = 0
                if event.key == pygame.K_w:
                    self.animation.sprites = [
                        pygame.transform.scale(sprite_manager.get(f"sprites/jaba/f1{index}"), (50, 50))
                        for index in range(0, 3)]
                    self.turning_side = 1
                if event.key == pygame.K_a:
                    self.animation.sprites = [
                        pygame.transform.scale(sprite_manager.get(f"sprites/jaba/f0{index}"), (50, 50))
                        for index in range(0, 3)]
                    self.turning_side = 2
                if event.key == pygame.K_s:
                    self.animation.sprites = [
                        pygame.transform.scale(sprite_manager.get(f"sprites/jaba/b0{index}"), (50, 50))
                        for index in range(0, 3)]
                    self.turning_side = 3
                if event.key == pygame.K_z:
                    self.status_cancel = True

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a]:
                    self.turning_side = -1
                if event.key == pygame.K_z:
                    self.status_cancel = False

    def draw(self, screen: pygame.surface.Surface):
        self.animation.update()
        self.animation.draw(screen)
