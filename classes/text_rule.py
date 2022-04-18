class TextRule:
    def __init__(self, text, objects, prefix, infix):
        self.text_rule = text
        self.objects_in_rule = objects
        self.prefix = [prefix]
        self.infix = [infix]

    def __copy__(self):
        copied_rule = TextRule(
            text=self.text_rule,
            objects=self.objects_in_rule,
            prefix=self.prefix,
            infix=self.infix
        )
        return copied_rule

    def check_fix(self, rule_object,  matrix):
        status_prefix = False
        status_infix = False
        if self.prefix is None:
            status_prefix = True
        else:
            for pref in self.prefix:
                if pref == 'lonely':
                    if len(matrix[rule_object.y][rule_object.x]) == 1:
                        status_prefix = True
        if self.infix is None:
            status_infix = True

        return status_infix and status_prefix

