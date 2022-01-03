import re
from typing import NamedTuple, List, Tuple

from .type import Type, all_type_names, validate_type, composite_type_names

ALLOW_UPPERCASE_IN_NAMES = False


class Argument(NamedTuple):
    name: str
    type: Type


class Signature:
    def __init__(self, names_and_types: List[Tuple[str, Type]]):
        self.name = names_and_types[0][0]
        self.type = names_and_types[0][1]
        self.args = [Argument(i[0], i[1]) for i in names_and_types[1:]]


class ValidationException(Exception):
    pass


class InvalidNameException(ValidationException):
    pass


class InvalidTypeException(ValidationException):
    pass


def parse(signature: str) -> Signature:
    """Parses a string like 'int32 f(x:int32,y:int32)' into a Signature instance."""
    pattern = r'(.+) (.+)\((.+)*\)'  # The string must be in format: "type0 fun_name(args*)".
    signature = signature.strip()
    regex_string = re.fullmatch(pattern, signature)

    if regex_string is None:  # if regex is not matched.
        raise ValidationException('Malformed function signature')

    groups = regex_string.groups()
    return_type = groups[0]
    function_name = groups[1]

    if (groups[2] is None) or groups[2].strip() == '':  # Function does not have arguments.
        function_args = []
    else:
        function_args = groups[2].split(
            ':')  # It will be in format ["arg1", "type1, arg2", "type2, arg3", ..., "typeN"]

    if len(function_args) == 1:
        raise ValidationException('Invalid format of function arguments')

    names_and_types: List[str] = [function_name, return_type]  # Argument names and types will be appended:

    if len(function_args) > 0:
        names_and_types.append(function_args[0])

    function_args_len = len(function_args)

    for i in range(1, function_args_len - 1):
        type_arg_list = function_args[i].rsplit(',', 1)
        if len(type_arg_list) < 2:
            raise ValidationException('Invalid format of function arguments')

        names_and_types.extend(type_arg_list)

    if function_args_len > 0:
        names_and_types.append(function_args[function_args_len - 1])  # Appending typeN at the end of list.
    # Remove extra spaces from beginning and end of each arg and type.
    names_and_types = list(map(str.strip, names_and_types))
    tuples_list: List[Tuple[str, str]] = []  # Function name/type, then 1st argument name/type, 2nd, etc.

    for i in range(0, len(names_and_types), 2):
        tuples_list.append((names_and_types[i], names_and_types[i + 1]))
    return Signature(_validate(tuples_list))


def _raise_invalid_type_exception(invalid_type):
    error_message = f'{invalid_type} is an invalid type declaration.'
    if invalid_type in composite_type_names():
        error_message = f'{error_message} Did you mean {invalid_type}[int32]?'
    raise InvalidTypeException(error_message)


def _validate(arg_type_list: List[Tuple[str, str]]) -> List[Tuple[str, Type]]:
    """Validates names and types of the function and arguments, converts types from str to Type."""
    function_name = arg_type_list[0][0]
    function_type = arg_type_list[0][1]

    new_arg_type_list = []

    if not _validate_name(function_name):
        raise InvalidNameException(f'Invalid function name: {function_name}')

    function_type_validation = validate_type(function_type)
    if not function_type_validation[1]:
        _raise_invalid_type_exception(function_type)
    else:
        new_arg_type_list.append((function_name, function_type_validation[0]))

    for i in arg_type_list[1:]:
        if not _validate_name(i[0]):
            raise InvalidNameException(f'Invalid argument name: {i[0]}')

        result = validate_type(i[1])
        if not result[1]:
            _raise_invalid_type_exception(i[1])
        else:
            new_arg_type_list.append((i[0], result[0]))

    # Argument names cannot repeat, argument cannot be named as the function:
    for i in range(0, len(new_arg_type_list)):
        for j in range(i + 1, len(new_arg_type_list)):
            if new_arg_type_list[i][0] == new_arg_type_list[j][0]:
                raise InvalidNameException(
                    f'"{new_arg_type_list[i][0]}" appears more than once among function and argument names')

    # Not allowing declarations of a custom type with more than one different subtypes in one function:
    for i in range(0, len(new_arg_type_list)):
        for j in range(i + 1, len(new_arg_type_list)):
            if new_arg_type_list[i][1].custom:
                if new_arg_type_list[i][1].name == new_arg_type_list[j][1].name:
                    if new_arg_type_list[i][1] != new_arg_type_list[j][1]:
                        raise InvalidTypeException(
                            f'Two declarations of custom type {new_arg_type_list[i][1].name}')

    # Function or argument cannot be named as one of the types:
    for i in range(0, len(new_arg_type_list)):
        for type_name in all_type_names():
            if new_arg_type_list[i][0] == type_name:
                raise InvalidNameException(
                    f'"{type_name}" matches a type name; that is not acceptable for a name')

    return new_arg_type_list


def _validate_name(name: str) -> bool:
    """Checks if given string is a valid name for the student's solution function or its argument."""
    return ALLOW_UPPERCASE_IN_NAMES and bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name)) or \
           not ALLOW_UPPERCASE_IN_NAMES and bool(re.match(r'^[a-z][a-z0-9_]*$', name))
