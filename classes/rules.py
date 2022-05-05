import math
import random
from copy import copy

import pygame

from classes.text_rule import TextRule


class Broken:
    @staticmethod
    def apply(rule_object, level_rules, *_, **__):
        object_name = rule_object.name
        for sec_rule in level_rules:
            if f'{object_name}' == sec_rule.text_rule.split()[-3] or f'{object_name}' == sec_rule.text_rule.split()[-4] \
                    and sec_rule.text_rule != f'{object_name} is broken':
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
    def __init__(self, num: int = 1):
        self.num: int = num

    def apply(self, matrix, rule_object, events, level_rules, level_processor, *_, **__):
        rule_object.check_events(events, self.num)
        rule_object.move(matrix, level_rules, level_processor)


class Is3d:
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
    def apply(matrix, rule_object, level_rules, **__):
        boom_objects = []
        for object in matrix[rule_object.y][rule_object.x]:
            boom_objects.append(object)
            matrix[rule_object.y][rule_object.x].pop(object.get_index(matrix))
        for object in boom_objects:
            object.die(0, 0, matrix, level_rules)


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
        assert rule_object.animation is not None
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
        for level_object in matrix[rule_object.y][rule_object.x]:
            if level_object.name != rule_object.name and rule_object.can_iteract(level_rules, level_rules):
                if rule_object.direction == 0:
                    level_object.motion(0, -1, matrix, level_rules, 'push')
                elif rule_object.direction == 1:
                    level_object.motion(1, 0, matrix, level_rules, 'push')
                elif rule_object.direction == 2:
                    level_object.motion(0, 1, matrix, level_rules, 'push')
                elif rule_object.direction == 3:
                    level_object.motion(-1, 0, matrix, level_rules, 'push')


class Melt:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        for level_object in matrix[rule_object.y][rule_object.x]:
            if not level_object.check_melt(0, 0, matrix, level_rules, rule_object):
                level_object.die(0, 0, matrix, level_rules)


class Win:
    @staticmethod
    def apply(matrix, rule_object, level_rules, level_processor, *_, **__):
        for level_object in matrix[rule_object.y][rule_object.x]:
            rule_object.level_processor = level_processor
            level_object.level_processor = level_processor
            rule_object.check_win(level_rules, level_object, matrix)
            rule_object.check_win(level_rules, rule_object, matrix)
            level_object.check_win(level_rules, rule_object, matrix)


class Defeat:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        for rule in level_rules:
            if f'{rule_object.name} is you' in rule.text_rule and not rule_object.is_text or rule_object.text(rule, 'is you'):
                if not rule_object.is_safe:
                    matrix[rule_object.y][rule_object.x].pop(rule_object.get_index(matrix))
                    rule_object.die(0, 0, matrix, level_rules)
                    return False
        for level_object in matrix[rule_object.y][rule_object.x]:
            if not level_object.check_defeat(0, 0, matrix, level_rules, rule_object):
                level_object.die(0, 0, matrix, level_rules)


class ShutOpen:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        for rule in level_rules:
            if f'{rule_object.name} is open' in rule.text_rule and not rule_object.is_text:
                if not rule_object.is_safe and rule_object.can_interact(level_rules, level_rules):
                    matrix[rule_object.y][rule_object.x].pop(rule_object.get_index(matrix))
                    return False
        for level_object in matrix[rule_object.y][rule_object.x]:
            if rule_object.can_interact(level_object, level_rules):
                if not rule_object.check_shut_open(
                        0, 0, matrix, level_rules, level_object):
                    level_object.die(0, 0, matrix, level_rules)
                    rule_object.die(0, 0, matrix, level_rules)


class Sink:
    @staticmethod
    def apply(matrix, rule_object, level_rules, *_, **__):
        if len(matrix[rule_object.y][rule_object.x]) > 1:
            for level_object in matrix[rule_object.y][rule_object.x]:
                if rule_object.get_index(matrix) != level_object.get_index(matrix):
                    if not rule_object.check_sink(0, 0, matrix, level_rules, level_object):
                        level_object.die(0, 0, matrix, level_rules)
                        rule_object.die(0, 0, matrix, level_rules)


class Make:
    @staticmethod
    def apply(matrix, rule_object, rule_noun, *_, **__):
        status = True
        for check_object in matrix[rule_object.y][rule_object.x]:
            if check_object.name == rule_noun:
                status = False
        if status:
            matrix[rule_object.y][rule_object.x].pop(
                rule_object.get_index(matrix))
            new_object = copy(rule_object)
            new_object.name = rule_noun
            new_object.animation = new_object.animation_init()
            matrix[rule_object.y][rule_object.x].append(new_object)
            new_object = copy(rule_object)
            matrix[rule_object.y][rule_object.x].append(new_object)


class Write:
    @staticmethod
    def apply(matrix, rule_object, rule_noun, *_, **__):
        matrix[rule_object.y][rule_object.x].pop(rule_object.get_index(matrix))
        rule_object.name = rule_noun
        rule_object.is_text = True
        rule_object.animation = rule_object.animation_init()
        matrix[rule_object.y][rule_object.x].append(rule_object)


class Fear:
    def apply(self, matrix, rule_object, rule_noun, level_rules, **__):
        fear_top = False
        if rule_object.check_valid_range(0, -1):
            for level_object in matrix[rule_object.y - 1][rule_object.x]:
                if not level_object.is_text and level_object.name == rule_noun:
                    fear_top = True
        fear_bottom = False
        if rule_object.check_valid_range(0, 1):
            for level_object in matrix[rule_object.y + 1][rule_object.x]:
                if not level_object.is_text and level_object.name == rule_noun:
                    fear_bottom = True
        fear_left = False
        if rule_object.check_valid_range(-1, 0):
            for level_object in matrix[rule_object.y][rule_object.x - 1]:
                if not level_object.is_text and level_object.name == rule_noun:
                    fear_left = True
        fear_right = False
        if rule_object.check_valid_range(1, 0):
            for level_object in matrix[rule_object.y][rule_object.x + 1]:
                if not level_object.is_text and level_object.name == rule_noun:
                    fear_right = True
        turning_side = self.find_side_move(fear_top, fear_bottom, fear_left, fear_right, rule_object.turning_side)
        if turning_side == 0:
            rule_object.motion(1, 0, matrix, level_rules)
        elif turning_side == 1:
            rule_object.motion(0, -1, matrix, level_rules)
        elif turning_side == 2:
            rule_object.motion(-1, 0, matrix, level_rules)
        elif turning_side == 3:
            rule_object.motion(0, 1, matrix, level_rules)

    @staticmethod
    def find_side_move(fear_top, fear_bottom, fear_left, fear_right, side):
        if (fear_top and fear_bottom and not fear_left and not fear_right) or \
                (not fear_top and not fear_bottom and fear_left and fear_right):
            return side

        if (fear_top and not fear_left and not fear_right and not fear_bottom) or \
                (fear_top and not fear_bottom and fear_left and fear_right) or \
                (fear_top and fear_left and not fear_right and not fear_bottom and side == 2) or \
                (fear_top and not fear_left and fear_right and not fear_bottom and side == 0):
            return 3

        if (not fear_top and fear_left and not fear_right and not fear_bottom) or \
                (fear_top and fear_bottom and fear_left and not fear_right) or \
                (fear_left and fear_top and not fear_right and not fear_bottom and side == 1) or \
                (fear_left and not fear_top and not fear_right and fear_bottom and side == 3):
            return 0

        if (not fear_top and not fear_left and fear_right and not fear_bottom) or \
                (fear_top and fear_bottom and not fear_left and fear_right) or \
                (fear_right and fear_top and not fear_left and not fear_bottom and side == 1) or \
                (fear_right and not fear_top and not fear_left and fear_bottom and side == 3):
            return 2

        if (not fear_top and not fear_left and not fear_right and fear_bottom) or \
                (not fear_top and fear_bottom and fear_left and fear_right) or \
                (fear_bottom and fear_left and not fear_right and not fear_top and side == 2) or \
                (fear_bottom and not fear_left and fear_right and not fear_top and side == 0):
            return 1

        return -1


class Eat:
    @staticmethod
    def apply(matrix, rule_object, rule_noun, *_, **__):
        for level_object in matrix[rule_object.y][rule_object.x]:
            if level_object.name == rule_noun and not level_object.is_text:
                if rule_object.name != rule_noun:
                    matrix[level_object.y][level_object.x].pop(
                        level_object.get_index(matrix))
                else:
                    if level_object.get_index(matrix) != rule_object.get_index(matrix):
                        matrix[level_object.y][level_object.x].pop(
                            level_object.get_index(matrix))


class Follow:
    @staticmethod
    def apply(matrix, rule_object, rule_noun, **__):
        min_delta_y = 100
        min_delta_x = 100
        for i in matrix:
            for j in i:
                for level_object in j:
                    if level_object.name == rule_noun and not rule_object.is_text:
                        new_delta_x = rule_object.x - level_object.x
                        new_delta_y = rule_object.y - level_object.y
                        if (min_delta_x ** 2 + min_delta_y ** 2) ** 0.5 > (new_delta_x ** 2 + new_delta_y ** 2) ** 0.5:
                            min_delta_x = new_delta_x
                            min_delta_y = new_delta_y
        vector2 = math.atan2(min_delta_y, min_delta_x)
        angle = vector2 * (180.0 / math.pi)
        angle = 180 - angle
        if 315 <= angle < 360 or 0 <= angle < 45:
            rule_object.turning_side = 0
            rule_object.direction = 1
        elif 45 <= angle < 135:
            rule_object.turning_side = 1
            rule_object.direction = 0
        elif 225 <= angle < 315:
            rule_object.turning_side = 3
            rule_object.direction = 2
        elif 135 <= angle < 225:
            rule_object.turning_side = 2
            rule_object.direction = 3
        matrix[rule_object.y][rule_object.x].pop(rule_object.get_index(matrix))
        rule_object.animation = rule_object.animation_init()
        matrix[rule_object.y][rule_object.x].append(rule_object)


class Tele:
    @staticmethod
    def apply(matrix, rule_object, level_rules, **__):
        first_tp = rule_object
        status = False
        teleports = []
        x1 = first_tp.x
        y1 = first_tp.y
        for i, line in enumerate(matrix):
            for j, cell in enumerate(line):
                for second_object_tp in cell:
                    if not second_object_tp.is_text:
                        if second_object_tp.name == first_tp.name \
                                and (second_object_tp.x != first_tp.x or second_object_tp.y != first_tp.y) \
                                and len(matrix[i][j]) > 1:
                            status = True
                            teleports.append(copy(second_object_tp))
        if not status:
            return False
        second_tp = teleports[random.randint(0, len(teleports) - 1)]
        x2 = second_tp.x
        y2 = second_tp.y
        for objects in matrix[y1][x1]:
            if objects.name != first_tp.name and rule_object.can_iteract(objects, level_rules):
                matrix[y1][x1].pop(objects.get_index(matrix))
                objects.update_parameters(x2 - x1, y2 - y1, matrix)
        for objects in matrix[y2][x2]:
            if objects.name != second_tp.name and rule_object.can_iteract(objects, level_rules):
                matrix[y2][x2].pop(objects.get_index(matrix))
                objects.update_parameters(-(x2 - x1), -(y2 - y1), matrix)


class RuleProcessor:
    def __init__(self):
        self.matrix = None
        self.object = None
        self.events = None
        self.rules = None
        self.level_processor = None
        self.objects_for_tp = None
        self.num_obj_3d = None

        self.dictionary = {
            'broken': Broken(),
            'you': You(1),
            'you2': You(2),
            '3d': Is3d(),
            'chill': Chill(),
            'boom': Boom(),
            'auto': Auto(),
            'defeat': Defeat(),
            'direction': Direction(),
            'fall': Fall(),
            'more': More(),
            'turn': Turn(),
            'deturn': Deturn(),
            'shift': Shift(),
            'tele': Tele(),
            'move': Move(),
            'text': Text(),
            'melt': Melt(),
            'shut': ShutOpen(),
            'sink': Sink(),
            'win': Win(),
            'make': Make(),
            'write': Write(),
            'fear': Fear(),
            'eat': Eat(),
            'follow': Follow()
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

    def process(self, rule: TextRule) -> bool:
        text_rule = rule.text_rule
        status_rule = None
        if text_rule.split()[-1] in self.dictionary:
            status_rule = 'property'
        if text_rule.split()[-2] in self.dictionary:
            status_rule = 'verb'
        try:
            if status_rule == 'property':
                if rule.check_fix(self.object, self.matrix, self.rules):
                    self.dictionary[text_rule.split()[-1]].apply(matrix=self.matrix,
                                                            rule_object=self.object,
                                                            events=self.events,
                                                            level_rules=self.rules,
                                                            objects_for_tp=self.objects_for_tp,
                                                            num_obj_3d=self.num_obj_3d,
                                                            level_processor=self.level_processor)
            elif status_rule == 'verb':
                if rule.check_fix(self.object, self.matrix, self.rules):
                    self.dictionary[text_rule.split()[-2]].apply(matrix=self.matrix,
                                                            rule_object=self.object,
                                                            events=self.events,
                                                            level_rules=self.rules,
                                                            rule_noun=text_rule.split(
                                                            )[-1],
                                                            num_obj_3d=self.num_obj_3d,
                                                            level_processor=self.level_processor)

        except RecursionError:
            print(
                f'!!! RecursionError appeared somewhere in {rule.split()[-1]} rule')
        return True


# exports
processor = RuleProcessor()
