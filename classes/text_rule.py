class TextRule:
    def __init__(self, text, objects, prefix, infix):
        self.text_rule = text
        self.objects_in_rule = objects
        self.prefix = prefix
        self.infix = infix

    def __copy__(self):
        copied_rule = TextRule(
            text=self.text_rule,
            objects=self.objects_in_rule,
            prefix=self.prefix,
            infix=self.infix
        )
        return copied_rule
