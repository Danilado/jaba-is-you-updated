from settings import DEBUG
from typing import List, Tuple, Literal

import pygame

import settings
from classes.animation import Animation
from elements.global_classes import sprite_manager
from global_types import SURFACE


class Player:
    """
    Класс игрока

    :ivar x: Абсцисса изначального положения
    :ivar y: Ордината изначального положения
    :ivar moves: История движений
    :ivar status_of_rotate: Копия направления движения, изменять вне класса не рекомендуется
    :ivar turning_side: Текущее направление движения, 0 - вправо, 1 - вверх, 2 - влево, 3 - вниз
    :ivar status_cancel: Отменять ли последнее движение?
    """

    def __init__(self, x, y, animation_sync: bool = True):
        """
        Инициализация игрока

        :param x: Абсцисса изначального положения
        :param y: Ордината изначального положения
        """
        self._x = x
        self._y = y
        self.moves: List[Tuple[int, int, int]] = []

        self.status_of_rotate: Literal[0, 1, 2, 3] = 0  # TODO: Use enum, and make field private

        self.status_of_rotate = 0  # 0 - вправо, 1 - вверх, 2 - влево, 3 - вниз
        self.turning_side = -1
        self.status_cancel: bool = False
        self.animation = Animation(
                [pygame.transform.scale(sprite_manager.get(f"sprites/jaba/r0{index}"), (50, 50))
                 for index in range(0, 3)],
                200, (self.x, self.y), animation_sync
            )

    @property
    def animation_sync(self) -> bool:
        return self.animation.synchronize

    @animation_sync.setter
    def animation_sync(self, value: bool):
        self.animation.synchronize = value

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
        """Метод движения персонажа"""
        if self.turning_side == 0:
            self.move_right()
        if self.turning_side == 1:
            self.move_up()
        if self.turning_side == 2:
            self.move_left()
        if self.turning_side == 3:
            self.move_down()
        if DEBUG:
            print(self.turning_side, self.status_of_rotate)

    def cancel_move(self):
        """Отмена последнего движения, если установлен status_cancel"""
        if self.status_cancel:
            self.move_back()

    def move_up(self):
        """Метод движения персонажа вверх"""
        if self.y > 0:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 1
            self.y -= 1

    def move_down(self):
        """Метод движения персонажа вниз"""
        if self.y < settings.RESOLUTION[1] // 50 - 1:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 3
            self.y += 1

    def move_left(self):
        """Метод движения персонажа влево"""
        if self.x > 0:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 2
            self.x -= 1

    def move_right(self):
        """Метод движения персонажа вправо"""
        if self.x < settings.RESOLUTION[0] // 50 - 1:
            self.moves.append((self.x, self.y, self.status_of_rotate))
            self.status_of_rotate = 0
            self.x += 1

    def move_back(self):
        """Отмена последнего движения, в не зависимости от status_cancel"""
        if len(self.moves) != 0:
            self.x = self.moves[-1][0]
            self.y = self.moves[-1][1]
            self.status_of_rotate = self.moves[-1][2]
            self.moves = self.moves[:-1]

    def check_events(self, events: List[pygame.event.Event]):
        """Метод обработки событий"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.animation.sprites = [
                        pygame.transform.scale(sprite_manager.get(f"sprites/jaba/r0{index}"), (50, 50))
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
                        pygame.transform.scale(sprite_manager.get(f"sprites/jaba/l0{index}"), (50, 50))
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

    def draw(self, screen: SURFACE):
        """
        Метод отрисовки персонажа

        :param screen: Surface, на котором будет происходить отрисовка
        """
        self.animation.update()
        self.animation.draw(screen)
