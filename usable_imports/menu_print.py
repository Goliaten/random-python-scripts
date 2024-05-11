from stat_len import stat_len
from clear import clear
from shutil import get_terminal_size
from copy import deepcopy

def pause():
    o = input("Press anything to continue ")

err_c = 0   #used for counting number of (V V V) executed (or rather if it was executed)
m = 1     #decides page to be shown

def menu_print(menu, c=0, d=0, col=1, sec_menu=[]):
    # menu takes in list of strings, c is for vertical allignment,
    # d is for horizontal allignment, sec_menu is for small footer at the bottom of the screen
    # col is for number of columns
    # m is for choosing which menu to show
    # c=0 top; c=1 bottom; c=2 center; d=0 left; d=1 right; d=2 center
    global m, width, length
    clear()                                            #clearing screen
    max_width, length = get_terminal_size((80, 24))        #getting terminal size with default width 80 and length 24
    length -= 1 + len(sec_menu)                     #reducing length of menu(because of either input() or pause() and sec_menu)
    
    if col < 1:
        col = 1
    
    width = int(max_width/col)
    
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
        while len(page_foot[0]) < max_width:           #insterting spaces so that [back] and [next] are on opposite side of screen
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
    
    #----------------additional-column-menus-----------------------
    col_menus = []
    if col > 1:
        for x in range(1, col):
            n_key = f'menu{m+x}'
            if n_key in menus.keys():
                col_menus.append(menus[f'menu{m+x}'])
    
    
    #-----------------menu-alligner/printer-----------------------
    #aligns vertically line and prints it
    for y, x in enumerate(menu):
        
        col_x = []
        if col_menus:                   #gathering additional columns for current row
            for z in col_menus:
                if y < len(z):
                    col_x.append(z[y])
#             col_x = [z[y] for z in col_menus]
#                 print(len(col_menus[0]), y)
#             print(col_x)
        
        if d == 0 and col > 1:             #alligning to left and adding columns
            x = stat_len(x, width)
            if y < len(menu) - len(page_foot + sec_menu):      #if pointer is not in footer or secondary menu
                for z in col_x:
                    x += stat_len(z, width)                    #adding additional column
        elif d == 1:                               #alligning to right
            x = stat_len(x, width, 1)
            if y < len(menu) - len(page_foot + sec_menu):      #if pointer is not in footer or secondary menu
                for z in col_x:
                    x += stat_len(z, width, 1)                    #adding additional column
        elif d == 2:                             #alligning to center
            y = int((width - len(x))/2)+len(x)   #calculating optimal indent
            x = stat_len(stat_len(x, y, 1), width, 0)             #applying indent in front and on the back
            if y < len(menu) - len(page_foot + sec_menu):        #if pointer is not in footer or secondary menu
                for z in col_x:
                    y = int((width - len(z))/2)+len(z)            #calculating optimal indent second time
                    x += stat_len(stat_len(z, y, 1), width, 0)                    #adding additional column
            
        print(x)


#second return of V V V
#0 - all is good
#1 - loop continue (wrong input)
#2 - loop break (exit or go back)
#3 - next page
#4 - previous page

def in_err_ch(o, max_len, min_len=0, c=0):
    #input_error_check    old try: except: in a new function
    #o is for input, max_len and min_len are for limits of a number, c is for disabling wrong input check
    
    if max_len < min_len:                          #for safety
        raise Exception('max_len smaller than min_len')
    
    global m, err_c             #m is for page number, err_c is for instance of this funcion
    
    if err_c == 0:                        #if this is first instance of this function:
        m = 1                             #define page shown as 1st (to make sure it is 1st)
    try:
        o = int(o)               #trying to make number out of string
    except:
        err_c = 1                          #marks that this function has been run
        if o == 'ex':           #'ex' is used to quit from a loop
            m = 1               #define page shown as 1st (same function, as one higher, but has bigger effect(try to picture when this and one higher are used to understand it))
            err_c = 0           #reset instance
            return o, 2
        elif o == 'next':       #to show next page of menu
            return o, 3
        elif o == 'back':       #to show previous page of menu
            return o, 4
        if c == 0:                            #look up in header
            menu_print(['Wrong input'], 1)    #if string is not wanted and wrong
            pause()
        return o, 1
    else:
        if o < min_len or o > max_len:           #if input is smaller than 0 or bigger than length of menu
            err_c = 1                        #mars that this function has been run
            if c == 0:                     #look up in header
                menu_print(['Choice out of range'], 1)
                pause()
            return o, 1
        m = 1               #redefine page number to 1st for future menu show
        err_c = 0        #setting counter back to 0
        return o, 0


if __name__ == '__main__':
    while True:
        temp_menu = ['header']
        for x in range(0, 54):
            x = str(x)
            temp_menu.append(x)
        menu_print(temp_menu, 0, 2)
        a = input('Choose:')

        a, z = in_err_ch(a, len(temp_menu)-1)
       #V V V needed to operate on output of in_err_ch
        if z == 0:         #(usually this would not be needed)
           break
        if z == 1:
            continue
        elif z == 2:
            break
        elif z == 3:
            m += 1
        elif z == 4:
            m -= 1
    print('you passed the check')