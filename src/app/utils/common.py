from typing import Callable, TypeVar, List, Any
from datetime import datetime
import re

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

def extract_student_info(filename):
    pattern = r'.*/([A-Za-z0-9_]+)_(.*?)\.[A-Za-z]+$'
    match = re.search(pattern, filename)
    
    if match:
        student_name = match.group(1)
        question_title = match.group(2)
        return student_name, question_title
    else:
        return None, None

