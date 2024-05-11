from copy import deepcopy
import os                              #for clearing screen
from shutil import get_terminal_size   #for menu_print width and length


def pause():
    input('sth')

def clear():              #used to clear terminal/shell screen
    if os.name == 'nt':           #on windows
        os.system('cls')
    else:                #on linux/macOS  (Posix)
        os.system('clear')

m = 0

def menu_print(menu, c=0, d=0, sec_menu=[]):
    # menu takes in list of strings, c is for vertical allignment,
    # d is for horizontal allignment, sec_menu is for small footer at the bottom of the screen
    # m is for choosing which menu to show
    # c=0 top; c=1 bottom; c=2 center; d=0 left; d=1 right; d=2 center
    global m, width, length
    clear()                                            #clearing screen
    width, length = get_terminal_size((80, 24))        #getting terminal size with default width 80 and length 24
    length -= 1 + len(sec_menu)                     #reducing length of menu(because of either input() or pause() and sec_menu)
    
    menus = {
        'menu1': deepcopy(menu)       #creating first menu
    }
    
    #---------------line-breaker-------------------
    for y, x in enumerate(menus['menu1']):       #checking if line is wider than screen
        if len(x) > width:
            for z in range(width, -1, -1):  #spliting line
                v = x[z]
                if v == ' ':              #looking for closest space from the (length) character to first (i.e. looking for ' ' for nice split)
                    sep = z + 1          #separator #if separator is at 0 index, infinite loop wil be created
                    break
            else:                       #or taking the (width) bit
                sep = width
                
            part1 = x[:sep-1] if z == width else x[:sep]   #separating line
            part2 = x[sep:]
            menus['menu1'][y] = part1      #and adding it to menu  (part1 to place on old line)
            menus['menu1'].insert(y+1, part2)                   #(part 2 to next line)
    
    #-------------additional-footer-creator----------------
    page_foot = []       #if there are more than one page, footer is created
    if len(menus['menu1']) > length:
        length -= 1 #reducing length, so page footer can fit
        
        page_foot.append('[back][next]')
        while len(page_foot[0]) < width:           #insterting spaces so that [back] and [next] are on opposite side of screen
            page_foot[0] = page_foot[0][:6] + ' ' + page_foot[0][6:]
    
    
    #---------------new-menu-creator---------------------
    #adds new menu page each time the amount of lines in menu is bigger than length
    if len(menus['menu1']) > length:
        for x in range(0, int(len(menus['menu1']) / length)):
            new_key = 'menu' + str(x + 2)
            menus[new_key] = []


    #----------------menu-organiser------------
    #moves excess lines to next menu
    y = 0
    for key in menus:
        y += 1
        next_key = key[:4] + str(y + 1)         #setting next key in dictionary
        while len(menus[key]) > length:         #moving lines untill len(menu) fits in length
            if not menus[next_key]:           #adding excess line to new key
                menus[next_key] = [menus[key][length]]    #if doesn't hold anything
            else:
                menus[next_key].append(menus[key][length])   #if holds something
                
            del menus[key][length]     #deleting excess line from old key
    
    #---------page-normaliser---------------------
    #makes sure m isn't bigger than number of menus
    if len(menus) < m:
        m = len(menus)        #maximal m
    elif 0 >= m:
        m = 1            #minimal m
    
    menu = menus[f'menu{m}']  #setting active menu
    
    #---------------menu-extender----------------
    #extends menu until it is long enough
    if c == 0:
        while len(menu) < length:              #adds '' to end of the list
            menu.append('')
    elif c == 1:
        while len(menu) < length:           #adds '' to beginning of the list
            menu.insert(0, '')               #list.insert(index, value)
    elif c == 2:
        y = int((length - len(menu))/2)+len(menu)   #adds '' to beginning and the end of list
        while len(menu) < y:                      #adds '' to beginning of the list
            menu.insert(0, '')
        while len(menu) < length:              #adds '' to end of the list
            menu.append('')
    
    menu += page_foot + sec_menu
    
    #-----------------menu-alligner/printer-----------------------
    #aligns vertically line and prints it
    for x in menu:
        if d == 1:                               #alligning to right
            x = stat_len(x, width, 1)
        elif d == 2:                             #alligning to center
            y = int((width - len(x))/2)+len(x)   #calculating optimal indent
            x = stat_len(x, y, 1)
        print(x)


width, length = get_terminal_size((80, 24))
temp_menu = ['_', '', '']
for x in range(len(temp_menu)):
    for y in range(width):
        temp_menu[x] += '_'

menu_print(temp_menu)


