import abc
import random

from copy import copy


class Rule(abc.ABC):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object):
        ...


class Broken(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, rules):
        self.matrix = matrix
        self.rule_object = rule_object
        self.rules = rules
        self.object_name = self.rule_object.name
        for sec_rule in self.level_rules:
            if f'{self.object_name}' in sec_rule.text_rule and \
                    sec_rule.text_rule != f'{self.object_name} is broken':
                self.level_rules.remove(sec_rule)


class Return(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object):
        self.matrix = matrix
        self.rule_object = rule_object
        self.rule_object.direction += 1
        self.rule_object.status_of_rotate += 1
        if self.rule_object.direction > 3:
            self.rule_object.direction = 0
        if self.rule_object.status_of_rotate > 3:
            self.rule_object.status_of_rotate = 0


class You(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, events, level_rules):
        self.events = events
        self.level_rules = level_rules
        self.matrix = matrix
        self.rule_object = rule_object
        self.rule_object.check_events(self.events)
        self.rule_object.move(self.matrix, self.level_rules)


class Chill(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object):
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
    def __init__(self):
        ...

    def apply(self, matrix, rule_object):
        self.matrix = matrix
        self.rule_object = rule_object
        self.matrix[self.rule_object.y][self.rule_object.x].clear()


class Auto(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, level_rules):
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
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, direction):
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
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, level_rules):
        self.level_rules = level_rules
        self.matrix = matrix
        self.rule_object = rule_object
        while self.rule_object.move_down(self.matrix, self.level_rules):
            ...


class More(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, level_rules):
        self.matrix = matrix
        self.rule_object = rule_object
        self.level_rules = level_rules

        if self.rule_object.y < len(self.matrix) - 1:
            if not self.matrix[self.rule_object.y + 1][self.rule_object.x]:
                self.matrix[
                    self.rule_object.y + 1][
                    self.rule_object.x].append(copy(self.rule_object))

        if self.rule_object.x < len(self.matrix[self.rule_object.y]) - 1:
            if not self.matrix[self.rule_object.y][self.rule_object.x + 1]:
                self.matrix[
                    self.rule_object.y][
                    self.rule_object.x + 1].append(copy(self.rule_object))

        if self.rule_object.x > 0:
            if not self.matrix[self.rule_object.y][self.rule_object.x - 1]:
                self.matrix[
                    self.rule_object.y][
                    self.rule_object.x - 1].append(copy(self.rule_object))

        if self.rule_object.y > 0:
            if not self.matrix[self.rule_object.y - 1][self.rule_object.x]:
                self.matrix[
                    self.rule_object.y - 1][
                    self.rule_object.x].append(copy(self.rule_object))


broken = Broken()
return_rule = Return()
you = You()
chill = Chill()
boom = Boom()
auto = Auto()
direction = Direction()
fall = Fall()
more = More()
