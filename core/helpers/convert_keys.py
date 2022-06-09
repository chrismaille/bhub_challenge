from collections import OrderedDict

import stringcase
from rest_framework.exceptions import ErrorDetail


def convert_keys(
    data: dict[any] | list[dict[any]],
    to_case: str,
    show_none: bool = False,
) -> dict[any] | list[dict[any]]:
    """Converts dict keys to a specified case.

    Uses stringcase.convert_case() to convert keys.
    https://github.com/okunishinishi/python-stringcase

    Examples:
        >>> convert_keys(
        >>>     {'first_field': 1, 'second_field': 2, 'third_field': None},
        >>>        'camelcase'
        >>> )
        >>> {'firstField': 1, 'secondField': 2}

        >>> convert_keys(
        >>>    {
        >>>         'firstField': 1,
        >>>         'secondField': 2,
        >>>         'thirdField': None
        >>>    },
        >>>    'snakecase',
        >>>    show_none=True
        >>> )
        >>> {'first_field': 1, 'second_field': 2, 'third_field': None}

    Args:
        data (dict[any] | list[dict[any]]): The data to convert.
        to_case (str): The case to convert to.
        show_none (bool, optional): Whether to show None values. Defaults to False.
    """

    def _convert_keys(source: dict[any], target: dict[any], current_key: str):
        if isinstance(source[current_key], (dict, OrderedDict)):
            new_key = getattr(stringcase, to_case)(current_key)
            target[new_key] = {}
            for k in source[current_key].keys():
                _convert_keys(source[current_key], target[new_key], k)
        elif isinstance(source[current_key], (list, set)):
            new_key = getattr(stringcase, to_case)(current_key)
            target[new_key] = []
            for index, i in enumerate(source[current_key]):
                if isinstance(i, dict):
                    target[new_key].append({})
                    for k in i.keys():
                        _convert_keys(i, target[new_key][index], k)
                else:
                    target[new_key].append(i)
        else:
            new_key = getattr(stringcase, to_case)(current_key)
            if show_none or source[current_key] is not None:
                target[new_key] = source[current_key]

    if isinstance(data, (dict, OrderedDict)):
        converted_dict = {}
        for key in data.keys():
            if isinstance(key, ErrorDetail):
                return data
            _convert_keys(data, converted_dict, key)

        return converted_dict

    if isinstance(data, (list, set)):
        converted_list = []
        for item in data:
            if not isinstance(item, dict):
                converted_list.append(item)
                continue
            converted_dict = {}
            for key in item:
                _convert_keys(item, converted_dict, key)
            converted_list.append(converted_dict)
        return converted_list

    return data
