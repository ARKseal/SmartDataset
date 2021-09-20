import importlib
import re
import uuid


def safe(s: str, expr: str = '{}'):
    '''Evaluate the given expression more safely.'''

    if re.sub('[^A-Za-z0-9_]', '', s) != s:
        raise ValueError(f"safe: illegal characters in: '{s}'")

    return eval(expr.format(s))


def new_name():
    return uuid.uuid4().hex


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
