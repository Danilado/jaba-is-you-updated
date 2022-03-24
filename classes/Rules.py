import pygame
import random

from copy import copy


class Broken:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        object_name = rule_object.name
        for sec_rule in level_rules:
            if f'{object_name}' in sec_rule.text_rule and \
                    sec_rule.text_rule != f'{object_name} is broken':
                level_rules.remove(sec_rule)


class Deturn:
    @staticmethod
    def apply(matrix, rule_object, *_, **__):
        matrix[rule_object.y][rule_object.x].pop(
            rule_object.get_index(matrix))
        rule_object.direction -= 1
        rule_object.status_of_rotate -= 1
        if rule_object.direction < 0:
            rule_object.direction = 3
        if rule_object.status_of_rotate < 0:
            rule_object.status_of_rotate = 3
        rule_object.animation = rule_object.animation_init()
        matrix[rule_object.y][rule_object.x].append(
            copy(rule_object))


class Text:
    @staticmethod
    def apply(matrix, rule_object, *_, **__):
        matrix[rule_object.y][rule_object.x].pop(
            rule_object.get_index(matrix))
        rule_object.is_text = True
        rule_object.animation = rule_object.animation_init()
        matrix[rule_object.y][rule_object.x].append(
            copy(rule_object))


class Turn:
    @staticmethod
    def apply(matrix, rule_object, *_, **__):
        matrix[rule_object.y][rule_object.x].pop(
            rule_object.get_index(matrix))
        rule_object.direction += 1
        rule_object.status_of_rotate += 1
        if rule_object.direction > 3:
            rule_object.direction = 0
        if rule_object.status_of_rotate > 3:
            rule_object.status_of_rotate = 0
        rule_object.animation = rule_object.animation_init()
        matrix[rule_object.y][rule_object.x].append(
            copy(rule_object))


class You:
    @staticmethod
    def apply(matrix, rule_object, events, level_rules, level_processor, *_, **__):
        rule_object.check_events(events, 1)
        rule_object.move(matrix, level_rules, level_processor)


class You2:
    @staticmethod
    def apply(matrix, rule_object, events, level_rules, level_processor, *_, **__):
        rule_object.check_events(events, 2)
        rule_object.move(matrix, level_rules, level_processor)


class Is_3d:
    @staticmethod
    def apply(matrix, rule_object, events, level_rules, level_processor, num_obj_3d, *_, **__):
        if rule_object.num_3d == num_obj_3d:
            rule_object.check_events(events, 1)
            if events[0].key == pygame.K_s:
                num_obj_3d += 1
            level_processor.num_obj_3d = num_obj_3d
            rule_object.move(matrix, level_rules, level_processor)


class Chill:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        rand_dir = random.randint(0, 4)
        if rand_dir == 0:
            rule_object.motion(0, -1, matrix, level_rules)
        elif rand_dir == 1:
            rule_object.motion(1, 0, matrix, level_rules)
        elif rand_dir == 2:
            rule_object.motion(0, 1, matrix, level_rules)
        elif rand_dir == 3:
            rule_object.motion(-1, 0, matrix, level_rules)


class Boom:
    @staticmethod
    def apply(matrix, rule_object, *_, **__):
        matrix[rule_object.y][rule_object.x].clear()


class Auto:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        if rule_object.direction == 0:
            rule_object.motion(0, -1, matrix, level_rules)
        elif rule_object.direction == 1:
            rule_object.motion(1, 0, matrix, level_rules)
        elif rule_object.direction == 2:
            rule_object.motion(0, 1, matrix, level_rules)
        elif rule_object.direction == 3:
            rule_object.motion(-1, 0, matrix, level_rules)


class Move:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        if rule_object.direction == 0:
            if not rule_object.motion(0, -1, matrix, level_rules):
                rule_object.direction = 2
                rule_object.motion(0, 1, matrix, level_rules)
        elif rule_object.direction == 1:
            if not rule_object.motion(1, 0, matrix, level_rules):
                rule_object.direction = 3
                rule_object.motion(-1, 0, matrix, level_rules)
        elif rule_object.direction == 2:
            if not rule_object.motion(0, 1, matrix, level_rules):
                rule_object.direction = 0
                rule_object.motion(0, -1, matrix, level_rules)
        elif rule_object.direction == 3:
            if not rule_object.motion(-1, 0, matrix, level_rules):
                rule_object.direction = 1
                rule_object.motion(1, 0, matrix, level_rules)


class Direction:
    @staticmethod
    def apply(rule_object, direction, *_, **__):
        if direction == 'up':
            rule_object.direction = 0
            rule_object.status_of_rotate = 1

        elif direction == 'right':
            rule_object.direction = 1
            rule_object.status_of_rotate = 0

        elif direction == 'down':
            rule_object.direction = 2
            rule_object.status_of_rotate = 3

        elif direction == 'left':
            rule_object.direction = 3
            rule_object.status_of_rotate = 2


class Fall:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        # FIXME by Gospodin
        # Падающий объект не толкает на пути другие
        while rule_object.motion(0, 1, matrix, level_rules):
            ...


class More:
    @staticmethod
    def apply(matrix, rule_object, *_, **__):
        if rule_object.y < len(matrix) - 1:
            if not matrix[rule_object.y + 1][rule_object.x]:
                new_object = copy(rule_object)
                new_object.y += 1
                new_object.animation = new_object.animation_init()
                matrix[
                    rule_object.y + 1][
                    rule_object.x].append(new_object)

        if rule_object.x < len(matrix[rule_object.y]) - 1:
            if not matrix[rule_object.y][rule_object.x + 1]:
                new_object = copy(rule_object)
                new_object.x += 1
                new_object.animation = new_object.animation_init()
                matrix[
                    rule_object.y][
                    rule_object.x + 1].append(new_object)

        if rule_object.x > 0:
            if not matrix[rule_object.y][rule_object.x - 1]:
                new_object = copy(rule_object)
                new_object.x -= 1
                new_object.animation = new_object.animation_init()
                matrix[
                    rule_object.y][
                    rule_object.x - 1].append(new_object)

        if rule_object.y > 0:
            if not matrix[rule_object.y - 1][rule_object.x]:
                new_object = copy(rule_object)
                new_object.y -= 1
                new_object.animation = new_object.animation_init()
                matrix[
                    rule_object.y - 1][
                    rule_object.x].append(new_object)


class Shift:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        for object in matrix[rule_object.y][rule_object.x]:
            if object.name != rule_object.name:
                if rule_object.direction == 0:
                    object.motion(0, -1, matrix, level_rules, 'push')
                elif rule_object.direction == 1:
                    object.motion(1, 0, matrix, level_rules, 'push')
                elif rule_object.direction == 2:
                    object.motion(0, 1, matrix, level_rules, 'push')
                elif rule_object.direction == 3:
                    object.motion(-1, 0, matrix, level_rules, 'push')


class Tele:
    @staticmethod
    def apply(matrix, rule_object, objects_for_tp, *_, **__):
        if len(objects_for_tp) == 1:
            if objects_for_tp[0] == 'skip':
                objects_for_tp[0] = 'skip again'
            elif objects_for_tp[0] == 'skip again':
                objects_for_tp = []
        elif len(objects_for_tp) == 0:
            coord = [rule_object.y, rule_object.x]
            first = []
            for object in matrix[rule_object.y][rule_object.x]:
                if object.get_index(matrix) != rule_object.get_index(matrix):
                    first.append(object)
                    matrix[object.y][object.x].pop(
                        object.get_index(matrix))
            objects_for_tp.append(coord)
            objects_for_tp.append(first)

        else:
            coor_x = objects_for_tp[0][1]
            coor_y = objects_for_tp[0][0]
            second = []
            for object in matrix[rule_object.y][rule_object.x]:
                if object.get_index(matrix) != rule_object.get_index(matrix):
                    second.append(object)
                    matrix[object.y][object.x].pop(
                        object.get_index(matrix))
            objects_for_tp.append(second)
            for object in objects_for_tp[1]:
                object.y = rule_object.y
                object.x = rule_object.x
                object.ypx = object.y * 50
                object.xpx = object.x * 50
                object.animation = object.animation_init()
                matrix[rule_object.y][rule_object.x].append(object)
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
        self.level_processor = None

        self.dictionary = {
            'broken': Broken(),
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
            'move': Move(),
            'text': Text(),
            'you2': You2(),
        }

    def update_lists(self, level_processor, matrix, events):
        self.level_processor = level_processor
        self.matrix = matrix
        self.events = events
        self.rules = level_processor.level_rules
        self.objects_for_tp = level_processor.objects_for_tp
        self.num_obj_3d = level_processor.num_obj_3d

    def update_object(self, rule_object):
        self.object = rule_object

    def process(self, rule) -> bool:
        if rule.split()[-1] not in self.dictionary:
            return False
        try:
            self.dictionary[rule.split()[-1]].apply(matrix=self.matrix,
                                                    rule_object=self.object,
                                                    events=self.events,
                                                    level_rules=self.rules,
                                                    objects_for_tp=self.objects_for_tp,
                                                    num_obj_3d=self.num_obj_3d,
                                                    level_processor=self.level_processor)
        # except IndexError:
         #   print(
        #        f'!!! IndexError appeared somewhere in {rule.split()[-1]} rule')
        except RecursionError:
            print(
                f'!!! RecursionError appeared somewhere in {rule.split()[-1]} rule')
        return True


# exports
processor = RuleProcessor()
