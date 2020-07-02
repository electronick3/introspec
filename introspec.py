""" Get useful information from live Python objects. """

__all__ = ['print_attributes']
__author__ = 'Chagay Nikolay aka Electronick <chagay.ni@gmail.com>'

# This module is in the public domain.  No warranties.

import inspect
import argparse
import importlib
import statistics
import _json

# ----------------------------------------------------------- const
FORMAT_PARENT = "{} [{}] ({})"

FORMAT_CHILD = "    {}.{} ({})"

TEXT_LENGTH = 79

NAME_LENGTH = 20


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
            'obj_doc': _getdoc(obj)
            }


def _attributes(parent, rem_parent=None, processed=None, only_public=False):
    """Obtaining recursively the attributes of the parent.

     stores the received attributes in the processed variable

     """
    if processed is None:
        processed = set()

    for name, item in (arg for arg in inspect.getmembers(parent)
                       if (only_public and not arg[0].startswith('_'))
                          or not only_public):

        try:
            if (parent, name,) not in processed:
                processed.add((parent, name,))
                if rem_parent:
                    yield _getattr(rem_parent, item)
                else:
                    yield _getattr(item, item)
            else:
                continue
        except TypeError:
            pass

        if inspect.ismodule(item) or inspect.isclass(item):
            yield from _attributes(item, item, processed, only_public)


# ----------------------------------------------------------- public

def print_attributes(my_object, page=None, only_public=False):
    for num, item in enumerate(_attributes(my_object, only_public=only_public)):

        if item['obj_parent'] == item['obj_child']:
            print(FORMAT_PARENT.format(item['obj_parent'],
                                       item['obj_type'],
                                       item['obj_doc']))
        else:
            print(FORMAT_CHILD.format(item['obj_parent'],
                                      item['obj_child'],
                                      item['obj_doc']))

        if page and (num > 0 and num % page == 0):
            input('Press enter to continue...')


if __name__ == '__main__':
    """Создать скрипт на python который выведет 
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
    """Return the parsed arguments """
    parser = argparse.ArgumentParser(description='Parse object and setting attributes')
    parser.add_argument('-o', action='store', dest='object', type=str,
                        default=None, help='Object for introspection')
    parser.add_argument('-op', action='store_true', dest='only_public',
                        help='Deselect private attributes')
    parser.add_argument('-p', action='store', dest='page_count', type=int,
                        default=None, help='Pagination')
    args = parser.parse_args()

    if args.object is None or args.object == '__builtins__':
        print_attributes(__builtins__, args.page_count, args.only_public)
    else:
        try:
            obj = importlib.import_module(args.object)

            print_attributes(obj, args.page_count, args.only_public)
        except ImportError:
            print("Unable to import '{}'\n".format(args.object))
