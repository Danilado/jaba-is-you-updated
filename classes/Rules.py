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


class Deturn(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, screen):
        self.matrix = matrix
        self.rule_object = rule_object
        self.screen = screen
        self.rule_object.direction -= 1
        self.rule_object.status_of_rotate -= 1
        if self.rule_object.direction < 0:
            self.rule_object.direction = 3
        if self.rule_object.status_of_rotate < 0:
            self.rule_object.status_of_rotate = 3
        self.rule_object.animation = self.rule_object.animation_init()


class Turn(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, screen):
        self.matrix = matrix
        self.rule_object = rule_object
        self.screen = screen
        self.rule_object.direction += 1
        self.rule_object.status_of_rotate += 1
        if self.rule_object.direction > 3:
            self.rule_object.direction = 0
        if self.rule_object.status_of_rotate > 3:
            self.rule_object.status_of_rotate = 0
        self.rule_object.animation = self.rule_object.animation_init()


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

    def apply(self, matrix, rule_object, level_rules):
        self.matrix = matrix
        self.rule_object = rule_object
        self.level_rules = level_rules
        rand_dir = random.randint(0, 4)
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


class Shift(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, level_rules):
        self.matrix = matrix
        self.rule_object = rule_object
        self.level_rules = level_rules
        for object in self.matrix[self.rule_object.y][self.rule_object.x]:
            if object.get_index(self.matrix) != self.rule_object.get_index(self.matrix):
                if self.rule_object.direction == 0:
                    object.move_up(
                        self.matrix, self.level_rules, 'push')
                elif self.rule_object.direction == 1:
                    object.move_right(
                        self.matrix, self.level_rules, 'push')
                elif self.rule_object.direction == 2:
                    object.move_down(
                        self.matrix, self.level_rules, 'push')
                elif self.rule_object.direction == 3:
                    object.move_left(
                        self.matrix, self.level_rules, 'push')


class Tele(Rule):
    def __init__(self):
        ...

    def apply(self, matrix, rule_object, objects_for_tp):
        self.matrix = matrix
        self.rule_object = rule_object
        print(len(objects_for_tp))
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
                    self.matrix[object.y][object.x].pop(object.get_index(self.matrix))
            objects_for_tp.append(coord)
            objects_for_tp.append(first)

        else:
            coor_x = objects_for_tp[0][1]
            coor_y = objects_for_tp[0][0]
            second = []
            for object in self.matrix[self.rule_object.y][self.rule_object.x]:
                if object.get_index(self.matrix) != self.rule_object.get_index(self.matrix):
                    second.append(object)
                    self.matrix[object.y][object.x].pop(object.get_index(self.matrix))
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


broken = Broken()
deturn_rule = Deturn()
turn_rule = Turn()
you = You()
chill = Chill()
boom = Boom()
auto = Auto()
direction = Direction()
fall = Fall()
more = More()
shift = Shift()
tele = Tele()

