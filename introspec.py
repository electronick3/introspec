import sys, os
from os import path

def trim_(text, n=80):
    
    if text == None:
        return ""

    return ' '.join(text.replace('\n', ' ').split(' '))[:n]

def print_first_line(f=None, **kwarg):
    """
    print the first formatted line
    """
    print(f"{kwarg['obj_name']} [{kwarg['obj_type']}] ({kwarg['obj_doc']})",  
            sep='', end='\n', file=f)

def print_second_line(f=None, **kwarg):
    """
    print the second formatted line 
    """
    print(f"    {kwarg['obj_name']}.{kwarg['obj_method']} ({kwarg['obj_doc']})",  
            sep='', end='\n', file=f)

def getattr_(obj):
    attr_dic = {}
    
    # Name object
    obj_name = ""
    if hasattr(obj, '__name__'):
        obj_name = trim_(obj.__name__, 20)
    else:
        obj_name = trim_(str(obj), 20)    
        
    # Type of object 
    obj_type = ""
    obj_type = type(obj)

    # Doc string 
    obj_doc = ""
    if hasattr(obj, '__doc__'):
        obj_doc = trim_(obj.__doc__)

    # Callable 
    obj_call = False
    obj_method = ""
    if hasattr(obj, '__call__'):
        obj_call = True
        obj_method = obj_name

    # Modules
    obj_loader = False 
    if hasattr(obj, '__loader__'):
        obj_loader = True

    attr_dic.update({'obj_name': obj_name, 
                    'obj_type': obj_type,
                    'obj_method': obj_method, 
                    'obj_doc': obj_doc,
                    'obj_call': obj_call,
                    'obj_loader': obj_loader})

    return attr_dic

def print_attr(obj, write_file=False):
    """
    print_attr() -> obj, write_file=False


    iter for every attributes in obj and print infomation  
    """
    
    cur_dir = os.path.split(os.path.abspath(__file__))[0]
    out_file = os.path.join(cur_dir, 'file.txt')

    with open(out_file, 'w') as f: 
        if not write_file:
            f = None

        for arg in [arg for arg in dir(obj) if not arg.startswith('_')]:
            attr = getattr(obj, arg)
            print_first_line(f, **getattr_(attr))

            for sub_arg in [sub_arg for sub_arg in dir(attr) if not sub_arg.startswith('_')]:
                sub_attr = getattr(attr, sub_arg)
                sub_attr_attr = getattr_(sub_attr)
                # this is fun
                if callable(sub_attr):
                    sub_attr_attr.update({'obj_name': str(arg)})
                    print_second_line(f, **sub_attr_attr)    


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

    print_attr(__builtins__, write_file=True)
