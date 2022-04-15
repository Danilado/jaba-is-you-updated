from dataclasses import dataclass
from typing import List

from classes.objects import Object


@dataclass
class TextRule:
    text_rule: str
    objects_in_rule: List[Object]

    def __copy__(self):
        copied_rule = TextRule(
            text_rule=self.text_rule,
            objects_in_rule=self.objects_in_rule
        )
        return copied_rule
