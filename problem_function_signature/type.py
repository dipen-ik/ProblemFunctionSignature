import re
from typing import Tuple, Optional

import itertools


_primitive_type_names = ['int32', 'int64', 'bool', 'char', 'str', 'float']
_composite_type_names = ['list', 'SinglyLinkedListNode']


def all_type_names():
    return itertools.chain(_primitive_type_names, _composite_type_names)


def primitive_type_names():
    return itertools.chain(_primitive_type_names)


def composite_type_names():
    return itertools.chain(_composite_type_names)


class Type:
    """Type of function argument or return value. Intended to be immutable (not enforced)."""

    def __init__(self, name: str, element_type=None):
        self.name = name
        self.element_type = element_type  # Type of the element of a composite type, e.g. a collection.
        self.primitive = element_type is None
        self.custom = name == 'SinglyLinkedListNode'
        # "Custom" types are different from the others ("built-in") in that we declare every custom type
        # as a class or struct in code stubs (head.txt) in all languages.

        if self.primitive:
            assert name in _primitive_type_names
            assert element_type is None
            assert not self.custom
        else:
            assert name in _composite_type_names
            assert element_type is not None

    def __eq__(self, other):
        if not hasattr(other, 'name') or self.name != other.name:
            return False
        if not hasattr(other, 'element_type') or self.element_type != other.element_type:
            return False
        return True

    def __hash__(self):
        return hash((self.name, self.element_type))

    def __str__(self):
        if self.primitive:
            return self.name
        else:
            return f'{self.name}_{self.element_type}'

    def contains_list_of_primitive(self):
        """Returns whether self is a list of primitive values OR contains one.
           If it is or does, second returned value is the (primitive) type of the list elements."""
        if self.primitive:
            return False, None
        elif self.element_type.primitive:
            return self.name == 'list', self.element_type
        else:
            return self.element_type.contains_list_of_primitive()

    def is_list_of_lists(self):
        if self.primitive:
            return False
        return self.name == 'list' and self.element_type.name == 'list'

    def to_dict(self):
        return {
            'name': self.name,
            'element_type': self.element_type.to_dict() if self.element_type else None,
            'primitive': self.primitive,
            'custom': self.custom,
        }


def validate_type(data_type: str) -> Tuple[Optional[Type], bool]:
    """Checks if given string is a valid type and returns the Type instance.
    Recursively validates/creates subtypes for composite types.
    If validation failed, returns False as the second value."""
    if data_type in primitive_type_names():
        return Type(data_type), True

    for composite_type in composite_type_names():
        pattern = rf'(^{composite_type})\[(.+)\]'
        regex_string = re.fullmatch(pattern, data_type)
        if regex_string is not None:
            sub_type = regex_string.groups()[1].strip()
            result = validate_type(sub_type)
            if result[1]:
                return Type(composite_type, result[0]), True
            else:
                return None, False

    return None, False
