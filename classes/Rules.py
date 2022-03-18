import abc
from asyncio import events
import random

from copy import copy
from typing import List


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
        self.rule_object.direction += 1
        self.rule_object.status_of_rotate += 1
        if self.rule_object.direction > 3:
            self.rule_object.direction = 0
        if self.rule_object.status_of_rotate > 3:
            self.rule_object.status_of_rotate = 0


class You(Rule):
    def apply(self, matrix, rule_object, events, level_rules, *_, **__):
        self.events = events
        self.level_rules = level_rules
        self.matrix = matrix
        self.rule_object = rule_object
        print(rule_object.is_safe)
        self.rule_object.check_events(self.events)
        self.rule_object.move(self.matrix, self.level_rules)
        print(rule_object.is_safe)


class Chill(Rule):
    def apply(self, matrix, rule_object, *_, **__):
        self.matrix = matrix
        self.rule_object = rule_object
        rand_dir = random.randint(0, 5)
        if rand_dir == 0:
            self.rule_object.move_up(
                self.matrix, self.level_rules)
        elif rand_dir == 1:
            self.rule_object.move_right(
                self.matrix, self.level_rules)
        elif rand_dir == 2:
            self.rule_object.move_down(
                self.matrix, self.level_rules)
        elif rand_dir == 3:
            self.rule_object.move_left(
                self.matrix, self.level_rules)


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
            self.rule_object.move_up(
                self.matrix, self.level_rules)
        elif self.rule_object.direction == 1:
            self.rule_object.move_right(
                self.matrix, self.level_rules)
        elif self.rule_object.direction == 2:
            self.rule_object.move_down(
                self.matrix, self.level_rules)
        elif self.rule_object.direction == 3:
            self.rule_object.move_left(
                self.matrix, self.level_rules)


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
        while self.rule_object.move_down(self.matrix, self.level_rules):
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
            'chill': Chill(),
            'boom': Boom(),
            'auto': Auto(),
            'direction': Direction(),
            'fall': Fall(),
            'more': More(),
        }

    def update_lists(self, matrix, events, level_rules):
        self.matrix = matrix
        self.events = events
        self.rules = level_rules

    def update_object(self, object):
        self.object = object

    def process(self, rule) -> bool:
        if rule.split()[-1] not in self.dictionary:
            return False

        self.dictionary[rule.split()[-1]].apply(matrix=self.matrix,
                                                rule_object=self.object,
                                                events=self.events,
                                                level_rules=self.rules)
        return True


# exports
processor = RuleProcessor()
