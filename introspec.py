""" Get useful information from live Python objects. """

__all__ = ['print_attributes']
__author__ = ('Chagay Nikolay aka Electronick <chagay.ni@gmail.com>')

# This module is in the public domain.  No warranties.

import inspect
import argparse
import importlib

# ----------------------------------------------------------- const
FORMAT_PARENT = "{} [{}] ({})"

FORMAT_CHILD = "    {}.{} ({})"

TEXT_LENGTH = 79

NAME_LENGTH = 20


# ----------------------------------------------------------- private
def _parser():
    """Return the parsed arguments """
    parser = argparse.ArgumentParser(description='Parse object and setting attributes')
    parser.add_argument('-o', action='store', dest='object', type=str, default=None,
                        help='Object for introspection')
    parser.add_argument('-p', action='store_true', dest='only_public',
                        help='Deselect private attributes')

    return parser.parse_args()


def _parse_args(args):
    """
    First if args.object is None then print attributes of __builtins__ module
    else
    Try import args.object if not raise ImportError
    and then
    print the attributes of args.object
    """
    print(args)

    if args.object is None or args.object == '__builtins__':
        print_attributes(__builtins__, args.only_public)
        return

    try:
        obj = importlib.import_module(args.object)
        print_attributes(obj, args.only_public)
    except ImportError:
        print("Unable to import '{}'\n".format(args.object))


def _trim(text, n=TEXT_LENGTH):
    """ Return the trimmed text,  not more than TEXT_LEN """
    if text is None:
        return ""

    s = ' '.join(str(text).replace('\n', ' ').split(' '))
    if len(s) > n:
        if n == TEXT_LENGTH:
            if len(s) > TEXT_LENGTH:
                return '{}...'.format(s[:n - 3])
        else:
            return s[:n]
    return s


def _getname(obj):
    """Return trimmed __name__ or string representation of obj"""
    if hasattr(obj, '__name__'):
        return _trim(obj.__name__, NAME_LENGTH)

    return _trim(str(obj), NAME_LENGTH)


def _getdoc(obj):
    """Return trimmed doc string of obj"""
    return _trim(inspect.getdoc(obj))


def _gettype(obj):
    """Return type of obj"""
    return type(obj)


def _getattr(parent, obj):
    """Returns the dict object needed for printing formatting"""
    return {'obj_parent': _getname(parent),
            'obj_child': _getname(obj),
            'obj_type': _gettype(obj),
            'obj_doc': _getdoc(obj)}


def _attributes(parent, processed=None, only_public=False):
    """Obtaining recursively the attributes of the parent.
     stores the received attributes in the processed variable"""
    if processed is None:
        processed = set()

    for name, item in (arg for arg in inspect.getmembers(parent)
                       if (only_public and not arg[0].startswith('_')) or not only_public):

        try:
            if (parent, name,) not in processed:
                processed.add((parent, name,))
                yield _getattr(parent, item)
            else:
                continue
        except TypeError:
            pass

        if inspect.ismodule(item) or inspect.isclass(item):
            yield from _attributes(item, processed, only_public)


# ----------------------------------------------------------- public


def print_attributes(my_object, only_public=False):
    """ Print formatted attributes for given my_object"""
    parent = None
    for item in _attributes(my_object, only_public=only_public):
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
    _parse_args(_parser())
