import inspect
import os
import sys
import types
from os import path

# ----------------------------------------------------------- const
FORMAT_PARENT = "{} [{}] ({})"

FORMAT_CHILD = "    {}.{} ({})"

CUR_DIR = os.path.split(os.path.abspath(__file__))[0]

FILENAME = os.path.join(CUR_DIR, 'file.txt')

VARIABLE, MODULE, FUNCTION, BUILTIN = '<Variable>', '<Module>', '<Function/Method>', '<Builtin method>'


# ----------------------------------------------------------- type
def ismodule(obj):
    return isinstance(obj, types.ModuleType)


def isclass(obj):
    return isinstance(obj, type)


def ismethod(obj):
    return isinstance(obj, types.MethodType)


def isfunction(obj):
    return isinstance(obj, types.FunctionType)


def isbuiltin(obj):
    return isinstance(obj, types.BuiltinFunctionType)


# ----------------------------------------------------------- private
def _trim(text, n=80):
    if text is None:
        return ""

    s = ' '.join(str(text).replace('\n', ' ').split(' '))[:n]
    if n < 80:
        s.join('...')

    return s


def _getname(obj):
    if hasattr(obj, '__name__'):
        return _trim(obj.__name__, 20)

    return _trim(str(obj), 20)


def _getdoc(obj):
    if hasattr(obj, '__doc__'):
        return _trim(obj.__doc__)

    return ""


def _gettype(obj):
    return type(obj)


def _gettype2(obj):
    if isfunction(obj) or ismethod(obj):
        return '{}, {}'.format(type(obj), FUNCTION)

    elif ismodule(obj) or isclass(obj):
        return '{}, {}'.format(type(obj), MODULE)

    elif isbuiltin(obj):
        return '{}, {}'.format(type(obj), BUILTIN)

    else:
        return '{}, {}'.format(type(obj), VARIABLE)


def _getattr(parent, obj):
    return {'obj_parent': _getname(parent),
            'obj_child': _getname(obj),
            'obj_type': _gettype2(obj),
            'obj_doc': _getdoc(obj)}


# ----------------------------------------------------------- public

def attributes(parent, processed=None):
    if processed is None:
        processed = set()

    for item in (arg for arg in dir(parent) if not arg.startswith('_')):
        attr = getattr(parent, item)

        if (parent, item,) not in processed:
            processed.add((parent, item,))
            yield _getattr(parent, attr)
        else:
            continue

        if ismodule(attr) or isclass(attr):
            yield from attributes(attr, processed)


def print_attr(my_object):
    parent = None
    for item in attributes(my_object):
        if not parent:
            parent = item['obj_parent']

        if parent == item['obj_parent']:
            print(FORMAT_PARENT.format(item['obj_child'],
                                       item['obj_type'],
                                       item['obj_doc']))
        else:
            print(FORMAT_CHILD.format(item['obj_parent'],
                                      item['obj_child'],
                                      item['obj_doc']))


if __name__ == '__main__':
    """
    Создать скрипт на python который выведет 
    1. Все встроенные переменные, функции, типы и классы 
    с обозначением их типа
    
    2. Если у класса или типа есть встроенные методы 
    или свойства, то вывести их
    
    3. Если у функции/метода есть описание или сигнатура вывести и их

    2. Отформатировать вывод в читаемом формате:
        Имя [тип] (сигнатура/описание одной строкой 
        без переносов не более 80 символов)
        <4 пробела>Имя.метод (сигнатура/описание)
    """
    myObject = __builtins__

    print_attr(myObject)
