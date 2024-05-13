from typing import Callable, TypeVar, List, Any
from datetime import datetime

def to_str(
        value: Any,
        dateformat: str='%Y-%m-%dT%H:%M:%S.%fZ'
    ) -> str:
    if value is None:
        return None
    elif type(value) == datetime:
        return value.strftime(dateformat)
    else:
        return str(value)


def escape_regex(text: str) -> str:
    special_chars = '.*+^|[]()?$\\'

    return text.translate(str.maketrans({
        c: f'\\{c}'
        for c in special_chars
    }))

# EOF
