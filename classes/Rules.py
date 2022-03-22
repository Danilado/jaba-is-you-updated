import abc
from asyncio import events
from operator import le
import random

from copy import copy
from typing import List
from classes.state import State
from classes.game_state import GameState


class Rule(abc.ABC):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object):
        ...


class Broken(Rule):
    def apply(self, matrix, rule_object, rules, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        self.rules = rules
        self.object_name = self.rule_object.name
        for sec_rule in self.level_rules:
            if f'{self.object_name}' in sec_rule.text_rule and \
                    sec_rule.text_rule != f'{self.object_name} is broken':
                self.level_rules.remove(sec_rule)


class Deturn(Rule):
    def apply(self, matrix, rule_object, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        self.rule_object.direction -= 1
        self.rule_object.status_of_rotate -= 1
        if self.rule_object.direction < 0:
            self.rule_object.direction = 3
        if self.rule_object.status_of_rotate < 0:
            self.rule_object.status_of_rotate = 3
        self.rule_object.animation = self.rule_object.animation_init()


class Turn(Rule):
    def apply(self, matrix, rule_object, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        self.rule_object.direction += 1
        self.rule_object.status_of_rotate += 1
        if self.rule_object.direction > 3:
            self.rule_object.direction = 0
        if self.rule_object.status_of_rotate > 3:
            self.rule_object.status_of_rotate = 0
        self.rule_object.animation = self.rule_object.animation_init()


class You(Rule):
    def apply(self, matrix, rule_object, events, level_rules, level_processor, *_, **__):
        self.events = events
        self.level_rules = level_rules
        self.matrix = matrix
        self.rule_object = rule_object
        self.rule_object.check_events(self.events)
        self.rule_object.move(self.matrix, self.level_rules, level_processor)


class Is_3d(Rule):
    def apply(self, matrix, rule_object, events, level_rules, level_processor, *_, **__):
        self.events = events
        self.level_rules = level_rules
        self.matrix = matrix
        self.rule_object = rule_object
        self.rule_object.check_events(self.events)
        self.rule_object.move(self.matrix, self.level_rules, level_processor)


class Chill(Rule):
    def apply(self, matrix, rule_object, level_rules, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        self.level_rules = level_rules
        rand_dir = random.randint(0, 4)
        if rand_dir == 0:
            self.rule_object.motion(0, -1, self.matrix, self.level_rules)
        elif rand_dir == 1:
            self.rule_object.motion(1, 0, self.matrix, self.level_rules)
        elif rand_dir == 2:
            self.rule_object.motion(0, 1, self.matrix, self.level_rules)
        elif rand_dir == 3:
            self.rule_object.motion(-1, 0, self.matrix, self.level_rules)


class Boom(Rule):
    def apply(self, matrix, rule_object, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        self.matrix[self.rule_object.y][self.rule_object.x].clear()


class Auto(Rule):
    def apply(self, matrix, rule_object, level_rules, *_, **__):
        self.level_rules = level_rules
        self.matrix = matrix
        self.rule_object = rule_object
        if self.rule_object.direction == 0:
            self.rule_object.motion(0, -1, self.matrix, self.level_rules)
        elif self.rule_object.direction == 1:
            self.rule_object.motion(1, 0, self.matrix, self.level_rules)
        elif self.rule_object.direction == 2:
            self.rule_object.motion(0, 1, self.matrix, self.level_rules)
        elif self.rule_object.direction == 3:
            self.rule_object.motion(-1, 0, self.matrix, self.level_rules)


class Move(Rule):
    def apply(self, matrix, rule_object, level_rules, *_, **__):
        self.level_rules = level_rules
        self.matrix = matrix
        self.rule_object = rule_object
        if self.rule_object.direction == 0:
            if not self.rule_object.motion(0, -1, self.matrix, self.level_rules):
                self.rule_object.direction = 2
                self.rule_object.motion(0, 1, self.matrix, self.level_rules)
        elif self.rule_object.direction == 1:
            if not self.rule_object.motion(1, 0, self.matrix, self.level_rules):
                self.rule_object.direction = 3
                self.rule_object.motion(-1, 0, self.matrix, self.level_rules)
        elif self.rule_object.direction == 2:
            if not self.rule_object.motion(0, 1, self.matrix, self.level_rules):
                self.rule_object.direction = 0
                self.rule_object.motion(0, -1, self.matrix, self.level_rules)
        elif self.rule_object.direction == 3:
            if not self.rule_object.motion(-1, 0, self.matrix, self.level_rules):
                self.rule_object.direction = 1
                self.rule_object.motion(1, 0, self.matrix, self.level_rules)


class Direction(Rule):
    def apply(self, matrix, rule_object, direction, *_, **__):
        self.direction = direction
        self.matrix = matrix
        self.rule_object = rule_object

        if self.direction == 'up':
            self.rule_object.direction = 0
            self.rule_object.status_of_rotate = 1

        elif self.direction == 'right':
            self.rule_object.direction = 1
            self.rule_object.status_of_rotate = 0

        elif self.direction == 'down':
            self.rule_object.direction = 2
            self.rule_object.status_of_rotate = 3

        elif self.direction == 'left':
            self.rule_object.direction = 3
            self.rule_object.status_of_rotate = 2


class Fall(Rule):
    def apply(self, matrix, rule_object, level_rules, *_, **__):
        self.level_rules = level_rules
        self.matrix = matrix
        self.rule_object = rule_object
        while self.rule_object.motion(0, 1, self.matrix, self.level_rules):
            ...


class More(Rule):
    def apply(self, matrix, rule_object, level_rules, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        self.level_rules = level_rules

        if self.rule_object.y < len(self.matrix) - 1:
            if not self.matrix[self.rule_object.y + 1][self.rule_object.x]:
                new_object = copy(self.rule_object)
                new_object.y += 1
                new_object.animation = new_object.animation_init()
                self.matrix[
                    self.rule_object.y + 1][
                    self.rule_object.x].append(new_object)

        if self.rule_object.x < len(self.matrix[self.rule_object.y]) - 1:
            if not self.matrix[self.rule_object.y][self.rule_object.x + 1]:
                new_object = copy(self.rule_object)
                new_object.x += 1
                new_object.animation = new_object.animation_init()
                self.matrix[
                    self.rule_object.y][
                    self.rule_object.x + 1].append(new_object)

        if self.rule_object.x > 0:
            if not self.matrix[self.rule_object.y][self.rule_object.x - 1]:
                new_object = copy(self.rule_object)
                new_object.x -= 1
                new_object.animation = new_object.animation_init()
                self.matrix[
                    self.rule_object.y][
                    self.rule_object.x - 1].append(new_object)

        if self.rule_object.y > 0:
            if not self.matrix[self.rule_object.y - 1][self.rule_object.x]:
                new_object = copy(self.rule_object)
                new_object.y -= 1
                new_object.animation = new_object.animation_init()
                self.matrix[
                    self.rule_object.y - 1][
                    self.rule_object.x].append(new_object)


class Shift(Rule):
    def apply(self, matrix, rule_object, level_rules, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        self.level_rules = level_rules
        for object in self.matrix[self.rule_object.y][self.rule_object.x]:
            if object.get_index(self.matrix) != self.rule_object.get_index(self.matrix):
                if self.rule_object.direction == 0:
                    object.motion(0, -1, self.matrix, self.level_rules, 'push')
                elif self.rule_object.direction == 1:
                    object.motion(1, 0, self.matrix, self.level_rules, 'push')
                elif self.rule_object.direction == 2:
                    object.motion(0, 1, self.matrix, self.level_rules, 'push')
                elif self.rule_object.direction == 3:
                    object.motion(-1, 0, self.matrix, self.level_rules, 'push')


class Tele(Rule):
    def apply(self, matrix, rule_object, objects_for_tp, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        if len(objects_for_tp) == 1:
            if objects_for_tp[0] == 'skip':
                objects_for_tp[0] = 'skip again'
            elif objects_for_tp[0] == 'skip again':
                objects_for_tp = []
        elif len(objects_for_tp) == 0:
            coord = [self.rule_object.y, self.rule_object.x]
            first = []
            for object in self.matrix[self.rule_object.y][self.rule_object.x]:
                if object.get_index(self.matrix) != self.rule_object.get_index(self.matrix):
                    first.append(object)
                    self.matrix[object.y][object.x].pop(
                        object.get_index(self.matrix))
            objects_for_tp.append(coord)
            objects_for_tp.append(first)

        else:
            coor_x = objects_for_tp[0][1]
            coor_y = objects_for_tp[0][0]
            second = []
            for object in self.matrix[self.rule_object.y][self.rule_object.x]:
                if object.get_index(self.matrix) != self.rule_object.get_index(self.matrix):
                    second.append(object)
                    self.matrix[object.y][object.x].pop(
                        object.get_index(self.matrix))
            objects_for_tp.append(second)
            for object in objects_for_tp[1]:
                object.y = self.rule_object.y
                object.x = self.rule_object.x
                object.ypx = object.y * 50
                object.xpx = object.x * 50
                object.animation = object.animation_init()
                matrix[self.rule_object.y][self.rule_object.x].append(object)
            for object in objects_for_tp[2]:
                object.y = coor_y
                object.x = coor_x
                object.ypx = coor_y * 50
                object.xpx = coor_x * 50
                object.animation = object.animation_init()
                matrix[coor_y][coor_x].append(object)
            objects_for_tp = ['skip']
        return objects_for_tp


class RuleProcessor:
    def __init__(self):
        self.matrix = None
        self.object = None
        self.events = None
        self.rules = None

        self.dictionary = {
            'broken': Broken(),
            'deturn': Deturn(),
            'you': You(),
            '3d': Is_3d(),
            'chill': Chill(),
            'boom': Boom(),
            'auto': Auto(),
            'direction': Direction(),
            'fall': Fall(),
            'more': More(),
            'turn': Turn(),
            'deturn': Deturn(),
            'shift': Shift(),
            'tele': Tele(),
            'move': Move()
        }

    def update_lists(self, level_processor, matrix, events):
        self.level_processor = level_processor
        self.matrix = matrix
        self.events = events
        self.rules = level_processor.level_rules
        self.objects_for_tp = level_processor.objects_for_tp

    def update_object(self, object):
        self.object = object

    def process(self, rule) -> bool:
        if rule.split()[-1] not in self.dictionary:
            return False

        self.dictionary[rule.split()[-1]].apply(matrix=self.matrix,
                                                rule_object=self.object,
                                                events=self.events,
                                                level_rules=self.rules,
                                                objects_for_tp=self.objects_for_tp,
                                                level_processor=self.level_processor)
        return True


# exports
processor = RuleProcessor()
