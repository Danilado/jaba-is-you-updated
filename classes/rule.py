from dataclasses import dataclass
from typing import List

from classes.objects import Object


@dataclass
class Rule:
    text_rule: str
    objects_in_rule: List[Object]
