import os
from copy import deepcopy
from shutil import get_terminal_size

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def stat_len(x, y=1, c=0):      #x is value to be lengthened, y is length, c is option choosing
    x = str(x)
    while len(x) < y and c == 0:          #adds ' ' to the end
        x += ' '
    while len(x) < y and c == 1:          #adds ' ' to the beginning
        x = ' ' + x
    return x
    
# def menu_print(menu, c=0, d=0, length=23, width=80): #length could be 24, but inputs take one of the spaces
#     #menu takes in list of strings, c is for vertical allignment,
#     #d is for horizontal allignment, length is used with c, width is used with d
#     
#     clear()
#     menu = deepcopy(menu)
#     
#     if c == 0:
#         while len(menu) < length:   #adds '' to end of the list
#             menu.append('')
#     elif c == 1:
#         while len(menu) < length:   #adds '' to beginning of the list
#             menu.insert(0, '')     #list.insert(index, value)
#     
#     for x in menu:
#         if d == 1:
#             x = stat_len(x, width, d)   #used for alligning right
#         print(x)
def menu_print(menu, c=0, d=0, sec_menu=[]): #length could be 24, but inputs take one space
    #menu takes in list of strings, c is for vertical allignment,
    #d is for horizontal allignment, length is used with c, width is used with d
    #c=0 top; c=1 bottom; d=0 left; d=1 right; d=0 center
    clear()
    width, length = get_terminal_size((80, 24))
    menu = deepcopy(menu)
    
    length -= len(sec_menu)
    
    if c == 0:
        while len(menu) < length:   #adds '' to end of the list
            menu.append('')
        menu += sec_menu
    elif c == 1:
        while len(menu) < length:   #adds '' to beginning of the list
            menu.insert(0, '')     #list.insert(index, value)
        menu += sec_menu
    elif c == 2:
        y = int((length - len(menu))/2)+len(menu)    #adds '' to beginning and the end of list
        while len(menu) < y:   #adds '' to beginning of the list
            menu.insert(0, '')
        while len(menu) < length:
            menu.append('')
        menu += sec_menu
            
    for x in menu:
        if d == 1:                        #alligning to right
            x = stat_len(x, width, 1)
        elif d == 2:                      #alligning to center
            y = int((width - len(x))/2)+len(x)   #calculating optimal indent
            x = stat_len(x, y, 1)
        print(x)

menu_1 = [
    'Welcome to the menu 1',
    ' 1. option 1',
    ' 2. option 2',
    ' 3. option 3',
    ]

menu_2 = [
    'Player one',
    'Fight'
    ]

menu_print(menu_1)
empty = input('enter ')
menu_print(menu_1, 1)
empty = input('enter ')
menu_print(menu_1, 2)
empty = input('enter ')
menu_print(menu_1, 0, 1)
empty = input('enter ')
menu_print(menu_1, 1, 1)
empty = input('enter ')
menu_print(menu_1, 2, 1)
empty = input('enter ')
menu_print(menu_1, 0, 2)
empty = input('enter ')
menu_print(menu_1, 1, 2)
empty = input('enter ')
menu_print(menu_1, 2, 2, menu_2)
empty = input('enter ')
# menu_print(menu_1, 0, 1)
# empty = input('enter ')