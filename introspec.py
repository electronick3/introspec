import sys, os
import inspect
import types
from os import path

#----------------------------------------------------------- const
FORMAT_PARENT = "{} [{}] ({})"

FORMAT_CHILD = "    {}.{} ({})"

CURDIR = os.path.split(os.path.abspath(__file__))[0]

FILENAME = os.path.join(CURDIR, 'file.txt')
#----------------------------------------------------------- type
def ismodule(obj):
    return isinstance(obj, types.ModuleType)

def isclass(obj):
    return isinstance(obj, type) 

#def isobjectclass(obj, (object)) # дописать 
#     pass
#inspect.getmodule    

def ismethod(obj):
    return isinstance(obj, types.MethodType)

def isfunction(obj):
    return isinstance(obj, types.FunctionType)

def isbuiltin(obj):
    return isinstance(obj, types.BuiltinFunctionType) 

#----------------------------------------------------------- private
def _trim(text, n=80):
    if text == None:
        return ""
    
    s = ' '.join(str(text).replace('\n', ' ').split(' '))[:n]
    if n<80:
        s.join('...')

    return s

def _getname(obj):
    if hasattr(obj, '__name__'): 
        return _trim(obj.__name__, 20)
    
    return _trim(str(obj),20)

def _getdoc(obj):
    if hasattr(obj, '__doc__'):
        return _trim(obj.__doc__)

    return ""    

def _gettype(obj):
   return type(obj)

def _gettype2(obj):
    VARIABLE, MODULE, FUNCTION, BUILTIN  = '<Variable>', '<Module>', '<Function/Method>', '<Builtin method>'

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
            'obj_type': _gettype(obj),
            'obj_doc': _getdoc(obj)}

#----------------------------------------------------------- public

def generator(parent):

    for item in (arg for arg in dir(parent) if not arg.startswith('_')):
        attr = getattr(parent, item)

        yield _getattr(parent, attr)

        if ismodule(attr) or isclass(attr):
            yield from generator(attr)

def new_print_attr(myObject):
    rem = None
    for n, line in enumerate(generator(myObject), 1):
        if not rem:
            rem = line['obj_parent']

        if rem == line['obj_parent']:
            print(FORMAT_PARENT.format(line['obj_child'],
                                       line['obj_type'], line['obj_doc']))
        else:
            print(FORMAT_CHILD.format(line['obj_parent'],
                                      line['obj_child'],
                                      line['obj_doc']))

def print_attr(parent):
    """ 
    print_attr() -> obj

    iter for every attributes in obj and print infomation  
    """
    for arg in [arg for arg in dir(parent) if not arg.startswith('_')]:
        attr = getattr(parent, arg)
        item = _getattr(attr, arg)
        print(FORMAT_PARENT.format(item['obj_parent'], 
                                    item['obj_type'], item['obj_doc']))

        for sub_arg in [sub_arg for sub_arg in dir(attr) 
                        if not sub_arg.startswith('_')]:
            sub_attr = getattr(attr, sub_arg)
            sub_attr_attr = _getattr(sub_attr, arg)                
            print(FORMAT_CHILD.format(sub_attr_attr['obj_parent'], 
                                    sub_attr_attr['obj_child'], 
                                    sub_attr_attr['obj_doc']))   
               
# только модули смотрим внутрь и сделать только один генератор                

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

    new_print_attr(myObject)
    #
    # myObject = os
    # for n, line in  enumerate(generator(myObject), 1):
    #     print(n, line)

