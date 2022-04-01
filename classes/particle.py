"""Модуль класса партикла"""
from math import sin, cos
import os
from random import randint
from typing import Tuple, Union

import pygame

from global_types import COLOR, SURFACE
from elements.global_classes import sprite_manager


particle_sprites_cache = {}
preset_strategies = {}


class ParticleStrategy:
    """Класс стратегии движения партикла"""

    def __init__(self, x_dimensions: Tuple[int, int] = None, y_dimensions: Tuple[int, int] = None,
                 size: int = None, rotation: Tuple[int, int] = None, wobble: int = 0,
                 duration: int = None, loop: bool = False, randomize_start_values: bool = False):
        """Инициализация стратегии партикла

        :param x_dimensions: координаты x начала и конца движения партикла, defaults to None
        :type x_dimensions: Tuple[int, int], optional
        :param y_dimensions: координаты y начала и конца движения партикла, defaults to None
        :type y_dimensions: Tuple[int, int], optional
        :param size_args: размер партикла, defaults to None
        :type size: int, optional
        :param rotation: угол поворота спрайта партикла в начале и конце движения, defaults to None
        :type rotation: Tuple[int, int], optional
        :param wobble: кол-во пикселей смещения партикла в процессе движение, defaults to 0
        :type wobble: int, optional
        :param duration: Длина анимации в секундах, defaults to None
        :type duration: int, optional
        :param loop: зациклена ли анимация, defaults to False
        :type loop: bool, optional
        :param randomize_start_values: рандомизирует стартовые значения в пределах введённых, defaults to False
        :type randomize_start_values: bool, optional
        """
        try:
            self.duration = duration * 1000
            self.loop = loop
            self.wobble = wobble

            self.x_position = x_dimensions[0]
            self.x_start = x_dimensions[0]
            self.x_offset = x_dimensions[1] - self.x_start

            self.y_position = y_dimensions[0]
            self.y_start = y_dimensions[0]
            self.y_offset = y_dimensions[1] - self.y_start

            self.size = size

            self.angle = rotation[0]
            self.angle_start = rotation[0]
            self.angle_offset = rotation[1] - self.angle_start

            self.time_randomizer = 0

            if randomize_start_values:
                self.x_position = randint(min(x_dimensions[0], x_dimensions[1]), max(
                    x_dimensions[0], x_dimensions[1]))
                self.y_position = randint(min(y_dimensions[0], y_dimensions[1]), max(
                    y_dimensions[0], y_dimensions[1]))
                self.angle = randint(
                    min(rotation[0], rotation[1]), max(rotation[0], rotation[1]))
                self.time_randomizer = randint(0, self.duration)

            self.start_timestamp = pygame.time.get_ticks()
        except IndexError or TypeError:
            print(x_dimensions, y_dimensions, rotation, duration, loop)
            print('^ В создание стратегии партикла переданы неправильные аргументы ^')

    def update_values(self):
        timestamp = pygame.time.get_ticks()
        time_position = timestamp + self.time_randomizer - self.start_timestamp
        if time_position > self.duration:
            if self.loop:
                self.start_timestamp = timestamp + self.time_randomizer
                self.x_position = self.x_start
                self.y_position = self.y_start
                self.angle = self.angle_start
                return self.update_values()
            return False
        time_offset = time_position / self.duration

        self.x_position = self.x_start + self.x_offset * time_offset
        self.y_position = self.y_start + self.y_offset * time_offset

        if self.wobble:
            self.x_position += self.wobble * \
                cos((timestamp+self.time_randomizer)/1000)
            self.y_position += self.wobble * \
                sin((timestamp+self.time_randomizer)/1000)
        self.angle = self.angle_start + self.angle_offset * time_offset
        return True


class Particle:
    def __init__(self, screen: SURFACE, name: str = None, strategy: Union[ParticleStrategy, str] = None, color: COLOR = 'white'):
        self.screen = screen
        self.sprite_name = name
        self.color = color

        if strategy not in preset_strategies:
            self.strategy = strategy

        if f'{self.sprite_name}_{self.color}' not in particle_sprites_cache:
            self.initialize_sprites()

        self.sprites = particle_sprites_cache[f'{self.sprite_name}_{self.color}']

        self.sprites_count = len(self.sprites)
        self.sprite_index = 0
        self.animation_timestamp = pygame.time.get_ticks()

    def initialize_sprites(self):
        path = os.path.join('./', 'sprites', self.sprite_name)
        states = [sprite_manager.get(os.path.join(
            path, name), color=self.color) for name in os.listdir(path)]
        particle_sprites_cache[f'{self.sprite_name}_{self.color}'] = states

    def update(self):
        if self.strategy.update_values():
            if pygame.time.get_ticks() - self.animation_timestamp >= 200:
                self.sprite_index += 1
                self.sprite_index %= self.sprites_count
                self.animation_timestamp = pygame.time.get_ticks()

            return True
        else:
            return False

    def draw(self, screen):
        if self.update():
            screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], int(self.strategy.angle)),
                        (self.strategy.x_position, self.strategy.y_position))
