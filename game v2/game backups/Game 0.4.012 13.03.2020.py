#!/usr/bin/env python3.7
from random import randint             #for random integer (duh...)
from copy import deepcopy              #for copying class instances
import os                              #for clearing screen
from shutil import get_terminal_size   #for menu_print width and length

#----------letters_used_in_code---------------------
#currently used: a,b,c,d,k,l,m,o,p, q,w,v,x,y,z

#z is for while loops(used in error protection) AND another placeholder used in for loop (used first in fight_choose print)
#s is secondary for while loops(also used in error protection)
#o is for returns/data to be used outside of function AND targeting AND choices
#p is secondary for targeting  AND better looking inventory prints(see item.buy_item) AND better looking class t_comm
#x AND y AND w are for 'for' loops
 #x is used as:(for x in ...) AND is used for character in current turn in fight(so try to not redefine it in subsequent functions)
 #y is for counter in for loop
 #z often substitutes x or y AND is often used as return of in_err_ch()
#v is for empty input(not in pause func) AND a mostly used placeholder
#l is secondary/placeholder for choices
#k is tertiary placeholder
#c and d are for choosing which option of function to run
#d is for choosing in dictionaries(see shop>buy items)
#a is for choosing what to do(in wide/main function)
#m is GLOBAL for menu pages
#q is used as variable for special attacks experimental version

#----------------other_variable_names-------------////incomplete////
#obviously names of functions and classes
#t_target used for getting out of item_fnc targets
#emptyinput is for pause()
#dmg is used in calculating damage for attack
#known_magic/skills/passive are for 'global' magic/skills/passive

#-----------------sort_keys_here-------------------
sortid = lambda y : y.ID

version = '0.4.012'
gold = 100             #gold owned (duh...)
all_id_class = []      #for showing all class ID
ID = 0                 #for unified ID order
# DO NOT SORT KILL COUNTERS
kill_counter = [[], []]   #counter for kills (stores id and on corresponding index count for kills)
cmsn_kill_counter = [[], []]  #comission copy of A A A

#--------------------function_zone-----------------------

def pause(x=0):   #x=1 if for secret debug menu
    o = input("Press anything to continue ")
    if x == 1:
        return o

def clear():              #used to clear terminal/shell screen
    if os.name == 'nt':           #on windows
        os.system('cls')
    else:                #on linux/macOS  (Posix)
        os.system('clear')

def stat_len(x, y=1, c=0, char=' '):      #x is value to be lengthened, y is length, c is option choosing
    x = str(x)
    while len(x) < y and c == 0:          #adds ' ' to the end
        x += char
    while len(x) < y and c == 1:          #adds ' ' to the beginning
        x = char + x
    return x

#-/-/-/-/-/-/ unused \-\-\-\-\-\-
def list_substr(lis_1, lis_2):
    #substracts values of list 2 from list 1 and outputs result and indexes with values lower than 0
    out, r_list = [], []              #r_list = 'removed' list
    maxim = 0
    
    for l, x in enumerate(zip(lis_1, lis_2)):
        maxim = l + 1
        x, y = x                    #unpacking list
        z = x - y                    #calculating new number
        if z <= 0:                    #if it's smaller than 0
            r_list.append(l)        #add index, at which it was, to 'removed' list
            continue
        out.append(z)
    else:
        for x in range(maxim, len(lis_1)):       #add those numbers, which index was bigger, than those of lis_2
            out.append(lis_1[x])
    return out, r_list

#2 dimensional list substracion with structure[[indexes/headers], [data]]
def list_sub_2d_id(lis_1, lis_2):
    out = [[], []]
    r_lis = []
    for ind1, x in enumerate(lis_1[0]):
        if x in lis_2[0]:
            ind2 = lis_2[0].index(x)
            
            n_y = lis_1[1][ind1] - lis_2[1][ind2]
#             print(f' ind1y:{lis_1[1][ind1]}, ind2y:{lis_2[1][ind2]}')
#             print(f' ind1:{ind1}, ind2:{ind2}, n_y:{n_y}')
            
            if n_y > 0:
                out[0].append(x)
                out[1].append(n_y)
        else:
            n_y = lis_1[1][ind1]
            out[0].append(x)
            out[1].append(n_y)
    
    return out

char2num = lambda lis : [x.ID for x in lis]
num2char = lambda lis : [y for y in all_id_class for x in lis if x == y.ID]

def nice_drop_comm(base, option=0):         #counter function, makes drop info a bit nicer
    #takes in list of items and outputs their names and how much of each of them there are
    #opion=1 returns tables on which function was operating =0 returns output for fight end drop gain
    orig = []                          #original items
    orig_count = []       #count of items in A A A
    out = ''            #output
    
    for x in base:                  #making unique list and count lis
        if x.ID in [y.ID for y in orig]:
            index = [y.ID for y in orig].index(x.ID)
            orig_count[index] += 1
        else:                             #if item is seen for the first time
            orig.append(x)
            orig_count.append(1)
    
    if option == 1:
        return orig, orig_count
    
    for x, y in zip(orig, orig_count):        #creating comment
        out += f'{x.name}'
        
        if y != 1:
            out += f'*{y}, '
        else:
            out += ', '
    out = out[:-2] + ' '
    
    return out
    
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


err_c = 0   #used for counting number of (V V V) executed (or rather if it was executed)
m = 1     #decides page to be shown

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

#---------------example-code---------------+
# while True:
#     temp_menu = ['header']
#     for x in range(0, 54):
#         x = str(x)
#         temp_menu.append(x)
#     menu_print(temp_menu, 0, 2)
#     a = input('Choose:')
# 
#     a, z = in_err_ch(a, len(temp_menu)-1)
#    #V V V needed to operate on output of in_err_ch
#     if z == 0:(usually this would not be needed)
#        break
#     if z == 1:
#         continue
#     elif z == 2:
#         break
#     elif z == 3:
#         m += 1
#     elif z == 4:
#         m -= 1
#------------------------------------------+

temp_menu = [f'Initialising Game v{version}',
             'Important notes:',
             '-if any errors occur please inform me',
             '-currently drop tables and comissions are being introduced',
             '(they may cause exception)',
             '-help is written in 5.Menu > 1.Show help']
menu_print(temp_menu, 2, 2)
dev_opt = pause(1)

def type_check(char, enem, atk_dmg):    #(character that attacks, enemy that defends, attack damage)
                                        #depending on weapon.dmg_type returns dmg_bonus and dmg_reduction
    bon = 0         #these two are for weapons that have no dmg_type
    red = 0
    x = char.weapon.dmg_type_1
    z = char.weapon.dmg_type_2
    y = enem.defence
    
    if x == 'blunt' or z == 'blunt':    #blunt
        bon = int(atk_dmg*0.4)              #damage bonus(depends on enemy defence)
        red = int(atk_dmg*0.2)              #damage reduction(reduces effect of bon)
        if bon > y:                     #prevents bon or red from going over the defence
            bon = y
        return bon, red
    if x == 'slash' or z == 'slash':   #slash
        bon = int(atk_dmg*0.2)
        red = int(atk_dmg*0.4)
        if red > y:
            red = y
        return bon, red
    if x == 'pierce' or z == 'pierce':   #pierce
        bon = int(atk_dmg*0.1)
        if bon > y:
            bon = y
        return bon, red
    return bon, red                       #for none types

#I could shorten stat() using list comprehension/string if statements, but it would look awful
def stat(char, c=0, leng=10):      #(character, c=0:basic stats c=1:extended stats, length of name)
    if c == 0:                   #displays statictics
        out = f'{stat_len(char.name, leng+1)}- health:{char.stat_hp}/{char.stat_hp_max} attack:{char.atkmin}-{char.atkmax} total defence:{char.stat_defence}'
        if char.mana_max != 0:
            out += f' mana:{char.stat_mana}/{char.stat_mana_max}'
        return out
    elif c == 1:             #displays statistics with weapons and armor
        out = f'{stat_len(char.name, leng+1)}- health:{char.stat_hp}/{char.stat_hp_max} attack:{char.atkmin}-{char.atkmax} total defence:{char.stat_defence}'
        if char.weapon.ID != basic.ID:
            out += f' weapon:{char.weapon.stat_name} dmg:{char.weapon.stat_dmg} (~{char.weapon.dmg_var})'
        if char.armor.ID != basal.ID:
            out += f' armor:{char.armor.stat_name} armor defence:{char.armor.stat_defence}'
        if char.mana_max != 0:
            out += f' mana:{char.stat_mana}/{char.stat_mana_max} (+{char.stat_mana_gain})'
        return out

def stat_print(c=0):
    #c=0 print everyone, c=1 print friendly team, c=2 print enemy team, c=3 print more about friendly team

    ret_list = []         #return list
    max_len = 0   #maximal length of name

    if c == 0:           #for making dynamic stat display(available length depends on length of longest character name)
        for x in team_1 + team_2:
            if len(x.name) > max_len:
                max_len = len(x.name)
    elif c in [1, 3]:
        for x in team_1:
            if len(x.name) > max_len:
                max_len = len(x.name)
    elif c == 2:
        for x in team_2:
            if len(x.name) > max_len:
                max_len = len(x.name)
    
    if c == 0:                      #adding header for allies
        ret_list.append('Allies')
        
    if c==0 or c==1 or c==3:     #allies statistics
        for x in team_1:
            if c==3:                 #detailed
                y = stat(x, 1, max_len)
            else:                    #basic
                y = stat(x, 0, max_len)
                
            ret_list.append(y)           #add to return list
                
    if c == 0:                   #adding header for enemies
        ret_list += ['', 'Enemies:']
        
    if c==0 or c==2:
        for x in team_2:            #ading enemies' stats to return list
            y = stat(x, 0, max_len)
            
            ret_list.append(y)        #add to return list
            
    return ret_list

def EoT_summ():                                      #End of Turn summary
    temp_menu = [f'Turn {turn} summary:']
    for x in all_fghtr:                   #prints what character did in a turn
        temp_menu.append(x.t_comm)     #adding turn comment to temp_menu
        if x.hp <= 0:                   #overwriting turn comments depending on health of character
            x.t_comm = f'{x.name} died'
        else:
            x.t_comm = f'{x.name} did not do a thing'
            
    if len(passive_comm) > 2:   #if there are any passives
        temp_menu += passive_comm      #taking comments from passives (list)
    
    menu_print(temp_menu)        #printing summary
    pause()

def team_target(c, sec_menu=[]):        #used for choosing target
    #(c=1 target is team_1 c=2 target is team_2)
    
    global o, m          #no returns instead working on global o
    sec_menu_bac = [z for z in sec_menu]  #backup for secondary menu
    z = 0
    if c == 1:               #target is team_1
        while True:
            sec_menu = [z for z in sec_menu_bac]      #for starting with same sec_menu all times
            
            for y, x in enumerate(team_1):
                if x.hp <= 0:         #can't target for attack/buff/debuff/heal deadman (not here at least)
                    continue
                if y == 0 and not sec_menu:
                    sec_menu = [f'{y}. {x.stat_name} {x.stat_hp}/{x.stat_hp_max}']
                else:
                    sec_menu.append(f'{y}. {x.stat_name} {x.stat_hp}/{x.stat_hp_max}')            #printing team_1 members with indexes
                    
            menu_print(temp_menu, 0, 0, sec_menu)
            
            o = input('Choose: ')
            
            o, z = in_err_ch(o, y)
            
            if z == 1:
                continue
            elif z == 3:
                m += 1
            elif z == 4:
                m -= 1
            elif z == 0:
                if team_1[o].hp <= 0:
                    menu_print(temp_menu, 0, 0, [f'{team_1[o].name} is already dead'])
                    p = input('Do you want to act upon a dead body?(type "yes" to confirm) ')
                    if p == 'yes':
                        break
                    else:
                        continue
                break
    if c == 2:
        while True:
            sec_menu = [z for z in sec_menu_bac]       #for starting with same sec_menu all times
            
            for y, x in enumerate(team_2):
                if x.hp <= 0:         #can't target for attack/buff/debuff/heal deadman (not here at least)
                    continue
                if y == 0 and not sec_menu:
                    sec_menu = [f'{y}. {x.stat_name} {x.stat_hp}/{x.stat_hp_max}']
                else:
                    sec_menu.append(f'{y}. {x.stat_name} {x.stat_hp}/{x.stat_hp_max}')            #printing team_2 members with indexes
            menu_print(temp_menu, 0, 0, sec_menu)
            
            o = input('Choose: ')
            
            o, z = in_err_ch(o, y)
            
            if z == 1:
                continue
            elif z == 3:
                m += 1
            elif z == 4:
                m -= 1
            elif z == 0:
                if team_2[o].hp <= 0:
                    menu_print(temp_menu, 0, 0, [f'{team_2[o].name} is already dead'])
                    p = input('Do you want to act upon a dead body?(type "yes" to confirm) ')
                    if p == 'yes':
                        break
                    else:
                        continue
                break

def fight_end(c, g_gain=0, exp_gain=0, def_drop=[], prb_drop=[]):
    #c is just to choose which side won,
    #g_gain, exp_gain are for gold and experience gained respectively
    #def_drop and prb_drop are for definitive and probable drop respectively
    global gold, held_mater, temp_menu, kill_counter
    for x in team_1:
        x.heal_up()
    if c == 1:         #if team_1 won
        
        temp_menu = ['You won the fight']                        #(prepare to)print some info
        
        #--------------------gold------------------------
        if g_gain == 0:                                          #if gold is not specified
            for x in team_2:                              #get gold gained from monster gold_drop
                g_gain += x.g_drop
            temp_menu.append(f'You gained {g_gain} gold')
            gold += g_gain     #add gained gold
            
        else:                                     #if gold was specified
            temp_menu = [
            'You won the fight',
            f'You gained {g_gain} gold'
            ]
            gold += g_gain                                   #gain set amount f gold
        
        #----------------------exp-------------------------
        if exp_gain == 0:
            for x in team_2:
                exp_gain += x.exp_drop
            exp_gain = int(exp_gain/len(team_1))
            
            for x in team_1:
                x.exp += exp_gain - int(exp_gain*(x.level-1)/100)
                x.total_exp += exp_gain - int(exp_gain*(x.level-1)/100)
                temp_menu.append(f'{x.name} gained {exp_gain} experience points')
        
        else:
            exp_gain = int(exp_gain/len(team_1))
            for x in team_1:
                x.exp += exp_gain - int(exp_gain*(x.level-1)/100)
                x.total_exp += exp_gain - int(exp_gain*(x.level-1)/100)
                temp_menu.append(f'{x.name} gained {exp_gain} experience points')
        
        #---------------------------definitive drop----------------------------
        temp_menu += ['']         #adding spacer in menu
        temp_drop = []
        if def_drop:
            held_mater += def_drop                         #adding drop table to held materials
            comm = f'{"Monsters" if len(team_2)>1 else "Monster"} belched out: '
            comm += nice_drop_comm(def_drop)
            temp_menu.append(f'{comm}which you gather.')
            
        else:
            for x in team_2:                        #going over each definitive drop table of the enemies
                if x.def_drop != None:
                    held_mater += x.def_drop
                    temp_drop += x.def_drop
            if temp_drop:
                comm = f'{"Monsters" if len(team_2)>1 else "Monster"} belched out: '
                comm += nice_drop_comm(temp_drop)
                temp_menu.append(f'{comm}which you gather.')
        
        #-------------------------propable drop--------------------------------
        if prb_drop:
            temp_drop = []
            for drop, chance in zip(prb_drop[0], prb_drop[1]):           #go over drop items and their drop chances simultaneously
                if chance >= randint(1, 100):              #if chance is greater than randomised number
                    temp_drop.append(drop)                #temporarily gain item
            
            if temp_drop:                            #if probable drop was indeed gained
                comm = f'{"They" if len(team_2)>1 else "It"} also left: '
                comm += nice_drop_comm(temp_drop)
                temp_menu.append(f'{comm}behind.')
                held_mater += temp_drop                  #adding gained items to held material list
            
        else:
            temp_drop = []
            for x in team_2:
                if x.prb_drop != None:
                    for drop, chance in zip(x.prb_drop[0], x.prb_drop[1]):
                        if chance >= randint(1, 100):              #if chance is greater than randomised number
                            temp_drop.append(drop)                #temporarily gain item
                
            if temp_drop:                            #if probable drop was indeed gained
                comm = f'{"They" if len(team_2)>1 else "It"} also left: '
                comm += nice_drop_comm(temp_drop)
                temp_menu.append(f'{comm}behind.')
                held_mater += temp_drop                  #adding gained items to held material list
                
        held_mater.sort(key=sortid)
        
        #----------------kill counter incrementation--------------------
        for x in team_2:
            if not x.ID in kill_counter[0]:
                kill_counter[0].append(x.ID)
                kill_counter[1].append(0)
            
            ind = kill_counter[0].index(x.ID)
            kill_counter[1][ind] += 1
        
        temp_menu.append('')         #adding spacer in menu
        for x in team_1:
            x.level_up_check()

    if c == 2:        #if team_2 won
        temp_menu = [
        'You lost the fight',
        'What a shame...'
        ]
    menu_print(temp_menu)
    pause()
        
def fight_end_check(g_gain=0, exp_gain=0, def_drop=[], prb_drop=[]): #checking if battle ended
    #g_gain is for setting gold gained, exp_gain is for experience obtained
    #def_drop is for manually set definitive drop, prb_drop is for manually set probable drop
    x = 0
    for y in team_1:
#         if y == False:        #oh wow, this is an old artifact part of code. i better comment it
#             continue
        x += y.hp                    #summing up hp of team_1 fighters
    if x <= 0:                      #if it's less or equal than 0
        EoT_summ()                 #summarise the turn
        fight_end(2)                #use <- function
        return 'end'                #used for breaking loops
    
    x = 0
    for y in team_2:
        x += y.hp                #summing hp of team_2 fighters
    if x <= 0:                   #if it's less or equal 0
        EoT_summ()               #summarise turn
        fight_end(1, g_gain, exp_gain, def_drop, prb_drop)            #core function for handling end of battle
        return 'end'               #used for breaking loops

def fight(ally, enem, g_gain=0, exp_gain=0, def_drop=[], prb_drop=[]):
    #this one might be messy, since it was taken from __main__ into function
    
    global team_1, team_2, o, p, all_fghtr, all_fghtr_dict, turn, held_items, l, x, temp_menu, m, passive_comm
    
    team_1 = ally               #can't set team_1 as a parameter and as a global simultaneously
    team_2 = enem
    
    for x in team_1:                     #setting variable for turn fighting
        x.team = 'allies'
    for x in team_2:
        x.team = 'enemies'
    
    all_fghtr = team_1 + team_2               #ading all fighters to a list
    
    all_fghtr_dict = {}                    #for buff.char access(loop part of effect)
    for x in all_fghtr:
        key = x.name
        all_fghtr_dict[key] = x

    turn = 0
    t_comm_list = []                    #list of turn comments
    sec_menu = []                     #for safety from UndefinedVariable error
    active_effects_cp = []            #also for safety from same error
    
    for x in all_fghtr:                    #heal and mana refill for next battle
        x.heal_up()
        
    for x in all_fghtr:
        for y in x.skill:            #setting initial cooldown for skills
            y.cooldown = y.init_cooldown
    
    e = ''                                #for end check
    z = 0                  #for main while loop in battle
#     s = 0
    while z == 0:
        passive_comm = ['','Passives and effects:']        #for comment at EoT_summ for passives
        turn += 1
            
        for x in all_fghtr:
            while z == 0:
                if x.hp <= 0:
                    break
                temp_menu = [f'Turn: {str(turn)}', '']
                temp_menu += stat_print(0)
                
                if x.team == 'allies':
                    sec_menu = [
                    x.name + ' turn',
                    "1.Attack",
                    "2.Special attack",
                    "3.Use item",
                    "4.Flee"
                    ]
                    menu_print(temp_menu, sec_menu=sec_menu)
                    a = input("choose a number: ")

                    a, k = in_err_ch(a, len(sec_menu)-1, 1)
                    
                    if k == 1:
                        continue
                    elif k == 3:
                        m += 1
                    elif k == 4:
                        m -= 1
                        
                    if a == 1:
                        team_target(2, [f'Who does {x.name} attack? '])      #choosing target
                        p = team_2[o]                                           #defining p for class comment in deal_dmg
                        dmg = x.deal_dmg()                              #setting damage
                        team_2[o].take_dmg(dmg)                 #target receiving damage
                        del p, dmg
                        
                        e = fight_end_check(g_gain, exp_gain, def_drop, prb_drop)      #end check
                        break
                    elif a == 2:
                        while True:
                            y = 1
                            contr = []
                            sp_atk = x.magic + x.skill
                            if not sp_atk:
                                menu_print([], 0, 0, [f'{x.name} does not now any special attack.'])
                                pause()
                                break
                            else:
                                temp_menu = ['Available special attacks']
                                if x.mana_max != 0 and x.magic: #remove x.magic for old v                     #if character has mana pool
                                    temp_menu.append(f'{y}. Magic')
                                    contr.append(1)
                                    y += 1
                                if x.skill:    #if known_skills        #if (/t/e/a/m/)character knows any skills
                                    temp_menu.append(f'{y}. Skills')
                                    contr.append(2)
                                    y += 1
                                
                                menu_print(temp_menu)
                                l = input('Choose (type "ex" to quit"): ')
                                
                                l, k = in_err_ch(l, len(temp_menu)-1, 1)
                                
                                if k in [1, 3, 4]:
                                    continue
                                elif k == 2:
                                    break
                                
                                if l == 1 and 1 in contr:               #if magic was chosen print available magic
                                    for y, w in enumerate(x.magic):
                                        if y == 0:
                                            temp_menu = ['Magic:']
                                        temp_menu.append(f'{y}. {w.stat_name} fnc:{w.fnc_name} for:{w.value} cost:{w.m_cost}')
                                    menu_print(temp_menu)
                                    sec_menu = 'Choose magic to cast(type "ex" to quit"): '
                                
                                elif (l == 2 and len(contr) == 2) or (l == 1 and contr == [2]):
                                    for y, w in enumerate(x.skill):       #if skills was chosen print available skills
                                        v = ''
                                        if y == 0:
                                            temp_menu = ['Skills:']
                                        if w.cooldown != 0:
                                            v = f' cooldown:{w.cooldown}'
                                        temp_menu.append(f'{y}. {w.stat_name} fnc:{w.fnc_name} for:{w.value} {v}')
                                    menu_print(temp_menu)
                                    sec_menu = 'Choose skill to use(type "ex" to quit"): '
                                    
                                v = input(sec_menu)
                                    
                                v, k = in_err_ch(v, len(temp_menu)-2)
                                
                                if k == 1:
                                    continue
                                elif k == 2 or k == 0:
                                    break
                                elif k == 3:
                                    m += 1
                                    continue
                                elif k == 4:
                                    m -= 1
                                    continue
                        if sp_atk:
                            if k == 2:
                                continue
                            
                            if l == 1 and 1 in contr:        #for magic
                                x.t_comm, l = x.magic[v].use()
                            elif (l == 2 and len(contr) == 2) or (l == 1 and contr == [2]):   #for skills
                                x.t_comm, l = x.skill[v].use()
                            
                            if l == 1:
                                continue
                            
                        del l, k, v, y, w, contr, sp_atk      #deleting excess variables
                        e = fight_end_check(g_gain, exp_gain, def_drop, prb_drop)
                        break
                    elif a == 3:
                        if held_items:
                            while True:
                                temp_menu = ['Available items:']
                                for y, w in enumerate(held_items):
                                    temp_menu.append(f'{y}. {w.stat_name}: function:{w.fnc_name} for:{w.x}')
                                menu_print(temp_menu)
                                
                                l = input('Choose (type "ex" to quit): ')
                                    
                                l, k = in_err_ch(l, len(temp_menu)-1)
                                
                                if k == 1:
                                    continue
                                elif k == 2 or k == 0:
                                    break
                                elif k == 3:
                                    m += 1
                                    continue
                                elif k == 4:
                                    m -= 1
                                    continue
                            if k == 2:
                                continue
                            
                            x.t_comm = held_items[l].use_item()
                            
                            del y, w, l, k
                            e = fight_end_check(g_gain, exp_gain, def_drop, prb_drop)
                            break
                        else:
                            menu_print(['','You do not hold any items'], 2, 2)
                            pause()
                            continue
                    elif a == 4:
                        menu_print(['You fleed from battle'])
                        pause()
                        z = 1
                        break
                elif x.team == 'enemies':
                    if settings['2'] == 0:      #setting for better AI
                        o = randint(0,len(team_1)-1)                                                  #enemy choosing random target
                        while team_1[o] == False or team_1[o].hp <= 0:
                            o = randint(0,len(team_1)-1)                                 #enemy choosing random target again if chose empty fighter place or fighter dead
                    else:
                        o, secondary = x.AI(x)
                        o = team_1.index(o)
                        
                        for y in team_2:              #telling helpers who to attack
                            if y.AI == AI_helper:
                                y.sugtarget = o          #sugma
                        
                    p = team_1[o]
                    dmg = x.deal_dmg()
                    team_1[o].take_dmg(dmg)
                    del dmg, p
                    
                    e = fight_end_check(g_gain, exp_gain, def_drop, prb_drop)      #checking if fight had already ended with control "e" as return
                    break
                
            if e == 'end':
                z = 1           #control number that breaks while loops
                break
            

        #-------------after everyone ended their turn-------------------------
        active_effects_cp = deepcopy(active_effects)      #making copy since it is impossible to change dict while iterating
        for x in active_effects_cp.values():         #loop checking for this turn effects and their duration
            x.check()
        
        for x in all_fghtr:          #reducing cooldown for skills by one
            for y in x.skill:
                y.cd_check()                #sp_skill turn check
        
        for x in all_fghtr:               #regenerate mana
            x.mana += x.mana_gain
            if x.mana > x.mana_max:      #prevent MANA OVERWHELMING
                x.mana = x.mana_max
        
        for x in all_fghtr:                 #known_passive
            if x.hp > 0:                   #for each living combatant
                for y in x.passive:           #and for each of his passives
                    v = y.activate()              #activate its effect
                    passive_comm.append(v)            #and add returned comment to one of the EoT lists
        
        #-----------------last fight end check-------------------
        if e != 'end':
            e = fight_end_check(g_gain, exp_gain, def_drop, prb_drop)      #checking if fight had already ended with control "e" as return
        
        if z == 1:                                              #if fight has ended
            for x in team_1 + team_2:                     #deleting variable for turn fighting
                del x.team

            if active_effects:                                   #if there are active effects
                active_effects_cp = deepcopy(active_effects)       #making copy since it is impossible to change dict while iterating
                for x in active_effects_cp.values():
                    x.end()                                    #forcefully ending effect
            break
        
        EoT_summ()

def shop(items, weapons, armor, red=0):
    global o, sell_red
    sell_red = red    #sell_reduction = percernage value reducing gold acquired from selling
    while True:
        
        temp_menu = [
        'Welcome to the shop',
        f'Current gold:{gold}',
        'What do you want to do here?',
        '1. Buy items',
        '2. Sell items',
        '3. Buy equipment',
        '4. Sell equipment',
        '5. Exit shop'
        ]
        
        menu_print(temp_menu)
        
        a = input('Choose: ')
        
        a, z = in_err_ch(a, len(temp_menu)-3, 1)
        
        if z == 1:
            continue
        elif z == 3:
            m += 1
        elif z == 4:
            m -= 1
            
        if a == 1:
            while True:
                temp_menu = ['Types of items available for sale:']
                y = -1
                d = []
                for x in items:
                    y += 1
                    temp_menu.append(f'{y}. {x}')
                    d.append(x)
                
                menu_print(temp_menu)
                
                o = input('Choose (type "ex" to quit): ')
                
                o, z = in_err_ch(o, len(temp_menu)-1)
                
                if z == 1:
                    z = 1
                    continue
                elif z == 2:
                    z = 1
                    break
                elif z == 3:
                    m += 1
                elif z == 4:
                    m -= 1
                elif z == 0:
                    break
                    
            l = o
            while z == 0:
                temp_menu = ['Which item do you want to buy?']
                y = -1
                v = items[d[l]]
                for x in v:
                    y += 1
                    temp_menu.append(f'{y}. {x.stat_name} function:{x.fnc_name} for:{x.x} cost:{x.cost}')
                
                menu_print(temp_menu)
                
                o = input('Choose (type "ex" to quit): ')
                
                o, z = in_err_ch(o, len(temp_menu)-1)
                
                if z == 1:
                    z = 0
                    continue
                elif z == 2:
                    break
                elif z == 3:
                    m += 1
                    z = 0
                    continue
                elif z == 4:
                    m -= 1
                    z = o
                    continue
                    
                v[o].buy_item()
                        
        elif a == 2:
            while True:
                sec_menu = [f'Value of items is reduced by {sell_red}% of basic cost']
                
                if held_items:
                    temp_menu = ['Your items:']
                    y = -1
                    for x in held_items:
                        y += 1
                        v = int(x.cost - x.cost * sell_red / 100)
                        temp_menu.append(f'{y}. {x.stat_name}: value:{stat_len(v, 3, 1)} function:{x.fnc_name} for:{x.x}')
                    
                    menu_print(temp_menu, 0, 0, sec_menu)
                    
                    o = input('Choose item for sale(type "ex" to quit): ')
                    
                    o, z = in_err_ch(o, len(temp_menu)-1)
                    
                    if z == 1:
                        continue
                    elif z == 2:
                        break
                    elif z == 3:
                        m += 1
                    elif z == 4:
                        m -= 1
                        
                    held_items[o].sell_item(sell_red)
                    
                elif not held_items:
                    menu_print(["But it doesn't matter right now since you don't hold any item that can be sold"], 1)
                    pause()
                    break
        elif a == 3:
            while True:
                temp_menu = ['Equipment for sale:']
                y = -1
                d = []
                for x in global_equipment:
                    y += 1
                    temp_menu.append(f'{y}. {x}')
                    d.append(x)
                
                menu_print(temp_menu)
                
                o = input('Choose (type "ex" to quit): ')
                
                o, z = in_err_ch(o, len(temp_menu)-1)
                
                if z == 1:
                    continue
                elif z == 2:
                    z = 1
                    break
                elif z == 3:
                    m += 1
                elif z == 4:
                    m -= 1
                elif z == 0:
                    z = 0
                    break

            if z == 1:
                continue
            l = o
            v = global_equipment[d[l]]
            while z == 0:
                if v == weapons:
                    temp_menu = ['Which weapon do you want to buy?']
                    y = -1
                    for x in v:
                        y += 1
                        temp_menu.append(f'{y}. {x.stat_name}: cost:{stat_len(x.cost, 3, 1)} damage:{x.stat_dmg} variable:{x.dmg_var} type:{x.dmg_type_1}, {x.dmg_type_2}')
    
                elif v == armor:
                    y = -1
                    temp_menu = ['Which armor do you want to buy']
                    for x in v:
                        y += 1
                        temp_menu.append(f'{y}. {x.stat_name}: cost:{stat_len(x.cost, 3, 1)} defence:{x.stat_defence}')
                
                menu_print(temp_menu)
                
                o = input('Choose(type "ex" to exit): ')
                
                o, z = in_err_ch(o, len(temp_menu)-1)
                
                if z == 1:
                    z = 0
                    continue
                elif z == 2:
                    break
                elif z == 3:
                    z = 0
                    m += 1
                elif z == 4:
                    z = 0
                    m -= 1
                    
                v[o].buy_equipment()
        elif a == 4:
            while True:
                
                sec_menu = [f'Value of equipment is reduced by {sell_red}% of basic cost']
                
                held_equipment = held_armor + held_weapons
                if held_equipment:
                    y = -1
                    v = -1
                    for x in held_equipment:
                        y += 1
                        if y == 0:
                            temp_menu = ['Held equipment:']
                        value = stat_len(int(x.cost - x.cost * sell_red / 100), 3, 1)
                        if type(x) == Weapon:
                            if v == -1:
                                temp_menu.append(' Weapons:')
                            temp_menu.append(f'  {y}. {x.stat_name} value:{value} damage:{x.stat_dmg}({x.dmg_var})')
                            v += 1
                        else:
                            if y == 0:
                                temp_menu.append(' Armor:')
                            temp_menu.append(f'  {y}. {x.stat_name} value:{value} defence:{x.stat_defence}')
                    
                    menu_print(temp_menu, 0, 0, sec_menu)
                    
                    o = input('Choose equipment to sell(type "ex" to quit): ')
                    
                    o, z = in_err_ch(o, y)
                    
                    if z == 1:
                        continue
                    elif z == 2:
                        break
                    elif z == 3:
                        m += 1
                    elif z == 4:
                        m -= 1
                    
                    if type(held_equipment[o]) == Weapon:
                        o -= y-v
                        held_weapons[o].sell_equipment()
                    else:
                        held_armor[o].sell_equipment()
                    pause()
                if not held_equipment:
                    menu_print(["But you don't have anything to sell"], 1)
                    pause()
                    break
                
        
        elif a == 5:
            menu_print(['You left the shop'])
            pause()
            break


#--------------------------------item function---------------------------------------------------
        #return None, target   #use when item used properly
        #return not_used_comm?    #use when not used
        
def revival(hp, c=0):  #hp for health after revivalion, c=0 for ally ress c=1 for enem ress
    global k
    while True:
        temp_menu = [f'Turn: {turn}', ''] + stat_print(0)
        y = -1    #for indexes
        z = []    #for checking if someone is actally dead
        
        if c == 0:
            target = team_1
        elif c == 1:
            target = team_2
        for char in target:
            y += 1
            if char.hp == 0:
                if not z:
                    sec_menu = ['Who do you want to revive?']
                sec_menu.append(f' {y}. {char.stat_name}- health:{char.stat_hp}/{char.stat_hp_max} attack:{char.atkmin}-{char.atkmax} total defence:{char.stat_defence}')
                z.append(y)
                
        if not z:         #-------------this may be used often in future(spoiler, it is, i think)-----------------------------
            menu_print(['No one is dead'], 1)
            pause()
            return f'{x.name} tried to find anyone that may be in dead need, but he just lost time(and a turn)', None        #see item>use_item
            #------------------return-when-unused--------------

        menu_print(temp_menu, 0, 0, sec_menu)
        
        o = input('Choose: ')
        
        o, l = in_err_ch(o, len(sec_menu)-1)
        
        if l == 1:
            continue
        elif l == 3:
            m += 1
        elif l == 4:
            m -= 1
            
        if o in z:
            target[o].hp += hp
            if target[o].hp > target[o].hp_max:
                target[o].hp = target[o].hp_max
            target[o].stat_hp = stat_len(target[o].hp, 3, 1)
            
            menu_print(temp_menu, 0, 0,[target[o].name + ' has been revived and has ' + str(target[o].hp) + ' health points'])
            pause()
            return None, target[o]        #see item>use_item
            #-------------return-when-all-good------------
        else:
            menu_print(['This character is not dead'], 1)
            pause()
            continue

def heal(x, c=0): #x for heal amount, c=0 for ally heal, c=2 for enem heal
    global t_target, temp_menu, sec_menu
    while True:
        temp_menu = [f'Turn: {turn}', ''] + stat_print(0)
        sec_menu = ['Who do you want to heal?']
        team_target(1, sec_menu)
        
        if c == 0:
            if team_1[o].hp == 0:
                menu_print(["You can't heal dead with this"], 1)
                pause()
                continue
            y = team_1[o]
        elif c == 1:
            if team_2[o].hp == 0:
                menu_print(["You can't heal dead with this"], 1)
                continue
            y = team_2[o]
            
        v = y.hp                                      #for print measures
        y.hp += x
        
        if y.hp > y.hp_max:                     #prevent overheal
            y.hp = y.hp_max
        y.stat_hp = stat_len(y.hp, 3, 1)
        
        l = y.hp                                      #for print measures
        menu_print([f'{y.name} has been healed for {l-v} health up to current {y.hp} health points'], 1)
        pause()
        return None, y        #see item>use_item
        #----------------return-if-good-------------


#to correctly use Effect in Item:
    #define (l_fnc that serves as a core of effect and does all the math(used in looping and end))
    #define (effect instance that takes in default duration, l_fnc and x(strength/healing etc.))
    #define (i_fnc that begins effect circulation and adds effect to active_effects)
    #define (item with i_fnc as its function)
#brain meltdown occured while making this

class Effect:           #consider doing deepcopies of it so multiple instances of the same effects can stack
    
    def __init__ (self, fnc):
        
        self.fnc = fnc    #function
        
    def start(self, char, dur=0):     #char is character passed down  (had to write this, my mind was melted after writing Effect)
        
        self.dur = dur
        self.time = self.dur
        self.char = char
        
        self.fnc(self.x, char, 1)   # '1' being option to begin effect
        
    def check(self):
        
        self.fnc(self.x, self.char)         #no third argument to check for effect(if exists)
        active_effects[self.key].time -= 1     #time left
        self.time -= 1
        if self.time == 0:
            self.end()
            
    def end(self):
        
        self.fnc(self.x, self.char, 2)   #2 being option to cancel effect(weaken/strengthen)
        del active_effects[self.key]       #why use pop, when you can use del :)

#----loop-fnc-used-in-Effect----
def l_atk_upp(x, char, c=0):      #(x=value, char=character, c==1 loop, c==2 end
    key = char.name             #why the hell does it work but global doesnt????
    char = all_fghtr_dict[key]
    if c == 1:   #start
        char.atk += x
        char.atkmin = stat_len(int(char.atkmin)+x, 2, 1)
        char.atkmax = stat_len(int(char.atkmax)+x, 2, 1)
#         print(char.name + ' attack was increased by ' + str(x))
        
    elif c == 2:   #end
        char.atk -= x
        char.atkmin = stat_len(int(char.atkmin)-x, 2, 1)
        char.atkmax = stat_len(int(char.atkmax)-x, 2, 1)
#         print(char.name + ' attack buff has ended')
    else:    #check
        True

def l_atk_down(x, char, c=0):
    key = char.name
    char = all_fghtr_dict[key]
    if c == 1:
        char.atk -= x
        char.atkmin = stat_len(int(char.atkmin)-x, 2, 1)
        char.atkmax = stat_len(int(char.atkmax)-x, 2, 1)
#         print(char.name + ' attack was decreased by ' + str(x))
    if c == 2:
        char.atk += x
        char.atkmin = stat_len(int(char.atkmin)+x, 2, 1)
        char.atkmax = stat_len(int(char.atkmax)+x, 2, 1)
#         print(char.name + ' attack debuff has ended')
    else:
        True

#_effect_fnc_
eff_atk_up = Effect(l_atk_upp)     #Effect(dur, fnc, x)
eff_atk_down = Effect(l_atk_down)

active_effects = {}
buff_count = 0

#_item_fnc_
def i_atk_up(z, y):            #works only for team_1
    global buff_count, t_target
    buff_count += 1                      #for creating keys
    key = str(buff_count)                   #creating new key
    
    active_effects[key] = deepcopy(eff_atk_up)    #making copy of effect+adding it to active_effects
    active_effects[key].x = z                 #assigning new x
    active_effects[key].key = key           #giving effect it's place in active effects to manipulate itself
    
    team_target(1, [f'Who does {x.name} want to increase attack of?'])
    v = team_1[o]                       #choosing target for effect
    active_effects[key].start(v, y)     #giving target and duration to effect and starting it
    return None, v        #see item>use_item
    #------------return-if-good-----------

def i_atk_down(z, y):            #works only for team_1
    global buff_count, t_target, passive_comm
    buff_count += 1        #for creating keys
    key = str(buff_count)  #creating new key
    
    active_effects[key] = deepcopy(eff_atk_down)    #making copy of effect+adding it to active_effects
    active_effects[key].x = z       #assigning new x
    active_effects[key].key = key    #giving effect it's place in active effects to manipulate itself
    
    team_target(2, [f'Who does {x.name} want to lower attack of?'])
    v = team_2[o]         #choosing target for effect
    active_effects[key].start(v, y)     #giving target and duration to effect and starting it
    return None, v        #see item>use_item
    #---------------------return-if-good----------------


#--------special attack functions parts---------------
#----------experiment---it should take less space to do functions from scrap------------
#sp h=header i=inner (f=footer) no footer present

#headers, they should be chosen only for deciding target
#return (variable that holds target), (comment version(name) of variable)
def sph_t1():
    return team_1, 'team 1'
def sph_t2():
    return team_2, 'team 2'
def sph_t1_targ():
    global p
    team_target(1, [f'Who does {x.name} target?'])
    target = team_1[o]
    p = target
    return target, target.name
def sph_t2_targ():
    global p
    team_target(2, [f'Who does {x.name} target?'])
    target = team_2[o]
    p = target
    return target, target.name

#inner function, these decide what actually special attack does
#return (part of turn comment)
def spi_dmg(target, q):   #(target=target from sph, q=value from sp_attack class itself)  (q is damageto be dealt)
    if type(target) == list:         #if target was as a list(either all or multiple)
        for y in target:
            y.take_dmg(q)
    elif type(target) == Char:      #if target is single(Character)
        target.take_dmg(q)
    return f'dealt {q} damage'

def spi_heal(target, q):        #q is amount of heal
    if type(target) == list:     #if targeting group
        for y in target:
            y.hp += q
            if y.hp > y.hp_max:    #prevent overheal
                y.hp = y.hp_max
            y.stat_set()         #i should make function inside Char that takes care of healing, seriously
    elif type(target) == Char:       #if targeting singularity
        target.hp += q
        if target.hp > target.hp_max:       #prevent overheal
            target.hp = target.hp_max
        target.stat_set()        #but i guess i will never read this again so. . . btw its 25.11.2019 here
    return f'restored {q} health'

def spi_atk_strong(target, q):   #stronger attack(q is multiplier)
    dmg = int(x.deal_dmg() * q)
    target.take_dmg(dmg)
    return f'dealt {dmg} damage'

def spi_atk_multi(target, q):   #for attacking multiple times  (q is attack number)
    t_dmg = 0                  #total damage in a turn
    for y in range(0, q):       #its a simple trick, but quite a potent one
        dmg = x.deal_dmg()
        target.take_dmg(dmg)
        t_dmg += dmg - target.defence     #summimg up total damage for turn comment
    return f'attacked {q} times and dealt a total of {t_dmg}'

def spi_atk_arm(target, q):   #attack penetrating armor(q is armor penetration)
    q = q if q < target.defence else target.defence
    dmg = x.deal_dmg() + q
    target.take_dmg(dmg)
    return f'dealt {dmg} damage'

#--------------for special attack gain-------------------------------
#partial brain meltdown while making this
#for more information about it(not the brain meltdwn) look for part of code, after which Char instances are defined
def sp_atk_lvl_up(tree, src, count, backup=[]):      #input tree, source sp_atk(__init__), which index +1 is on, old sp_atk
    out = []                                                          #list for output
    if len(tree)-1 < count:                                           #if last 'spell gain checkpoint' has already been reached
        return backup, [], []                                         #return old list
    for y, x in enumerate(tree[count]):                          #going over level of a tree      (y is spell family, x is spell level)
        if x != 0:                                                    #0 means no new sp_atk is gained
            x -= 1                                                    #reducing, so that basic spell is 0
            
            if type(src[0]) == list:                                  #------custom---------
                out.append(deepcopy(src[y][x]))                       #appending to skill_list deepcopy of a spell
            
            elif type(src[0]) in (SP_skill, SP_magic, SP_passive):    #------default------- #if no new sp_atk gain order is defined
                n_sp_atk = src[y]                                     #creating new basic skill
                
                while x >= n_sp_atk.level and n_sp_atk.upgrade != None:   #upgrading it till it can't be upgraded anymore
                    n_sp_atk = n_sp_atk.upgrade
                    
                out.append(deepcopy(n_sp_atk))                        #adding it to the list
    
    #------------adding commentary for sp_atk gain------------------
    y = 0
    upg_sp, new_sp = [], []
    for x, z in zip(backup, out):                        #comparing old and new list
        if x.ID != z.ID:
            upg_sp.append([x, z])                        #adding old and new sp_atk to return upgrade list
        y += 1
    else:                                                #if new spell was learnt
        if y < len(out):
            while y != len(out):
                new_sp.append(out[y])                    #adding it to new sp_atk list
                y += 1
                    
    return out, upg_sp, new_sp


#------------special attack class------------------
class SP_atk:
    
    def __init__(self, name, cost, sph, spi, fnc_name, value, level, upgrade):
        
        global ID
        self.ID = ID
        ID += 1
        self.name = name
        self.stat_name = stat_len(name, 7)
        self.cost = cost
        self.sph = sph
        self.spi = spi
        self.fnc_name = fnc_name
        self.value = value
        self.level = level
        self.upgrade = upgrade
#         self.target = target
        
#------------for each turn, (for start of battle not defined yet)-------------------
class SP_passive(SP_atk):
    
    def __init__(self, name, cost, sph, spi, fnc_name, value, level, upgrade):
        
        super().__init__(name, cost, sph, spi, fnc_name, value, level, upgrade)
        
    def activate(self):
        
        target, target_comm =  self.sph()
        action = self.spi(target, self.value)
        t_comm = f'{x.name} used {self.name} and {action} to {target_comm}'
        return t_comm


class SP_skill(SP_atk):
    
    def __init__(self, name, cost, sph, spi, fnc_name, value, cooldown, init_cooldown, level, upgrade):
        
        super().__init__(name, cost, sph, spi, fnc_name, value, level, upgrade)
        self.cooldown = init_cooldown
        self.max_cooldown = cooldown
        self.init_cooldown = init_cooldown
        
    def use(self):
        
        if self.cooldown == 0:                #if skill is available
            target, target_comm =  self.sph()
            action = self.spi(target, self.value)
            t_comm = f'{x.name} used {self.name} and {action} to {target_comm}'
            self.cooldown = self.max_cooldown
            opt = 0
        else:                                   #if skill is on cooldown
            menu_print([f"{x.name}s' {self.name} is still on cooldown."])
            pause()
            t_comm, opt = '', 1
        return t_comm, opt             #see item>use_item
    
    def cd_check(self):
        
        self.cooldown -= 1
        if self.cooldown < 0:
            self.cooldown = 0

class SP_magic(SP_atk):
    
    def __init__(self, name, cost, sph, spi, fnc_name, value, m_cost, level, upgrade):    #m_cost = mana cost
        
        super().__init__(name, cost, sph, spi, fnc_name, value, level, upgrade)
        self.m_cost = m_cost
        
    def use(self):
        
        if x.mana >= self.m_cost:          #if mage has enough mana pool
            x.mana -= self.m_cost
            target, target_comm =  self.sph()
            action = self.spi(target, self.value)
            t_comm = f'{x.name} used {self.name} and {action} to {target_comm}'
#             t_comm = self.fnc(self.value, self.target)
            opt = 0
        else:                             #if there is not enough mana
            t_comm = ''
            menu_print([f'{x.name} does not have enough mana to cast {self.name}.'])
            pause()
            opt = 1
        return t_comm, opt              #see item>use_item


#define special attacs from highest level to lowest, so that no exceptions will occur in the initialisation
#---magic attacks---
#                   SP_magic(name, cost, sph, spi, fnc_name, value, m_cost, level, upgrade)
sp_m_heal_all_v3 = SP_magic('Heal all v3', 0, sph_t1, spi_heal, 'heal', 20, 100, 3, None)
sp_m_heal_all_v2 = SP_magic('Heal all v2', 0, sph_t1, spi_heal, 'heal', 15, 75, 2, sp_m_heal_all_v3)
sp_m_heal_all_v1 = SP_magic('Heal all v1', 0, sph_t1, spi_heal, 'heal', 10, 40, 1, sp_m_heal_all_v2)

sp_m_dmg_all_v3 = SP_magic('Damage all v3', 0, sph_t2, spi_dmg, 'dmg', 11, 100, 3, None)
sp_m_dmg_all_v2 = SP_magic('Damage all v2', 0, sph_t2, spi_dmg, 'dmg', 9,  70, 2, sp_m_dmg_all_v3)
sp_m_dmg_all_v1 = SP_magic('Damage all v1', 0, sph_t2, spi_dmg, 'dmg', 7,  50, 1, sp_m_dmg_all_v2)

#---skill attacks---
               #SP_skill(name, cost, sph, spi, fnc_name, value, cooldown, init_cooldown, level, upgrade):
sp_s_atk_pent = SP_skill('Pentuple attack', 0, sph_t2_targ, spi_atk_multi, 'atk', 5, 6, 4, 4, None)
sp_s_atk_quad = SP_skill('Quaruple attack', 0, sph_t2_targ, spi_atk_multi, 'atk', 4, 5, 3, 3, sp_s_atk_pent)
sp_s_atk_tripl = SP_skill('Triple attack',  0, sph_t2_targ, spi_atk_multi, 'atk', 3, 5, 2, 2, sp_s_atk_quad)
sp_s_atk_doubl = SP_skill('Double attack',  0, sph_t2_targ, spi_atk_multi, 'atk', 2, 3, 1, 1, sp_s_atk_tripl)

sp_s_atk_v4 = SP_skill('Strong attack v4', 0, sph_t2_targ, spi_atk_strong, 'atk', 2.0, 6, 4, 4, None)
sp_s_atk_v3 = SP_skill('Strong attack v3', 0, sph_t2_targ, spi_atk_strong, 'atk', 1.7, 5, 3, 3, sp_s_atk_v4)
sp_s_atk_v2 = SP_skill('Strong attack v2', 0, sph_t2_targ, spi_atk_strong, 'atk', 1.5, 4, 2, 2, sp_s_atk_v3)
sp_s_atk_v1 = SP_skill('Strong attack v1', 0, sph_t2_targ, spi_atk_strong, 'atk', 1.3, 3, 2, 1, sp_s_atk_v2)

sp_s_atk_arm_v4 = SP_skill('Armor piercing attack v4', 0, sph_t2_targ, spi_atk_arm, 'atk', 5, 5, 2, 4, None)
sp_s_atk_arm_v3 = SP_skill('Armor piercing attack v3', 0, sph_t2_targ, spi_atk_arm, 'atk', 4, 4, 2, 3, sp_s_atk_arm_v4)
sp_s_atk_arm_v2 = SP_skill('Armor piercing attack v2', 0, sph_t2_targ, spi_atk_arm, 'atk', 3, 4, 2, 2, sp_s_atk_arm_v3)
sp_s_atk_arm_v1 = SP_skill('Armor piercing attack v1', 0, sph_t2_targ, spi_atk_arm, 'atk', 2, 3, 2, 1, sp_s_atk_arm_v2)

#---passive attacks---
                  #SP_passive(name, cost, sph, spi, fnc_name, value, level, upgrade)
sp_p_heal_all_v4 = SP_passive('Passive heal allies v4', 0, sph_t1, spi_heal, 'heal', 4, 4, None)
sp_p_heal_all_v3 = SP_passive('Passive heal allies v3', 0, sph_t1, spi_heal, 'heal', 3, 3, sp_p_heal_all_v4)
sp_p_heal_all_v2 = SP_passive('Passive heal allies v2', 0, sph_t1, spi_heal, 'heal', 2, 2, sp_p_heal_all_v3)
sp_p_heal_all_v1 = SP_passive('Passive heal allies v1', 0, sph_t1, spi_heal, 'heal', 1, 1, sp_p_heal_all_v2)

sp_p_dmg_all_v4 = SP_passive('Passive damage enemies v4', 0, sph_t2, spi_dmg, 'dmg', 4, 4, None)
sp_p_dmg_all_v3 = SP_passive('Passive damage enemies v3', 0, sph_t2, spi_dmg, 'dmg', 3, 3, sp_p_dmg_all_v4)
sp_p_dmg_all_v2 = SP_passive('Passive damage enemies v2', 0, sph_t2, spi_dmg, 'dmg', 2, 2, sp_p_dmg_all_v3)
sp_p_dmg_all_v1 = SP_passive('Passive damage enemies v1', 0, sph_t2, spi_dmg, 'dmg', 1, 1, sp_p_dmg_all_v2)

global_passive = [sp_p_heal_all_v1, sp_p_heal_all_v2, sp_p_heal_all_v3, sp_p_heal_all_v4,
                  sp_p_dmg_all_v1, sp_p_dmg_all_v2, sp_p_dmg_all_v3, sp_p_dmg_all_v4]

global_skill = [sp_s_atk_doubl, sp_s_atk_tripl, sp_s_atk_quad, sp_s_atk_pent,
                 sp_s_atk_v1, sp_s_atk_v2, sp_s_atk_v3, sp_s_atk_v4]

global_magic = [sp_m_heal_all_v1, sp_m_heal_all_v2, sp_m_heal_all_v3,
                sp_m_dmg_all_v1, sp_m_dmg_all_v2, sp_m_dmg_all_v3]
# known_passive, known_magic, known_skill = [], [], []

all_id_class += global_passive + global_skill + global_magic         #for checking all ID

#------------------equipment class------------------
class Weapon:
    
    def __init__ (self, name, cost, dmg, dmg_var, dmg_type_1, dmg_type_2='none', ohe='', ohe_name='', ohe_value=0):
        
        global ID
        self.name = name
        self.stat_name = stat_len(name, 10)   #for stat purpose
        
        self.ID = ID       #for sorting
        ID += 1
        
        self.cost = cost
        self.dmg = dmg
        self.stat_dmg = stat_len(dmg, 3, 1)   #for stat purpose
        self.dmg_var = dmg_var
        
        self.dmg_type_1 = dmg_type_1
        self.dmg_type_2 = dmg_type_2
        
        self.ohe = ohe              #on hit effect
        self.ohe_name = ohe_name
        self.ohe_value = ohe_value              #on hit effect value
        
    def equip(self, char):
        
        char.weapon = self
        char.atk += self.dmg
        char.atk_var += self.dmg_var
        
        char.atkmin = char.atk - char.atk_var           #atkmin and atkmax are for status display
        char.atkmax = char.atk + char.atk_var
        
        char.dmg_type_1 = self.dmg_type_1         #for future elemental system
        char.dmg_type_2 = self.dmg_type_2
        char.stat_set()
        
    def buy_equipment(self):
        
        global gold          #accesing held gold outside of function
        menu_print([])
        p = f'Are you sure you want to buy: {self.name}? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:        #checking if enough gold is held
                gold -= self.cost
                held_weapons.append(self)    #adding itself to held weapons
                
                temp_menu = [
                f'You have bought {self.name}.',
                f'You currently have {gold} gold.'
                ]
                
                p = 'You are currently holding '
                held_weapons.sort(key = sortid)        #sorting held weapons
                for x in held_weapons:
                    p = p + x.name + ', '           #and displaying all of them
                temp_menu.append(p)
                menu_print(temp_menu)
                pause()
            else:
                menu_print(['You do not have enough gold'], 1)
                pause()
                
    def sell_equipment(self):
        
        global gold, held_weapons
        menu_print([])
        p = f'Are you sure you want to sell: {self.name}? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            g_gained = int(self.cost - self.cost * sell_red / 100)
            gold += g_gained
            held_weapons.pop(o)
            menu_print([f'You sold {self.name} and gained {g_gained} gold'], 1)

#---------on hit effects------------------
def ohe_atk_heal(dmg, percent):
    global all_fghtr_dict
    dmg_heal = int(dmg * percent / 100)
    overheal = -x.hp_max + x.hp + dmg_heal
    dmg_heal -= overheal if overheal > 0 else 0
    
    x.hp += dmg_heal
    if dmg_heal > 0:
        x.t_comm += f' and healed himself for {dmg_heal} hp'
        x.stat_set()



class Armor:
    
    def __init__(self, name, cost, defence, defence_type='none'):
        
        global ID
        self.name = name
        self.stat_name = stat_len(name, 10)   #for stat purpose
        
        self.ID = ID  #for sorting
        ID += 1
        
        self.cost = cost
        self.defence = defence
        self.stat_defence = stat_len(defence, 3, 1)   #for stat purpose
        self.defence_type = defence_type
        
    def equip(self, char):
        
        char.armor = self
        char.defence += self.defence
        if char.defence_type_1 =='none':        #for future elemental system
            char.defence_type_1 = self.defence_type
        else:
            char.defence_type_2 = self.defence_type
        char.stat_set()
        
    def buy_equipment(self):
        
        global gold          #accesing held gold outside of function
        menu_print([])
        p = f'Are you sure you want to buy: {self.name}? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:        #checking if enough gold is held
                gold -= self.cost
                held_armor.append(self)    #adding itself to held armor
                
                temp_menu = [
                f'You have bought {self.name}.',
                f'You currently have {gold} gold.'
                ]
                
                p = 'You are currently holding '
                held_armor.sort(key = sortid)        #sorting held armor
                for x in held_armor:
                    p = p + x.name + ', '           #and displaying all of it
                temp_menu.append(p)
                menu_print(temp_menu)
                pause()
            else:
                menu_print(['You do not have enough gold'], 1)
                pause()
                
    def sell_equipment(self):
        
        global gold, held_armor
        menu_print([])
        p = f'Are you sure you want to sell: {self.name}? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            g_gained = int(self.cost - self.cost * sell_red / 100)
            gold += g_gained
            held_armor.pop(o)
            menu_print(['You sold {self.name} and gained {g_gained} gold'], 1)
            

#-----Weapon-----
#----user-weapons----
basic = Weapon('None', 0, 0, 0, 'blunt')        #(name, cost, dmg, dmg_var, dmg_type_1, dmg_type_2='None', ohe)
bat = Weapon('Bat', 50, 1, 1, 'blunt')
mace = Weapon('Mace', 90, 2, 0, 'blunt')
sword = Weapon('Sword', 170, 4, 0, 'slash')
hammer = Weapon('Hammer', 150, 3, 1, 'blunt')
flail = Weapon('Flail', 270, 6, 3, 'blunt')
bardiche = Weapon('Bardiche', 350, 8, 1, 'slash')
heal_sword = Weapon('Healing sword', 250, 3, 2, 'slash', 'none', ohe_atk_heal, 'lifesteal', 20)
creator_touch = Weapon('"Begone"', 9999, 150, 0, 'god')

#----momster-weapons----
imp_bas_wep = Weapon('None', 0, 0, 0, 'slash')
imp_lig_wep = Weapon('Light', 0, 1, 2, 'slash', 'fire')
imp_med_wep = Weapon('Medium', 0, 2, 3, 'blunt', 'fire')
imp_goo_wep = Weapon('Good', 0, 4, 0, 'pierce')

dem_bas_wep = Weapon('None', 0, 0, 0, 'slash')
dem_lig_wep = Weapon('Light', 0, 1, 0, 'pierce')
dem_med_wep = Weapon('Medium', 0, 2, 1, 'pierce')
dem_goo_wep = Weapon('Good', 0, 5, 1, 'blunt')

global_weapons = [bat, mace, sword, hammer, heal_sword, flail, bardiche, creator_touch]   #for shop display
global_weapons.sort(key = sortid)

dev_global_weapons = [imp_bas_wep, imp_lig_wep, imp_med_wep, imp_goo_wep, dem_bas_wep, dem_lig_wep, dem_med_wep, dem_goo_wep,
                 basic, bat, sword, hammer, mace, bardiche, flail, heal_sword, creator_touch]   #overall list for all weapons
all_id_class += dev_global_weapons   #for checking all ID
del dev_global_weapons

#-----Armor------
#----user-armor----
basal = Armor('None', 0, 0)  #name cost defence defence_type='none'
light = Armor('Light armor', 100, 1)
medial = Armor('Medium armor', 200, 3)
heavy = Armor('Heavy armor', 350, 5)
creator_skin = Armor('"Useless"', 9999, 50, 'god')

#----monster-armor
imp_bas_arm = Armor('None', 0, 0)
imp_lig_arm = Armor('Light', 0, 1)
imp_med_arm = Armor('Medium', 0, 3)
imp_goo_arm = Armor('Good', 0, 5)
imp_vgo_arm = Armor('Very good', 0, 8, 'shadow')

dem_bas_arm = Armor('None', 0, 0)
dem_lig_arm = Armor('Light', 0, 2)
dem_med_arm = Armor('Medium', 0, 4)
dem_goo_arm = Armor('Good', 0, 5)
dem_vgo_arm = Armor('Very good', 0, 7)

global_armor = [light, medial, heavy, creator_skin]  #for shop display
global_armor.sort(key = sortid)

dev_global_armor = [imp_bas_arm, imp_lig_arm, imp_med_arm, imp_goo_arm, imp_vgo_arm, dem_bas_arm, dem_lig_arm, dem_med_arm,
                    dem_goo_arm, dem_vgo_arm, light, basal, medial, heavy, creator_skin]  #overall list of all armor
all_id_class += dev_global_armor      #for showing all ID
del dev_global_armor

global_equipment = {
    'Weapons': global_weapons,
    'Armor': global_armor
    }

held_weapons = [bat, sword, hammer, heal_sword]
held_armor = [light, heavy, heavy]

if dev_opt == 'xel':
    held_weapons += [creator_touch, creator_touch, creator_touch]
    held_armor += [creator_skin, creator_skin, creator_skin]

#-------------------------------------enemy-AI----------------------------
#AI only works for enemies

# def AI_name(char):     #char is for passing down attack order/directory
#     AI_target, AI_secon = None, None  #AI_target is for character target of attack, AI_secon is unused
#
#     here put what it does
#
#     return AI_target, AI_secon         #using y.sugtarget for target suggestion

def AI_random(char):       #'if i wound anyone, i will be satisfied'
    AI_target, AI_secon = None, None
    
    while True:
        y = randint(0,len(team_1)-1)                              #automatic choose of random target
        if team_1[y].hp == 0:
            continue                 #if chosen fighter is dead
        break
    AI_target = team_1[y]
    
    return AI_target, AI_secon

def AI_weakfirst(char):         #'weaklings will die'       #there may be another similar to this but using defence
    AI_target, AI_secon, y = None, None, 0
    
    target_list = team_1
    sort = lambda char : char.hp
    target_list.sort(key = sort)
    
    while True:
        if target_list[y].hp == 0:
            y += 1
            continue
        break
    
    AI_target = target_list[y]
    
    return AI_target, AI_secon

def AI_strongfirst(char):   #'strong ones are scary, they should not exist'
    AI_target, AI_secon, y = None, None, 0
    
    target_list = team_1
    sort = lambda char : char.atk + char.atk_var
    
    target_list.sort(key = sort)
    target_list = target_list[::-1]
    
    while True:
        if target_list[y].hp == 0:
            y += 1
            continue
        break
    
    AI_target = target_list[y]
    
    return AI_target, AI_secon

def AI_onetarg(char):       #'this one is mine'   #attacks one target until it's dead
    AI_target, AI_secon = None, None
    
    if turn == 1 or team_1[char.sugtarget].hp == 0:
        while True:                 #cropped from AI_random
            AI_target = randint(0,len(team_1)-1)
            if team_1[AI_target].hp == 0:
                continue                 #if chosen fighter is dead
            char.sugtarget = AI_target
            break
        
    AI_target = team_1[char.sugtarget]
    
    return AI_target, AI_secon

def AI_command(char):
    AI_target, AI_secon = None, None
    
    while True:                       #choosing target for commander
        y = randint(0,len(team_1)-1)                              #automatic choose of random target
        if team_1[y].hp == 0:
            continue                 #if chosen fighter is dead
        break
    
    for x in team_2:               #giving order to servants
        if x.AI == AI_servant:
            x.sugtarget = y
    
    AI_target = team_1[y]
    
    return AI_target, AI_secon

def AI_servant(char):
    AI_target, AI_secon = None, None
    
    for z in range(0, len(team_1)):    #without this if char.sugtarget == 0 target  would be randomised
        if char.sugtarget == z:
            z = True
            break
    
    try:
        emptyinput = team_1[char.sugtarget]
    except:
            while True:
                y = randint(0,len(team_1)-1)
                if team_1[y].hp == 0:
                    continue                 #if chosen fighter is dead
                break
    else:
        if z != True or team_1[char.sugtarget].hp == 0:        #if char.sugtarget is chosen and is alive this does not execute
            while True:
                y = randint(0,len(team_1)-1)
                if team_1[y].hp == 0:
                    continue                 #if chosen fighter is dead
                break
        else:
            y = char.sugtarget
            
    AI_target = team_1[y]
    
    return AI_target, AI_secon

def AI_helper(char):
    AI_target, AI_secon = None, None
    
    for z in range(0, len(team_1)):    #without this if char.sugtarget == 0 target  would be randomised
        if char.sugtarget == z:
            z = True
            break
    
    try:
        emptyinput = team_1[char.sugtarget]
    except:
            while True:
                y = randint(0,len(team_1)-1)
                if team_1[y].hp == 0:
                    continue                 #if chosen fighter is dead
                break
    else:
        if z != True or team_1[char.sugtarget].hp == 0:        #if char.sugtarget is chosen and is alive this does not execute
            while True:
                y = randint(0,len(team_1)-1)
                if team_1[y].hp == 0:
                    continue                 #if chosen fighter is dead
                break
        else:
            y = char.sugtarget

    AI_target = team_1[y]
    
    
    return AI_target, AI_secon

#----i may do 'class' types just because some of character do not use some values or use mass[]
class Char:
    
    def __init__ (self, name, hp_max, atk, atk_var, recr_cost=0, g_drop=0, exp_drop=0, def_drop=[], prb_drop=[],
                  mana_max=0, mana_gain=5, defence=0,
                  defence_type_1='none', weapon=basic, armor=basal, AI=AI_random,
                  skill=[], skill_tree=[], magic=[], magic_tree=[], passive=[], passive_tree=[], tree_step=[]):
        
        global ID
        self.ID = ID                               #instance ID
        ID += 1                                    #increasing class ID counter
        
        self.name = name                                 #name(duh...)

        self.hp_max = hp_max                              #maximum health
        self.hp = hp_max                                 #current health
        
        self.atk = atk                                 #attack variable
        self.atk_var = atk_var                         #attack variable variable (try to comprehand this)
        self.atkmin = atk - atk_var                    #minimal attack possibility(used only in stat)
        self.atkmax = atk + atk_var                    #maximal attack possibility(used only in stat)
        
        self.recr_cost = recr_cost                    #recruitment cost

        self.g_drop = g_drop                          #gold drop variable
        
        self.exp_drop = exp_drop                      #experience gained for killing
        self.total_exp = 0          #total experience used in save/load
        self.exp = 0              #experience on current level
        self.level = 1       #current level (duh...)
        
        self.def_drop = def_drop          #definitive drop table
        self.prb_drop = prb_drop          #probable drop table
        
        self.mana_max = mana_max       #for using sp_magic #maximal mana
        self.mana = self.mana_max       #current mana
        self.mana_gain = mana_gain       #mana gain per turn
        
        self.defence = defence                             #setting innate defence

        self.base_hp_max = hp_max         #base/starting values for when something will bet out of control or when i will be too lazy
        self.base_atk = atk
        self.base_armor = armor
        self.base_atk_var = atk_var
        self.base_mana_max = mana_max
        self.base_mana_gain = mana_gain

        self.defence_type_1 = defence_type_1              #future elemental system?
        self.defence_type_2 = 'none'
        self.armor = armor               #default armor
        armor.equip(self)

        
#         self.dmg_type_1 = dmg_type_1                                     #damage type for future(?) elemental system
#         self.dmg_type_2 = dmg_type_2                #these are defined by weapon.equip() and char.unequip weapon() and same for armor
        
        self.t_comm = f'{self.name} did not have a chance to attack'          #turn comment if character died without taking action
        self.weapon = weapon        #default weapon
        weapon.equip(self)
        
        self.AI = AI
        self.sugtarget = None          #suggested target for 'advanced' AI
        
        
        self.skill_src = skill
        self.magic_src = magic
        self.passive_src = passive
        
        
        self.skill, self.magic, self.passive = [], [], []
        
        if not skill_tree:
            for y, x in enumerate(skill):
                if type(x) is SP_skill:
                    self.skill.append(deepcopy(x))
                else:
                    for z in skill[y]:
                        self.skill.append(deepcopy(z))
        else:
            self.skill, *empty = sp_atk_lvl_up(skill_tree, self.skill_src, 0)
        
        if not magic_tree:
            for y, x in enumerate(magic):
                if type(x) is SP_magic:
                    self.magic.append(deepcopy(x))
                else:
                    for z in magic[y]:
                        self.magic.append(deepcopy(z))
        else:
            self.magic, *empty = sp_atk_lvl_up(magic_tree, self.magic_src, 0)
        
        if not passive_tree:
            for y, x in enumerate(passive):
                if type(x) is SP_passive:
                    self.passive.append(deepcopy(x))
                else:
                    for z in passive[y]:
                        self.passive.append(deepcopy(z))
        else:
            self.passive, *empty = sp_atk_lvl_up(passive_tree, self.passive_src, 0)
        
        self.skill_tree = skill_tree
        self.magic_tree = magic_tree
        self.passive_tree = passive_tree
        
        self.tree_step = tree_step                    #at which lvl skill gain occur (steps of trees)
        
        self.stat_set()       #settig stat_* variables for showing in 'tables'
        
    def take_dmg (self, damage):
        
        self.hp -= damage                     #character taking damage(duh...)
        if self.hp < 0:                              #health can't be lower than zero
            self.hp = 0
        self.stat_set()                                 #setting stat variables
        
    def deal_dmg (self):
        
        atk_var = randint(0,self.atk_var*2) - self.atk_var             #making variable for damage
        atk_dmg = self.atk + atk_var
        
        if settings['1'] == 1:      #for fighting wiht or without type system
            dmg_bon, dmg_red = type_check(self, p, atk_dmg)    #checks if weapon has basic type(blunt, slash, pierce)
            atk_dmg = atk_dmg + dmg_bon - dmg_red - p.defence       #applies bonus and reduction
        else:
            atk_dmg = self.atk + atk_var - p.defence                                          #calculating damage from atk and variable
            
        if atk_dmg <= 0:
            atk_dmg = 0
            self.t_comm = (f'{self.name} dealt no damage to {p.name}')                     #turn comment used in EoT_summ
        else:
            self.t_comm = (f'{self.name} dealt {atk_dmg} damage to {p.name}')                      #turn comment used in EoT_summ
            if self.weapon.ohe != '':
                self.weapon.ohe(atk_dmg, self.weapon.ohe_value)                             #using effect of weapon

        return atk_dmg
    
    def heal_up(self):
        
        self.hp = self.hp_max
        self.mana = self.mana_max
        self.stat_set()
        
    def unequip_weapon(self):
        
        self.atk -= self.weapon.dmg
        self.atk_var -= self.weapon.dmg_var
        
        self.atkmin = self.atk - self.atk_var
        self.atmax = self.atk + self.atk_var
        
        self.dmg_type_1 = 'blunt'
        self.dmg_type_2 = 'none'
        basic.equip(self)
        self.stat_set()
        
    def unequip_armor(self):
        
        self.defence -= self.armor.defence
        if self.defence_type_2 != 'none':   #future elemental system?
            self.defence_type_2 = 'none'
        else:
            self.defence_type_1 = 'none'
        if self.armor != basal:
            held_armor.append(self.armor)
        basal.equip(self)
        self.stat_set()
        
    def recruit(self):
        
        global gold, team_1
        if gold >= self.recr_cost:
            menu_print([])
            p = f'Are you sure you want to recruit {self.name} for {self.recr_cost}? (type "yes" to confirm) '
            o = input(p)
            if o == 'yes':
                gold -= self.recr_cost
                team_1.append(self)
                global_allies.remove(self)
                menu_print([f'{self.name} has been recruited'], 1)
                pause()
        else:
            menu_print([f"You don't have enough money to recruit {self.name}"], 1)
            pause()
            
    def level_up_check(self, a=0):
        
        global temp_menu     #for inner comm() fnc
        
        exp_needed = 200*self.level          #formula for calculating required experience
        
        while self.exp >= exp_needed:               #if required experience is gained and while it is bigger than requirments
            self.level += 1
            self.exp -= exp_needed              #reducing total exp by amount needed for previous level
            exp_needed = 200 * self.level     #experience needed for next level
            if a == 0:
                global temp_menu
                temp_menu.append(f'{self.name} reached level {self.level}')
            
            lvl_change_dict = {
                'hp': [0, self.base_hp_max, self.hp_max, 15, 10],     #zero serves as index, first in list is stat without equipment/buff/skill
#                 'atk': [1, self.base_atk, self.atk, 2, 1],         #, second is stat that is used commonly(----------unused now---------- i tried to use it this way, but it didn't work)
                'mana': [2, self.base_mana_max, self.mana_max, 15, 10], # , third is maximum gain, when it is met it is reduced by fourth value
#                 'mana gain': [3, self.base_mana_gain, self.mana_gain, 4, 2]
                }
            #--------------------stat gain-----------------------
            for x in lvl_change_dict:    #increasing statistics
                index     = lvl_change_dict[x][0]     #setting variables
                stat      = lvl_change_dict[x][1]
                limit     = lvl_change_dict[x][3]
                decrease  = lvl_change_dict[x][4]
            
                y = int(stat*0.1)
                if y == 0:            #prevents from gain being 0
                    y = 1
                while y > limit:      #limits gain
                    y -= decrease
                    
                if index == 0:           #adds gain to stat
                    self.base_hp_max += y
                    self.hp_max += y
                elif index == 1:
                    self.base_atk += y
                    self.atk += y
                elif index == 2 and stat != 0:
                    self.base_mana_max += y
                    self.mana_max += y
                elif index == 3 and stat != 0:
                    self.base_mana_gain += y
                    self.mana_gain += y
                    
            #--------------sp_atk gain--------------------------
            z = 0
            
            if self.level in self.tree_step:                         #if tree exist, and level matches one of those in list
                count = self.tree_step.index(self.level) + 1
                z = 1
            if self.level % 5 == 0 and not self.tree_step:      #if there is no tree_step specified #new spell gain process
                count = int(self.level / 5)             #counter for level of 'tree'
                z = 1
                
            if z == 1:
                def comm(name, upg, new):
                    if a == 0:
                        global temp_menu
                        for x in upg:
                            temp_menu.append(f"{name}s' {x[0].name} was upgraded to {x[1].name} ")
                        for x in new:
                            temp_menu.append(f'{name} learnt {x.name}')
                            
                if self.skill_tree:      #if skill tree is defined
                    self.skill, upg, new = sp_atk_lvl_up(self.skill_tree, self.skill_src, count, self.skill)
                    #                       A A A A A A whole function designed to handle sp_atk gain
                    comm(self.name, upg, new)   #comments later added printed in fight end
                    
                if self.magic_tree:
                    self.magic, upg, new = sp_atk_lvl_up(self.magic_tree, self.magic_src, count, self.magic)
                    comm(self.name, upg, new)
                    
                if self.passive_tree:
                    self.passive, upg, new = sp_atk_lvl_up(self.passive_tree, self.passive_src, count, self.passive)
                    comm(self.name, upg, new)
                    
            self.stat_set()     #sets stat variables
            self.heal_up()      #sets health to max
            
    def stat_set(self):
        
        self.stat_name = stat_len(self.name, 14)   #may fall out of use since 0.3.004d #what did i mean writing this?
        self.stat_hp_max = stat_len(self.hp_max, 3)
        self.stat_hp = stat_len(self.hp, 3, 1)
        self.atkmin = stat_len(self.atk - self.atk_var, 2, 1)
        self.atkmax = stat_len(self.atk + self.atk_var, 2)
        self.stat_defence = stat_len(self.defence, 3, 1)
        self.stat_mana_max = stat_len(self.mana_max, 3, 1)
        self.stat_mana = stat_len(self.mana, 3, 1)
        self.stat_mana_gain = stat_len(self.mana_gain, 1)



class Item:
    
    def __init__ (self, name, cost, fnc_name, fnc, x, w=0):
        
        #fnc is a function, that said item will do. These functions have to be defined.
        global ID
        self.name = name
        self.stat_name = stat_len(name, 20) #for stat purpose
        
        self.ID = ID   #for sorting
        ID += 1

        self.cost = cost
        
        self.fnc_name = stat_len(fnc_name, 8)   #for stat purpose
        self.fnc = fnc           #function assigned to item
        self.x = x         #variables used it self.fnc
        self.w = w
        
    def use_item (self):
        
        global held_items, passive_comm
        t_comm, o = self.fnc(self.x, self.w)    #using function assigned to itself
        
        try:
            if self.fnc.__name__[:1] == 'i':          #getting function name as string
                passive_comm.append(f'{self.name} now affects {o.name}')     #for printing at EoT_summ
                
            if t_comm == None:                          #if item was actually used
                held_items.pop(l)                    #deleting self from list
                return(x.name + ' used ' + self.name + ' on ' + o.name)
            else:
                raise Exception('t_comm is present')
        except:
            return t_comm
        
    def buy_item (self):
        
        global gold                                    #accesing held gold outside of function
        menu_print([])
        p = f'Are you sure you want to buy: {self.name}? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:                    #checking if enough gold is held
                gold -= self.cost
                held_items.append(self)                 #adding itself to held items
                
                temp_menu = [
                f'You have bought {self.name}',
                f'You currently have {gold} gold'
                ]
                
                p = 'You are currently holding '
                held_items.sort(key = sortid)                   #sorting held items
                for x in held_items:
                    p += f'{x.name}, '                        #and displaying all of them
                temp_menu.append(p)
                menu_print(temp_menu)
                pause()
            else:                                            #if you don't have enough gold
                menu_print(['You do not have enough gold'], 1)
                pause()
                
    def sell_item(self, sell_red):                             #red == value reduction
        
        global gold, held_items
        menu_print([])
        p = f'Are you sure you want to sell: {self.name}? (type yes to confirm) '
        a = input(p)
        if a == 'yes':
            g_gained = int(self.cost - self.cost * sell_red / 100)        #reducing gold gained by value reduction
            gold += g_gained
            held_items.pop(o)
            menu_print([f'You sold {self.name} and gained {g_gained} gold'], 1)
            pause()


#------------------------------settings----------------------------
m = 1 #for menu page
typecheck = 1
enemAI = 1
settings = {
    '1': typecheck,     #for damage type calculation
    '2': enemAI       #for enemy AI
    }

savename = 'savefile.txt'

#weapons are defined with class
#--------------------------items------------------------------
potion = Item('Potion', 12, 'heal', heal, 10)        #Item(name, cost, fnc_name, fnc, x(fnc_attrib)) 
potionv2 = Item('Potion v2', 23, 'heal', heal, 20)
potionv3 = Item('Potion v3', 45, 'heal', heal, 30)

atk_potion = Item('Attack potion', 100, 'atk up', i_atk_up, 3, 6)
atk_potionv2 = Item('Attack potion v2', 180, 'atk up', i_atk_up, 5, 4)

weak_potion = Item('Weakening potion', 120, 'atk down', i_atk_down, 2, 6)
weak_potionv2 = Item('Weakening potion v2', 170, 'atk down', i_atk_down, 4, 4)

revival_potion = Item('Revival potion', 50, 'revival', revival, 20)
revivalv2_potion = Item('Revival potion v2', 150, 'revival', revival, 40)
revivalfull_potion = Item('Full revival potion', 300, 'revival', revival, 500)

held_items = [potionv2, atk_potion, weak_potion, revivalfull_potion]                      #defining held items
held_items.sort(key = sortid)

buff_items = [atk_potion, atk_potionv2]
debuff_items = [weak_potion, weak_potionv2]
healing_items = [potionv2, potion, potionv3, revival_potion, revivalv2_potion, revivalfull_potion]        #defining list of healing items


global_items = {                                            #using dictionary for easier manipulation
    'Healing items': healing_items,
    'Buff items': buff_items,
    'Debuff items': debuff_items
    }
for x in global_items.values():
    x.sort(key=sortid)

dev_global_items = []
for x in global_items.values():
    for y in x:
        dev_global_items.append(y)
all_id_class += dev_global_items    #for showing all ID
del dev_global_items

#---------------------------------------material/belch outs/trophies--------------------------------------------

class Mater:    #material
    
    def __init__ (self, name, cost, *effects):
        
        global ID
        
        self.ID = ID
        ID += 1
        
        self.name = name
        self.cost = cost
        
        if effects:
            self.attrib = effects[:-1]     #attributes
            self.attrib_lvl = effects[-1]
        

mat1 =       Mater('mat1',         0, 'def',   'wind',   'death',    1) #test materials
mat2 =       Mater('mat2',         0, 'atk',   'holy',   1)
mat3 =       Mater('mat3',         0, 'hp',    'shadow', 'slippery', 1)
imp_horn =   Mater('Imp horn',     0, 'demon', 'pierce', 1)
imp_heart =  Mater('Imp heart',    0, 'demon', 'fire',   1)
imp_soul =   Mater('Imp soul',     0, 'demon', 'spirit', 2)
met_nugget = Mater('Metal nugget', 0, 'metal', 'nugget', 1) #metal nugget
met_ingot =  Mater('Metal ingot', 0, 'metal', 'ingot',  1)
wood_plank = Mater('Wooden plank', 0, 'wood',  1)

held_mater = [met_nugget, met_ingot]   #held/owned materials

global_mater = [mat1, mat2, mat3, imp_horn, imp_heart, imp_soul, met_nugget, met_ingot, wood_plank]

all_id_class += global_mater     #for dev mode to show all class instances

#--------------------------------------drop tables------------------------------------------------
#first ones define assured drop
#latter ones define probable drop with chances stored in 2 different lists inside a list
#definitive
imp_def_drop_low = [imp_horn, met_nugget]        #low rank imp's drop table for definitive items
imp_def_drop_med = [imp_heart, met_nugget, met_nugget, met_nugget]
imp_def_drop_hig = [imp_soul, met_ingot, met_nugget]

#probable
#name = [[item_1, item_2], [item_1_drop_chance, item_2_drop_chance]]
imp_prb_drop_low = [[met_nugget], [50]]           #low rank imp's drop table for probable items with chances
imp_prb_drop_med = [[met_ingot, met_nugget], [20, 50]]
imp_prb_drop_hig = [[wood_plank, met_ingot, met_nugget, met_nugget], [20, 40, 70, 70]]


#----------------------------------------Characters------------------------------------------------
#(name hp_max atk atk_var recruitment_cost=0 g_drop=0 exp_drop=0,  def_drop=[], prb_drop=[],
#  mana_max=0 mana_gain=0 defence=0 defence_type='none' weapon=basic armor='basic', AI=AI_random,
#    skill=[], skill_tree=[], magic=[], magic_tree=[], passive=[], passive_tree=[],
#    tree_step=[]):

# For refference:
#  sp_atk and special attack refer to either magic, passive, skill class or variables inside Char class
#  tree refers to magic_tree, passive_tree, skill_tree variables inside Char class

# For drop tables see information located somewhere under Mater class(0.4.009).

# Tree has to be double level list: [[1,0],[1,1],[2,1],[3,1]] inner lists define levels of special attack on each level in tree_step.
#  Which special attack corresponds to each level in defined in magic/passive/skill(more on that 1 paragraph below).
#  If tree is not defined, character will not gain any more special attacks(it will always have ones that it began with).
#  Tree levels can't have 0 at the beginning or middle: [[0,0,0],[0,1,0],[0,1,1][1,1,1]] <-- this is unacceptable.
#   Reason: print of sp_atk gain comments

# Special attacks should be either list of basic special attacks, in which case their upgrade versions are set in sp_atk definition,
#  or 2 imensional list, [[magic1, magic2, magic3], [magicA, magicB, magicC]]
#  each inner list defines an order in which special attacks are gained(needs a tree to work).

#---example character for 1D default list---
# hero = Char('Hero', 70, 10, 1, 100,
#             skill=[sp_s_atk_doubl, sp_s_atk_v1],
#             skill_tree=[[1,0],[1,1],[1,2],[2,2],[3,2],[4,3]])

#---example character for 2D custom list---
# mage = Char('Mage', 50, 5, 1, 150, mana_max=100,
#             magic=[[sp_m_heal_all_v1, sp_m_heal_all_v2, sp_m_heal_all_v3], [sp_m_dmg_all_v1, sp_m_dmg_all_v2, sp_m_dmg_all_v3]],
#             magic_tree=[[1,0],[1,1],[2,1],[3,1],[3,2],[3,3]])

# Also keep in mind, that character that uses magic needs to have mana_max set above 0.

# tree_step = [3, 5, 10, 12, 15]  <-- describes, at which levels sp_atk gain occurs
# It should be as long, as the longest tree (i.e. magic_tree) -1 (ommit first stage).
#  If it is too short, not all skills written in tree will be given to character.
#  If too long, no exception, no new skill happen (but i'm guessing it still goes over sp_atk_lvl_up, so slows whole process a little).
#  And also try to not repeat numbers in it or put them in disorder. Haven't checked but it could mess things up.

                  
hero =     Char('Hero',     70,  10, 1, 100, defence=1, skill=[sp_s_atk_doubl, sp_s_atk_v1], skill_tree=[[1,0],[1,1],[1,2],[2,2],[3,2],[4,3]])
champion = Char('Champion', 90,  9,  2, 100, skill=[sp_s_atk_tripl])
mage =     Char('Mage',     50,  5,  1, 150, mana_max=100,
                magic=[[sp_m_heal_all_v1, sp_m_heal_all_v2, sp_m_heal_all_v3], [sp_m_dmg_all_v1, sp_m_dmg_all_v2, sp_m_dmg_all_v3]],
                magic_tree=[[1,0],[1,1],[2,1],[3,1],[3,2],[3,3]])
assasin =  Char('Assasin',  55,  11, 4, 100)
fighter =  Char('Fighter',  80,  11, 1, 200, defence=1)
defender = Char('Defender', 100, 4,  3, 170, defence=3)

test_boi_1 = Char('_test_boi_ 1', 1, 1, 0)

test_boi_2 = Char('_test_boi_ 2', 1, 1, 0)

test_boi_3 = Char('_test_boi_ 3', 100, 1, 0, mana_max = 200,
                skill=[sp_s_atk_doubl],
                skill_tree=[[0],[1],[2],[3]],
                magic=[sp_m_dmg_all_v1, sp_m_heal_all_v1],
                magic_tree=[[1,0],[1,1],[1,2],[2,2],[3,3]],
                passive=[sp_p_heal_all_v1],
                passive_tree=[[0],[1],[2],[3]],
                tree_step=[1, 3, 5, 10, 13])
test_boi_4 = Char('_test_boi_ 4', 100, 1, 0, mana_max = 200,
                skill=[[sp_s_atk_doubl, sp_s_atk_tripl, sp_s_atk_quad], [sp_s_atk_v2, sp_s_atk_v3, sp_s_atk_v4]],
                skill_tree=[[1,0],[1,1],[1,2],[2,2],[3,2],[3,3]],
                magic=[[sp_m_heal_all_v1, sp_m_heal_all_v2, sp_m_heal_all_v3], [sp_m_dmg_all_v1, sp_m_dmg_all_v2, sp_m_dmg_all_v3]],
                magic_tree=[[1,0],[1,1],[2,1],[3,1],[3,2],[3,3]],
                passive=[[sp_p_dmg_all_v1, sp_p_dmg_all_v2, sp_p_dmg_all_v4]],
                passive_tree=[[0],[1],[2],[3]],
                tree_step=[1, 2, 3, 4, 5, 6])

if dev_opt == 'xel':
    global_allies = [hero, champion, mage, assasin, fighter, defender, test_boi_1, test_boi_2, test_boi_3, test_boi_4]
else:
    global_allies = [hero, champion, mage, assasin, fighter, defender]

global_allies_baseline = []                         #used in loading from file
for x in global_allies:
    global_allies_baseline.append(deepcopy(x))

# monster = Char('Monster', 120, 8, 0, 50, armor=light)   #old char used in first battles /unused
# demon = Char('Demon', 40, 12, 4, 50, armor=light)  #second old char /unused

#(name hp_max atk atk_var recruitment_cost=0 g_drop=0 exp_drop=0,  def_drop=[], prb_drop=[],
#    mana_max=0 mana_gain=0 defence=0 defence_type='none' weapon=basic armor='basic', AI=AI_random,
#    skill=[], skill_tree=[], magic=[], magic_tree=[], passive=[], passive_tree=[]
#    tree_step=[])   #details described above

#--------------------imps---------------------
imp_1 = Char('Lesser Imp',  40,  4,  2, 0, 30,  10,  imp_def_drop_low, imp_prb_drop_low,  0, 0, 0, 'Low Demon', imp_bas_wep, imp_bas_arm)
imp_2 = Char('Imp Servant', 40,  4,  2, 0, 45,  20,  imp_def_drop_low, imp_prb_drop_low,  0, 0, 0, 'Low Demon', imp_lig_wep, imp_lig_arm, AI=AI_servant)
imp_3 = Char('Imp',         60,  7,  1, 0, 75,  35,  imp_def_drop_med, imp_prb_drop_med,  0, 0, 0, 'Low Demon', imp_lig_wep, imp_lig_arm, AI=AI_weakfirst)
imp_4 = Char('Imp Soldier', 60,  7,  1, 0, 120, 45,  imp_def_drop_med, imp_prb_drop_med,  0, 0, 0, 'Low Demon', imp_med_wep, imp_med_arm, AI=AI_servant)
imp_5 = Char('Greater Imp', 120, 10, 0, 0, 150, 65,  imp_def_drop_hig, imp_prb_drop_hig,  0, 0, 0, 'Demon',    imp_lig_wep, imp_med_arm, AI=AI_onetarg)
imp_6 = Char('Imp General', 120, 10, 0, 0, 225, 80,  imp_def_drop_hig, imp_prb_drop_hig,  0, 0, 0, 'Demon',    imp_med_wep, imp_goo_arm, AI=AI_command)
imp_7 = Char('Imp Outcast', 120, 10, 0, 0, 277, 100, imp_def_drop_hig, imp_prb_drop_hig,  0, 0, 0, 'Demon',    imp_goo_wep, imp_vgo_arm, AI=AI_strongfirst)

#---------------------demons-------------------
demon_1 = Char('Demon Slave',    100, 7,  2, 0, 70,  75,  None, None, 0, 0, 0, 'Demon',         dem_bas_wep, dem_bas_arm, AI=AI_servant)
demon_2 = Char('Lower Demon',    100, 7,  2, 0, 80,  86,  None, None, 0, 0, 0, 'Demon',         dem_lig_wep, dem_lig_arm, AI=AI_weakfirst)
demon_3 = Char('Demon',          150, 11, 1, 0, 120, 105, None, None, 0, 0, 1, 'Demon',         dem_lig_wep, dem_lig_arm)
demon_4 = Char('Demon Fighter',  150, 11, 1, 0, 155, 127, None, None, 0, 0, 1, 'Demon',         dem_med_wep, dem_med_arm, AI=AI_onetarg)
demon_5 = Char('Higher Demon',   270, 16, 2, 0, 220, 180, None, None, 0, 0, 1, 'High Demon',    dem_lig_wep, dem_med_arm, AI=AI_strongfirst)
demon_6 = Char('Demon Guardian', 270, 16, 2, 0, 250, 203, None, None, 0, 0, 1, 'High Demon',    dem_med_wep, dem_goo_arm, AI=AI_servant)
demon_7 = Char('Demon Warlord',  270, 16, 2, 0, 400, 300, None, None, 0, 0, 1, 'High Demon',    dem_goo_wep, dem_vgo_arm, AI=AI_command)
demon_8 = Char('Demon Chosen',   350, 17, 3, 0, 600, 400, None, None, 0, 0, 2, 'High Demon',    dem_goo_wep, dem_vgo_arm, AI=AI_onetarg)

global_enemies = [imp_1,imp_2,imp_3,imp_4,imp_5,imp_6,imp_7,demon_1,demon_2,demon_3,demon_4,demon_5,demon_6,demon_7]
global_char = global_enemies + global_allies

all_id_class += global_char     #for showing all ID
#--------------------------------------------------Character-copies------------------------------------------------------------
imp_1b = deepcopy(imp_1)      #copying class instance
imp_2b = deepcopy(imp_2)
imp_3b = deepcopy(imp_3)
imp_4b = deepcopy(imp_4)
imp_4c = deepcopy(imp_4)
imp_5b = deepcopy(imp_5)
imp_5c = deepcopy(imp_5)
imp_6b = deepcopy(imp_6)
demon_1b = deepcopy(demon_1)
demon_1c = deepcopy(demon_1)
demon_2b = deepcopy(demon_2)
demon_3b = deepcopy(demon_3)
demon_4b = deepcopy(demon_4)
demon_5b = deepcopy(demon_5)
demon_6b = deepcopy(demon_6)
demon_6c = deepcopy(demon_6)
demon_6d = deepcopy(demon_6)

#-------------------------------------------------fighting-groups-----------------------------------------------------------
# allies = global_enemies
if dev_opt == 'xel':
    allies = [test_boi_1, test_boi_2, test_boi_3, test_boi_4]
else:
    allies = [hero, mage]


enem_0 = [imp_2]
enem_1 = [imp_2, imp_1, imp_1b]      #remember to define more of the same char type as different entities(deepcopy)
enem_2 = [imp_3, imp_2, imp_1]
enem_3 = [imp_3, imp_3b]
enem_4 = [imp_4, imp_2, imp_2b]
enem_5 = [imp_4, imp_4b, imp_4c]
enem_6 = [imp_5, imp_3, imp_3b]
enem_7 = [imp_6, imp_4, imp_4b]
enem_8 = [imp_5, imp_5b, imp_5c]
enem_9 = [imp_6, imp_6b, imp_5]
enem_10 = [imp_7]
enem_11 = [imp_5, demon_1, demon_1b, demon_1c]
enem_12 = [demon_2, demon_2b, imp_7]
enem_13 = [demon_3, demon_3b]
enem_14 = [demon_5, demon_3, demon_3b]
enem_15 = [demon_4, demon_4b, imp_6, imp_6b]
enem_16 = [demon_5, demon_5b, demon_3, demon_4]
enem_17 = [demon_6, demon_6b]
enem_18 = [demon_6, demon_6b, demon_6c, demon_6d]
enem_19 = [demon_7, demon_6, demon_6b, demon_6c, demon_6d]
enem_20 = global_enemies

all_enem_fight = [enem_0, enem_1, enem_2, enem_3, enem_4, enem_5, enem_6, enem_7, enem_8, enem_9, enem_10,
                  enem_11, enem_12, enem_13, enem_14, enem_15, enem_16, enem_17, enem_18, enem_19, enem_20]


team_1 = allies     #needs to be defined for info display(check items/characters, option 4 in main while)
#leave this as it is, it may expolde if touched

for x in allies:    #loop for removing allies already it team from 'recruit' roster
    if x in global_allies:
        global_allies.remove(x)


#--------------------------------comission class------------------------------------------
class Cmsn:
    
    def __init__(self, name, rank, _type,
                 cmpl_kill=[], cmpl_kill_cnt=[], cmpl_item=[], cmpl_item_cnt=[],
                 rew_gold=0, rew_items=[],
                 req_cmsn_stry=[], req_cmsn_cnt=0, req_lvl_max=0, req_lvl_sum=0, req_team_cnt=0):
        
        global ID
        self.ID = ID
        ID += 1
        
        self.name = name
        self.rank = rank
        self.type = _type
        
        # completion kill
        self.cmpl_kill = cmpl_kill            #defines which enemies have to be killed
        # completion kill count
        self.cmpl_kill_cnt = cmpl_kill_cnt    #defines how many enemies at the same index in list above have to be killed
        # completion items
        self.cmpl_item = cmpl_item            #defines which items have to be delivered
        # completion items count
        self.cmpl_item_cnt = cmpl_item_cnt    #similar to cmpl_kill_cnt, defines number of items to be delivered
        
        self.prog_kill = cmpl_kill
        self.prog_kill_cnt = cmpl_kill_cnt
        self.prog_item = cmpl_item
        self.prog_item_cnt = cmpl_item_cnt
        
        # reward gold
        self.rew_gold = rew_gold
        # reward items
        self.rew_items = rew_items
        
        # required comission story
        self.req_cmsn_stry = req_cmsn_stry        #defines which previous story comissions have to be completed(by id or name(?))
        # required comission count
        self.req_cmsn_cnt = req_cmsn_cnt          #defines how many comissions of same rank have to be completed before taking this one
        # required level max
        self.req_lvl_max = req_lvl_max          #required one character of at least this level
        # required level summ
        self.req_lvl_sum = req_lvl_sum         #required summed up levels of all characters in team
        # required team count
        self.req_team_cnt = req_team_cnt      #required number of characters in a team
    
    def renew(self):
        #renewing progress counting variables
        
        self.prog_kill = self.cmpl_kill
        self.prog_kill_cnt = self.cmpl_kill_cnt
        self.prog_item = self.cmpl_item
        self.prog_item_cnt = self.cmpl_item_cnt
    
    def print_all(self):
        print(f'ID {self.ID}')
        print(f'name {self.name}')
        print(f'rank {self.rank}')
        print(f'type {self.type}')
        
        print(f'cmpl_kill {[x.ID for x in self.cmpl_kill]}')
        print(f'cmpl_kill_cnt {self.cmpl_kill_cnt}')
        print(f'cmpl_item {[x.ID for x in self.cmpl_item]}')
        print(f'cmpl_item_cnt {self.cmpl_item_cnt}')
        
        print(f'prog_kill {[x.ID for x in self.prog_kill]}')
        print(f'prog_kill_cnt {self.prog_kill_cnt}')
        print(f'prog_item {[x.ID for x in self.prog_item]}')
        print(f'prog_item_cnt {self.prog_item_cnt}')
        
        print(f'rew_gold {self.rew_gold}')
        print(f'rew_items {[x.ID for x in self.rew_items]}')
        
        print(f'req_cmsn_stry {self.req_cmsn_stry}')
        print(f'req_cmsn_cnt {self.req_cmsn_cnt}')
        print(f'req_lvl_max {self.req_lvl_max}')
        print(f'req_lvl_sum {self.req_lvl_sum}')
        print(f'req_team_cnt {self.req_team_cnt}')
    
        
#ranks of comissions
# Each comission should have its own rank. Then, from this rank, global team rank will be substracted.
#  New rank will be then converted to text:
#   < 1 'too easy'
#   1 'simple'
#   2 'easy'
#   3 'mediocre'
#   4 'difficult'
#   5 'hard'
#   6 'challenging'
#   > 6 'too hard'
#  If comission has rank lower than 1 or higher that 6, it will not be shown(applies to story quests).

# When random comission generator will be created, appropriate range of comission properties will be selected(rank/requirements) in it.

# add class of comission?
#  -assasination (defeat a single, strong opponent)
#  -hunt (defeat many(or not so many) opponents)
#  -protection (endure constant(until it is not) onslaught of monsters, i.e. if you kill one another comes, or they come sooner)
#  -search ()  <-- with modified/expanded/overhauled encounter/exploration/world structure this will have more sense
#  -gathering (gather some amount of items dropped by enemies(trophies or other))
#  -raid (hunt and gathering joined together)

#random comission generator
# make a list of possible comission requirements and their rank
#   divide them by rank, type
#   assign their names(at random(?))
#   requirements depending on rank an type
#   assign rewards(depending on rank/type/requirements);
#  if player will defeat certain story comission, global team rank will go up
#   (lowering rank of quests: challenging -> hard, hard -> difficult and so on).

# rewards as items/materials/armor/weapons
#  now define them manually
#  later add a randomiser(for cmsn_slots) and special instances of Item that will give random items from main comissions

# quest chain:
#  sometimes battles are interrupted by another, stronger enemy(or in each battle enemies will be stronger or more numerous
#  it is unknown why it appears, but investigation(comisson) chain will begin
#  after several gathering/hunt/raid comissions, the cause of this event will be unveiled
#  new assasination mission will appear with very strong enemy
#  after it is slain, event will end and good rewards will be bestowed upon the player

# allow comissions to unlock special fights

# compress comission selection in comission counter
#  instead of:
#   comission1: details, more details, even more details
#   comission2: details, more details, even more details
#  do:
#   comission1: name, type
#   comission2: name, type
#  and when you choose comission you get more details


#(self, name, rank,
# cmpl_kill=[], cmpl_kill_count=[], cmpl_item=[], cmpl_item_cnt=[],
# rew_gold=0, rew_items=[],
# req_cmsn_stry=[], req_cmsn_cnt=0, req_lvl_max=0, req_lvl_sum=0, req_team_cnt=0):

#here will be defined main story(?) comissions
cmsn_story_1 = Cmsn('First task',  1, 'hunt', [imp_2, imp_3], [2, 1], [], [], 100, [potion, potionv2])
cmsn_story_2 = Cmsn('Second task', 6, 'assasination', [imp_7, imp_6], [1, 1], [], [], 200, [imp_soul])
cmsn_story_3 = Cmsn('Third task',  2, 'gathering', [], [], [met_nugget, met_ingot], [3, 1], 80, [met_ingot, met_ingot])
cmsn_story_4 = Cmsn('Fourth task', 3, 'search')
cmsn_story_5 = Cmsn('Fifth task',  4, 'raid', [imp_3, imp_4], [5, 3], [met_ingot], [2], 250, [bardiche])
cmsn_story_6 = Cmsn('Sixth tash',  5, 'protection')

cmsn_empty = Cmsn('Empty', 0, 'empty')

#slots will be for random generated comissions
cmsn_slot_1 = Cmsn('slot', 0, 'slot')
cmsn_slot_2 = Cmsn('slot', 0, 'slot')
cmsn_slot_3 = Cmsn('slot', 0, 'slot')
cmsn_slot_4 = Cmsn('slot', 0, 'slot')

cmsn_story = [cmsn_story_1, cmsn_story_2, cmsn_story_3, cmsn_story_4, cmsn_story_5, cmsn_story_6]
cmsn_slots = [cmsn_slot_1, cmsn_slot_2, cmsn_slot_3, cmsn_slot_4]

global_cmsn = cmsn_story + cmsn_slots

accept_cmsn = cmsn_story_1   #accepted comission (decided not to use list; only one can be accepted at one time)

all_id_class += global_cmsn    #for dev mode to show all class instances

def cmsn_info(x, opt=0):
    #x is inputted comission, opt is for showing either progress left to fulfill or default progress
    if opt == 0:
        kill, kill_cnt, item, item_cnt = x.prog_kill , x.prog_kill_cnt , x.prog_item , x.prog_item_cnt
    else:
        kill, kill_cnt, item, item_cnt = x.cmpl_kill , x.cmpl_kill_cnt , x.cmpl_item , x.cmpl_item_cnt
        
    
    ret = [f'Name: {x.name}',
                 f'Rank: {"If you see this remind me of this line"}',
                 f'Type: {x.type}']
    
    out = 'Completion requirement: '
    
    if x.type in ['hunt', 'assasination', 'gathering', 'raid']:
        for lis in [[kill, kill_cnt], [item, item_cnt]]:    #going over all of completion requirements
            lis, lis_cnt = lis                            #unpacking (instances and count) list
            
            if len(lis) == 0:                 #prevents double space to occur, if in raid cmsn kill requirements have been fulfilled
                continue
            
            if lis:
                out += 'assasinate' if x.type == 'assasination' else ('hunt' if lis == kill else 'deliver')  #outputting header(?) for requirements
                
            for k, z in enumerate(zip(lis, lis_cnt)):                           #going over instances and count list with enumerator
                z, l = z
                
                out += f' {l}x {z.name}' if x.type != 'assasination' else f' {z.name}'  #outputting how many of z is needed or outputting just z if it's assasination
                if k+1 < len(lis):        #if enumerator isn't last, add comma
                    out += ','
            out += ' '
    else:
        pass
        
    ret.append(out)
    
    ret.append('Rewards: ' if (x.rew_gold or x.rew_items) else 'Rewards: None')  #add this to table if reward is present, else add that
    ret.append(f' gold:{x.rew_gold} ' if x.rew_gold else '')
    
    if x.rew_items:
        out = ''
        for l, z in enumerate(x.rew_items):
            if l == 0:
                out += f' {"items" if len(x.rew_items) > 1 else "item"}: '
            out += f'{z.name} '
            if l+1 < len(x.rew_items):
                out += ', '
        ret.append(out)
    
    return ret



#---------------for showing all ID-----------------
if dev_opt == 'xel':
    print(all_id_class)
    all_id_class = list(dict.fromkeys(all_id_class))  #removing duplicates by converting to dict and back to list
    all_id_class.sort(key=sortid)
    for x in all_id_class:
        print(f'{stat_len(x.name, 25)} ID:{x.ID}')    #print all classes and their ID
    pause()

#---------------------The Main Loop-------------------------
while True:
    allies = team_1     #making sure these 2 values are the same
    temp_menu = [
        'What do you want to do?',
        ' 1. Fight a monster',
        ' 2. Go to shop',
        ' 3. Go to tavern',
        ' 4. Check items/characters',
        ' 5. Menu',
        ' 6. Exit the Game'
        ]
    if dev_opt == 'xel':
        temp_menu.append(' 7. dev_options')
    menu_print(temp_menu)

    a = input("Choose: ")

    a, z = in_err_ch(a, len(temp_menu)-1, 1)

    if z == 1:
        continue
    elif z == 2:
        break
    elif z == 3:
        m += 1
        continue
    elif z == 4:
        m -= 1
        continue
    
    if a == 1:
        while True:
            temp_menu = [
            'Available fights:'
            ]
            y = -1
            for x in all_enem_fight:
                y += 1
                v = stat_len(y, 2, 1) + '. enemies: '
                for z in x:
                    v += z.stat_name + ' ,'
                temp_menu.append(v)
            menu_print(temp_menu)
                
            o = input('Choose one that you wish to participate in(type "ex" to quit): ')
            
            o, z = in_err_ch(o, len(temp_menu)-1)

            if z == 1:
                continue
            elif z == 2:
                break
            elif z == 3:
                m += 1
                continue
            elif z == 4:
                m -= 1
                continue


            fight(team_1, all_enem_fight[o])
            break
                     
    elif a == 2:
        shop(global_items, global_weapons, global_armor, 10)
        
    elif a == 3:
        while True:
            temp_menu = [
                'Welcome to the tavern',
                'What do you seek here?',
                ' 1. Recruit aventurers to your team',
                ' 2. Go to the comission counter',     #comission/quest/order
                ' 3. Exit tavern'
            ]
            
            menu_print(temp_menu)
            
            a = input('Choose: ')
            
            a, z = in_err_ch(a, len(temp_menu)-2, 1)

            if z == 1:
                continue
            elif z == 3:
                m += 1
                continue
            elif z == 4:
                m -= 1
                continue
            
            if a == 1:
                while True:
                    temp_menu = []
                    
                    if global_allies:
                        if len(global_allies) > 1:
                            temp_menu.append(f'Currently awaiting or recruitment {"are" if len(global_allies) > 1 else "is"}:')
                            for y, char in enumerate(global_allies):
                                temp_menu.append(f' {y}. {char.stat_name}- health:{char.stat_hp}/{char.stat_hp_max} attack:{char.atkmin}-{char.atkmax} defence:{char.stat_defence} recruit cost: {char.recr_cost}')
                                
                        menu_print(temp_menu)
                        o = input('Choose one to recruit(type "ex" to exit) ')

                        o, z = in_err_ch(o, len(temp_menu)-2)

                        if z == 1:
                            continue
                        elif z == 2:
                            break
                        elif z == 3:
                            m += 1
                            continue
                        elif z == 4:
                            m -= 1
                            continue
                        
                        global_allies[o].recruit()
                    else:
                        menu_print(['There is no one to recruit at this tavern'])
                        pause()
                        break
                
            elif a == 2:
                #----------------comission counter---------------------------
                while True:
                    temp_menu = ['Clerk: "Welcome to the comission counter.',
                                 '        How can I help you?"',
                                 ' 1. Available comissions',
                                 ' 2. Complete(remind of) a comission',
                                 ' 3. Put up a new comission',
                                 ' 4. Exit']
                    
                    menu_print(temp_menu)
                    
                    a = input('Choose: ')
                    a, z = in_err_ch(a, len(temp_menu)-2, 1)
                    
                    if z in [1, 2]:
                        continue
                    elif z == 3:
                        m += 1
                    elif z == 4:
                        m -= 1
                    
                    if a == 1:
                        while True:
                            temp_menu = ['Current urgent comissions:']
                            temp_cmsn = []
                            
                            for y, x in enumerate(cmsn_story):
                                temp_menu.append(f' {y} {x.name}: {x.type}')    #gathering general information about comission
                                temp_cmsn.append(x)                             #and gathering -a-l-l- chosen comission instances
                            
                            sec_menu = ['1. Display more details for comission',
                                        '2. Accept comission',
                                        '3. Exit']
                            
                            menu_print(temp_menu, 0, 0, sec_menu)
                            
                            a = input('Choose: ')
                            a, z = in_err_ch(a, 3, 1)
                            
                            if z in [1, 2]:
                                continue
                            elif z == 3:
                                m += 1
                            elif z == 4:
                                m -= 1
                            
                            if a == 1:
                                
                                menu_print(temp_menu)
                                
                                o = input('Which one? ')
                                o, z = in_err_ch(o, len(temp_cmsn)-1, 0)
                                
                                if z in [1, 2]:
                                    continue
                                elif z == 3:
                                    m += 1
                                elif z == 4:
                                    m -= 1
                                
                                temp_menu = cmsn_info(temp_cmsn[o])
                                
                                menu_print(temp_menu)
                                pause()
                                
                            elif a == 2:
                                while True:
                                    menu_print(temp_menu)
                                    o = input('Which one do you want to accept?(type "ex" to exit) ')
                                    o, z = in_err_ch(o, len(temp_cmsn))
                                    
                                    if z == 1:
                                        continue
                                    elif z == 2:
                                        break
                                    elif z == 3:
                                        m += 1
                                    elif z == 4:
                                        m -= 1
                                    
                                    
                                    if accept_cmsn:
                                        menu_print([f'You already have a comission accepted: {accept_cmsn.name}',
                                                    'Are you sure, you want to forget about it and accept a new one?',
                                                    '/ / Warning, it may have consequences / /'], 2, 2)
                                        
                                        z = input('Type "yes" to accept a new comission and forget other one. ')
                                        if z != 'yes':
                                            break
                                    
                                    cmsn_kill_counter = deepcopy(kill_counter)
                                    accept_cmsn.renew()
                                    accept_cmsn = temp_cmsn[o]
                                    
                                    menu_print([f'{accept_cmsn.name} has been accepted.'], 2, 2)
                                    pause()
                                    break
                                
                            elif a == 3:
                                del temp_cmsn
                                break
                    
                    #---------complete (remind of) a comission------------
                    elif a == 2:
                        z = 0
                        while True:
                            if accept_cmsn == cmsn_empty:
                                if z != 1:                          #flag from completed comission
                                    menu_print(["No comission is currently accepted."], 2, 2)
                                    z = 0
                                    pause()
                                break
                            
                            
                            temp_menu = ['Current comission:']
                            temp_menu += cmsn_info(accept_cmsn)
                            
                            sec_menu = ['1. Update progress and/or deliver items',
                                        '2. Forget about this comission',
                                        '3. Exit']
                            
                            menu_print(temp_menu, 0, 0, sec_menu)
                            
                            a = input('Choose: ')
                            
                            a, z = in_err_ch(a, len(sec_menu), 1)
                            
                            if z in [1, 2]:
                                continue
                            elif z == 3:
                                m += 1
                            elif z == 4:
                                m -= 1
                            
                            #----completion check
                            if a == 1:
                                
                                temp_menu = ['Current comission:'] + cmsn_info(accept_cmsn)
                                sec_menu = []
                                prog_flag = 0
                                
                                if accept_cmsn.type in ['hunt', 'assasination', 'raid']:
                                    
                                    back_kill_counter = deepcopy(kill_counter)     #making backup of kill_counter
                                    z = 1
                                    #---------------------------
                                    kill_counter = list_sub_2d_id(kill_counter, cmsn_kill_counter)  #substracting 2 2d lists
                                    #---------------------------
                                    if kill_counter[1]:
                                        out = 'After last progress report you have slain '
                                        for char in global_char:
                                            if char.ID in kill_counter[0] and char.ID in [x.ID for x in accept_cmsn.prog_kill]:
                                                ind = kill_counter[0].index(char.ID)
                                                count = kill_counter[1][ind]
                                                out += f'{count}x{char.name} '
                                                del ind, count
                                        else:
                                            out = out[:-1]
                                        sec_menu.append(out)
                                        prog_flag = 1
                                    else:
                                        out = ''            #defining out here too, so that i can safely delete it or one above
                                    
                                    #---------------------------
                                    
                                    accept_cmsn.prog_kill = char2num(accept_cmsn.prog_kill)       #convert characters to ID
                                    cmsn_prog_kill = [accept_cmsn.prog_kill, accept_cmsn.prog_kill_cnt]    #pack 2 values into 1(for nice looks)
                                    
                                    accept_cmsn.prog_kill, accept_cmsn.prog_kill_cnt = list_sub_2d_id(cmsn_prog_kill, kill_counter)  #substract lists
                                    accept_cmsn.prog_kill = num2char(accept_cmsn.prog_kill)          #convert ID to characters
                                    
                                    kill_counter = back_kill_counter    #recovering kill_counter from backup
                                    cmsn_kill_counter = deepcopy(kill_counter)
                                    #-----------------------------
                                    
                                    del back_kill_counter, z, out, cmsn_prog_kill
                                
                                if accept_cmsn.type in ['gathering', 'raid']:
                                    
                                         #convert held_mater to 2d kill_counter-like list
                                    mater_counter = [[], []]
                                    for x in held_mater:
                                        if not x.ID in mater_counter[0]:
                                            mater_counter[0].append(x.ID)
                                            mater_counter[1].append(0)
                                        
                                        ind = mater_counter[0].index(x.ID)
                                        mater_counter[1][ind] += 1
                                        del ind
                                    #------------------------
                                    deliv_items = [[], []]
                                    for y, x in enumerate(accept_cmsn.prog_item):
                                        if x.ID in mater_counter[0]:                #if wanted material is held/owned
                                            cmsn_cnt = accept_cmsn.prog_item_cnt[y]         #get count of needed materials
                                            ind = mater_counter[0].index(x.ID)          #get index of held material
                                            cnt = mater_counter[1][ind]                 #get its count
                                            del_items = cnt if cnt < cmsn_cnt else cmsn_cnt  #calculate how many materials can be delivered
                                            
                                            deliv_items[0].append(x)                   #append ID and count of items that can be delivered
                                            deliv_items[1].append(del_items)
                                            del cmsn_cnt, ind, cnt, del_items
                                    #------------------------
                                    if deliv_items[0]:
                                        
                                        out = 'You can deliver: '
                                        for x, y in zip(deliv_items[0], deliv_items[1]):    #writing comment, which items can be delivered
                                            out += f'{y}x{x.name} '
                                        sec_menu.append(out)
                                        
                                        menu_print(temp_menu, 0, 0, sec_menu)
                                        o = input('Deliver these items(type "yes" to confirm) ') 
                                        
                                        if o == 'yes':
                                                       #substracting delivered items from material counter
                                            mater_counter = list_sub_2d_id(mater_counter, [char2num(deliv_items[0]), deliv_items[1]])
                                            
                                            prog_item = accept_cmsn.prog_item, accept_cmsn.prog_item_cnt   #packing 2 lists
                                            prog_item = list_sub_2d_id(prog_item, deliv_items)           #removing delivered items from progress
                                            accept_cmsn.prog_item, accept_cmsn.prog_item_cnt = prog_item   #unpacking 2 lists
                                            
                                            mater_counter[0] = num2char(mater_counter[0])
                                            held_mater = []
                                            for x, y in zip(mater_counter[0], mater_counter[1]):     #converting mater_counter back to held_mater
                                                for _ in range(y):
                                                    held_mater.append(x)
                                                
                                            prog_flag = 1
                                            
                                            del out
                                    else:
                                        pass
                                    
                                    del deliv_items, mater_counter
                                    
                                elif accept_cmsn.type == 'raid':
                                    pass
                                
                                elif accept_cmsn.type == 'protection':
                                    pass
                                
                                elif accept_cmsn.type == 'search':
                                    pass
                                
                                else:
                                    pass
                                
                                if prog_flag == 1:
                                    sec_menu = ['Progress of comission will be updated.']
                                else:
                                    sec_menu = ['No progress has been made since last report.']
                                
                                menu_print(temp_menu, 0, 0, sec_menu)
                                pause()
                                
                                #---reward assignment
                                if not accept_cmsn.prog_kill + accept_cmsn.prog_item:
                                    temp_menu = [f'Comission {accept_cmsn.name} has been completed',
                                                 'You have gained:',
                                                 f' {accept_cmsn.rew_gold} gold']
                                    
                                    for rew in accept_cmsn.rew_items:
                                        if type(rew) == Item:
                                            held_items.append(rew)
                                        elif type(rew) == Mater:
                                            held_mater.append(rew)
                                        elif type(rew) == Char:
                                            team_1.append(rew)
                                        elif type(rew) == Armor:
                                            held_armor.append(rew)
                                        elif type(rew) == Weapon:
                                            held_weapons.append(rew)
                                        elif type(rew) == SP_magic:
                                            pass
                                        elif type(rew) == SP_skill:
                                            pass
                                        elif type(rew) == SP_passive:
                                            pass
                                        temp_menu[2] += f', {rew.name}'
                                    
                                    for x in [held_items, held_mater, held_weapons, held_armor]:
                                        x.sort(key=sortid)
                                    
                                    accept_cmsn.renew()
                                    accept_cmsn = cmsn_empty
                                    menu_print(temp_menu, 2, 2)
                                    z = 1                      #flag for not displaying "You do not have comission with you, go away."
                                    pause()
                                
                                
                            #-------------------
                            elif a == 2:
                                menu_print(['Are you sure, you want to forget about current comission?',
                                            '/ / Warning, it may have consequences / /'], 2, 2)
                                
                                o = input('Type "yes" to forget current comission. ')
                                
                                if o == 'yes':
                                    menu_print([f'{accept_cmsn.name} has been forgotten.'])
                                    pause()
                                    
                                    accept_cmsn.renew()     #renewing comission status
                                    accept_cmsn = cmsn_empty   #placeholder comission
                                    break
                            #------------------
                            elif a == 3:
                                break
                            
                    #---------put up a new comission---------
                    elif a == 3:
                        menu_print(['Unavailable for now'], 2, 2)
                        pause()
                        
                    elif a == 4:
                        break
                    
            elif a == 3:
                break
                
    elif a == 4:
        while True:
            temp_menu = [
            'What do you want to do?',
            ' 1. Display information',
            ' 2. Equip weapons',
            ' 3. Unequip weapons',
            ' 4. Equip armor',
            ' 5. Unequip armor',
            ' 6. Exit'
            ]
            
            menu_print(temp_menu)
            
            a = input('Choose: ')

            a, z = in_err_ch(a, len(temp_menu)-1, 1)

            if z == 1:
                continue
            elif z == 3:
                m += 1
                continue
            elif z == 4:
                m -= 1
                continue
            
            if a == 1:
                while True:
                    temp_menu = [
                    'Display information about',
                    ' 1. statistics about team',
                    ' 2. level and experience of team',
                    ' 3. items',
                    ' 4. equipment',
                    ' 5. special attacks',
                    ' 6. materials',
                    ' 7. kill counter',
                    ' 8. exit'
                    ]
                    
                    menu_print(temp_menu)
                    
                    a = input('Choose: ')
              
                    a, z = in_err_ch(a, len(temp_menu)-1, 1)

                    if z == 1:
                        continue
                    elif z == 3:
                        m += 1
                        continue
                    elif z == 4:
                        m -= 1
                        continue

                    if a == 1:
                        #----------------------------team detailed display------------------------
                        while True:
                            temp_menu = ['Your current team consists of:', '']
                            temp_menu += stat_print(3)                     #printing extended stats
                            
                            menu_print(temp_menu, d=2)
                            
                            o = input('Type anything besides next and back to exit ')
                            
                            o, z = in_err_ch(o, len(temp_menu)-1, 0, 1)
                            
                            if z == 1 or z == 2 or z == 0:
                                break
                            elif z == 3:
                                m += 1
                                continue
                            elif z == 4:
                                m -= 1
                                continue
                        
                    elif a == 2:
                        #-----------------------team experience display------------------------
                        while True:
                            temp_menu, leng = ['Your team:'], 0
                            #----------flexible name setter----------
                            for x in team_1:
                                if len(x.name) > leng:
                                    leng = len(x.name)
                            
                            #------------comment section-----------
                            for char in team_1:
                                temp_menu.append(f'{stat_len(char.name, leng+1)}: level: {stat_len(char.level, 2, 1)} experience points: {stat_len(char.exp, 6,1)} required exp points: {stat_len(200*char.level, 6, 1)}')
                            
                            menu_print(temp_menu, d=2)
                                
                            o = input('Type anything besides next and back to exit ')
                            
                            o, z = in_err_ch(o, len(temp_menu)-1, 0, 1)
                            
                            if z == 1 or z == 2 or z == 0:
                                break
                            elif z == 3:
                                m += 1
                                continue
                            elif z == 4:
                                m -= 1
                                continue
                        
                    elif a == 3:
                        #---------------------------held items display-------------------------------
                        while True:
                            #--------------flexible name setter-----------------
                            max_len = 0
                            for x in [x.name for x in held_items]:
                                if len(x) > max_len:
                                    max_len = len(x)
                            
                            #------------comment section-----------------
                            if held_items:                             #printing extended items
                                temp_menu = ['Currently held items: ']
                                for x in held_items:
                                    temp_menu.append(f' {stat_len(x.name, max_len)}: function:{x.fnc_name} for:{stat_len(x.x, 3, 1)}')
                            elif not held_items:
                                temp_menu = ["You don't hold any items in your inventory"]

                            menu_print(temp_menu, d=2)
                                
                            o = input('Type anything besides next and back to exit ')
                            
                            o, z = in_err_ch(o, len(temp_menu)-1, 0, 1)
                            
                            if z == 1 or z == 2 or z == 0:
                                break
                            elif z == 3:
                                m += 1
                                continue
                            elif z == 4:
                                m -= 1
                                continue
                            
                    elif a == 4:
                        #-----------------------------held weapons display---------------------------------
                        while True:
                            if held_weapons:
                                temp_menu = ['Currently held weapons:']
                                for x in held_weapons:              #printing weapon stats
                                    y = f' {x.stat_name}: damage:{x.stat_dmg}({x.dmg_var}) {stat_len(x.dmg_type_1, 5, 1)} {stat_len(x.dmg_type_2, 5, 1)}'
                                    if x.ohe:
                                        y += f' {x.ohe_name} for {x.ohe_value}(% for lifesteal)'
                                    temp_menu.append(y)
                            elif not held_weapons:
                                temp_menu = ['No weapons are being held in inventory']
                                
                            temp_menu.append('')
                            
                            if held_armor:
                                temp_menu.append('Currently held armor:')
                                for x in held_armor:
                                    temp_menu.append(f' {x.stat_name}: defence:{x.stat_defence} defence type:{stat_len(x.defence_type, 6, 1)}')
                            elif not held_armor:
                                temp_menu.append('No armor is being held in inventory')
                            
                            menu_print(temp_menu, d=2)
                                
                            o = input('Type anything besides next and back to exit ')
                            
                            o, z = in_err_ch(o, len(temp_menu)-1, 0, 1)
                            
                            if z == 1 or z == 2 or z == 0:
                                break
                            elif z == 3:
                                m += 1
                                continue
                            elif z == 4:
                                m -= 1
                                continue
                            
                    elif a == 5:
                        #-----------------special attacks----------------------
                        while True:
                            temp_menu = ['Your team special attacks:']
                            for x in team_1:
                                temp_menu.append(f'{x.name}:')
                                if x.magic:
                                    temp_menu.append(f" magic:")
                                    for y in x.magic:
                                        temp_menu.append(f'  {y.name} for {y.value}, cost:{y.m_cost}')
                                        
                                if x.skill:
                                    temp_menu.append(f" skills:")
                                    for y in x.skill:
                                        temp_menu.append(f'  {y.name} for {y.value}, cooldowns: initial= {y.init_cooldown} normal= {y.max_cooldown}')
                                    
                                if x.passive:
                                    temp_menu.append(f" passives:")
                                    for y in x.passive:
                                        temp_menu.append(f'  {y.name} for {y.value}')
                                        
                                if not x.magic + x.skill + x.passive:
                                    temp_menu.append(f' No special attacks')
                                    
                                temp_menu.append('')
                            
                            menu_print(temp_menu)
                                
                            o = input('Type anything besides next and back to exit ')
                            
                            o, z = in_err_ch(o, len(temp_menu)-1, 0, 1)
                            
                            if z == 1 or z == 2 or z == 0:
                                break
                            elif z == 3:
                                m += 1
                                continue
                            elif z == 4:
                                m -= 1
                                continue
                        
                    elif a == 6:
                        #------------------------material display---------------------
                        while True:
                            if held_mater:
                                temp_menu = ['Currently held materials:']
                                orig, orig_count = nice_drop_comm(held_mater, 1)
                                
                                #--------------(flexible)length setter----------------
                                max_len = 0                      #flexible name length(-s-t-o-l-e-n- taken from stat_print)
                                for x in [x.name for x in orig]:
                                    if len(x) > max_len:
                                        max_len = len(x)
                                
                                #-----------------actual comment section-----------------
                                for x, y, in zip(orig, orig_count):       #iterating over items and their count
                                    line = f'{y}*{stat_len(x.name, max_len)}: value:{x.cost} '
                                    
                                    if x.attrib:                                #if they have attributes
                                        line += f'attributes:'
                                        for z in x.attrib:
                                            line += f'{z} '
                                        else:
                                            line += f'{x.attrib_lvl}'
                                            
                                    temp_menu.append(line)
                            
                            else:
                                temp_menu = ['No materials are currently held in inventory']
                            
                            menu_print(temp_menu)
                                
                            o = input('Type anything besides next and back to exit ')
                            
                            o, z = in_err_ch(o, len(temp_menu)-1, 0, 1)
                            
                            if z == 1 or z == 2 or z == 0:
                                break
                            elif z == 3:
                                m += 1
                                continue
                            elif z == 4:
                                m -= 1
                                continue
                            
                        del orig, orig_count, max_len, line
                        
                    elif a == 7:
                        #-------------kill counter display-----------------
                        while True:
                            if kill_counter[0]:
                                temp_menu = ['You have slain a total of:']
                                for x, y in zip(num2char(kill_counter[0]), kill_counter[1]):
                                    temp_menu.append(f'{y} {x.name}')
                                
                                menu_print(temp_menu)
                                
                                o = input('Type anything besides next and back to exit ')
                                o, z = in_err_ch(o, len(temp_menu)-1, 0, 1)
                                
                                if z == 1 or z == 2 or z == 0:
                                    break
                                elif z == 3:
                                    m += 1
                                    continue
                                elif z == 4:
                                    m -= 1
                                    continue
                            else:
                                menu_print(['You have not slain anything yet.'])
                                pause()
                                break
                    
                    elif a == 8:
                        break

            elif a == 2 or a == 4:
                while True:
                    if a == 2:
                        if held_weapons:         #if you hav any weapon in eq
                            y = -1
                            temp_menu = ['Currently held weapons:']
                            for x in held_weapons:                 #printing weapons with stats
                                y += 1
                                temp_menu.append(f' {y}. {x.stat_name}: damage:{x.stat_dmg}({x.dmg_var}) {x.dmg_type_1} {x.dmg_type_2}')
                            
                            menu_print(temp_menu)
                            
                            o = input('Choose weapon to equip(type "ex" to exit) ')
                            
                        else:
                            menu_print(["You don't hold any weapons in inventory"])
                            pause()
                            break
                    else:
                        if held_armor:
                            y = -1
                            temp_menu = ['Currently held armor:']
                            for x in held_armor:
                                y += 1
                                temp_menu.append(f' {y}. {x.stat_name}: defence:{x.stat_defence} defence type:{x.defence_type}')
                            
                            menu_print(temp_menu)
                            
                            o = input('Choose armor to equip(type "ex" to exit) ')
                            
                        else:
                            menu_print(["You don't have any armor in inventory"])
                            pause()
                            break
                        
                    o, z = in_err_ch(o, len(temp_menu)-2)

                    if z == 1:
                        continue
                    elif z == 2:
                        break
                    elif z == 3:
                        m += 1
                        continue
                    elif z == 4:
                        m -= 1
                        continue
                    
                    y = -1
                    temp_menu = ['Characters:']
                    
                    for x in team_1:                         #printing char with info about weapon
                        y += 1
                        
                        if a == 2:
                            if x.weapon.ID == basic.ID:
                                temp_menu.append(f' {y}. {x.stat_name} current weapon: {x.weapon.stat_name}')
                            else:
                                temp_menu.append(f' {y}. {x.stat_name} current weapon: {x.weapon.stat_name} damage:{x.weapon.stat_dmg}({x.weapon.dmg_var})')
                        else:
                            if x.armor.ID == basal.ID:
                                temp_menu.append(f' {y}. {x.stat_name} current armor: {x.armor.stat_name}')
                            else:
                                temp_menu.append(f' {y}. {x.stat_name} current armor: {x.armor.stat_name} defence:{x.armor.stat_defence} defence type:{x.armor.defence_type}')
                    
                    menu_print(temp_menu)
                    if a == 2:
                        l = input('Choose character that will wield this weapon(type "ex" to exit) ')
                    else:
                        l = input('Choose character that will wear this armor(type "ex" to exit) ')
                    
                    l, z = in_err_ch(l, len(temp_menu)-2)

                    if z == 1:
                        continue
                    elif z == 2:
                        break
                    elif z == 3:
                        m += 1
                        continue
                    elif z == 4:
                        m -= 1
                        continue
                    
                    if a == 2 and team_1[l].weapon.ID != basic.ID:                         #if char already has a weapon
                        menu_print([f'{team_1[l].name} already has a {team_1[l].weapon.name} equipped'], 1)
                        
                        x = input(f'Unequip {team_1[l].weapon.name} and equip {held_weapons[o].name}? (yes to confirm) ')
                        if x != 'yes':         #only yes will allow  to equip a weapon
                            continue
                    elif a == 4 and team_1[l].armor.ID != basal.ID:
                        menu_print([f'{team_1[l].name} already wears {team_1[l].armor.name} armor'], 1)
                        
                        x = input(f'Unequip {team_1[l].armor.name} armor and equip {held_armor[o].name} armor? (yes to confirm) ')
                        if x != 'yes':
                            continue
                        
                    if a == 2:
                        v = team_1[l].weapon                                 #settin placeholder for weapon
                        team_1[l].unequip_weapon()                  #unequipping weapon old
                        
                        held_weapons[o].equip(team_1[l])            #equipping new weapon
                        menu_print([f'{team_1[l].name} now wields {held_weapons[o].name}'], 1)     #comment
                        pause()
                        
                        held_weapons.pop(o)            #deleting new weapon from held weapons
                        if v.ID != basic.ID:             #if old weapon existed(wasnt basic)
                            held_weapons.append(v)                    #add old weapon to held weapons
                        held_weapons.sort(key = sortid)
                    else:
                        v = team_1[l].armor             #setting placeholder for armor
                        team_1[l].unequip_armor()           #unequipping old armor
                        
                        held_armor[o].equip(team_1[l])      #equipping new one
                        menu_print([f'{team_1[l].name} now wears {held_armor[o].name}'], 1)  #comment
                        pause()
                        
                        held_armor.pop(o)           #deleting new one from held armor
                        if v.ID != basal.ID:          #if old weapon wasn't basal(was normal armor)
                            held_armor.append(v)            #add old one to held armor
                        held_armor.sort(key = sortid)       #sort

                
            elif a == 3 or a == 5:
                while True:
                    v = []                                       #list for those with equipment
                    y = -1          #LEAVE IT, do not enumerate it, it has to be this way
                    for x in team_1:
                        if a == 3 and x.weapon.ID == basic.ID:       #if holds basic weapon then doesn't count
                            continue
                        elif a == 5 and x.armor.ID == basal.ID:    #if holds basic armor then doesn't count
                            continue
                        
                        y += 1
                        v.append(x)                               #creating temporary list for wielders/holders of equipment
                        
                        if y == 0:
                            if a == 3:
                                temp_menu = ['Characters currently wielding a weapon:']
                            elif a == 5:
                                temp_menu = ['Characters with their armor equipped:']
                        
                        if a == 3:
                            temp_menu.append(f'{y}. {x.stat_name}: {x.weapon.stat_name} damage:{x.weapon.stat_dmg}({x.weapon.dmg_var})')
                        elif a == 5:
                            temp_menu.append(f'{y}. {x.stat_name}: {x.armor.stat_name} defence:{x.armor.stat_defence}')
                            
                    if y == -1:
                        if a == 3:
                            menu_print(['None of your characters hold a weapon'], 1)
                            pause()
                            break
                        elif a == 5:
                            menu_print(['None of your characters is armored'], 1)
                            pause()
                            break
                        
                    menu_print(temp_menu)
                    
                    if a == 3:
                        z = 'Choose one that will unequip his weapon'                    
                    elif a == 5:
                        z = 'Choose one that will take off his armor'
                    z += ' (type "ex" to quit): '
                    
                    o = input(z)
                    
                    o, z = in_err_ch(o, len(temp_menu)-1)

                    if z == 1:
                        continue
                    elif z == 2:
                        break
                    elif z == 3:
                        m += 1
                        continue
                    elif z == 4:
                        m -= 1
                        continue
                    
                    if a == 3:
                        menu_print([f'{v[o].name} has unequipped {v[o].weapon.name}.'])
                        held_weapons.append(v[o].weapon)       #adding old weapon to eq
                        held_weapons.sort(key = sortid)      #sorting
                        v[o].unequip_weapon()               #unequipping weapon
                    elif a == 5:
                        menu_print([f'{v[o].name} took off {v[o].weapon.name}.'])
                        held_armor.append(v[o].armor)
                        held_armor.sort(key = sortid)
                        v[o].unequip_armor()
                    
                    pause()
                    break

            elif a == 6:
                break
    elif a == 5:
        while True:
            temp_menu = [
            'Menu',
            ' 1. Show help',
            ' 2. Settings',
            ' 3. Save gamestate',
            ' 4. Load gamestate',
            ' 5. Exit'
            ]
            menu_print(temp_menu)
            
            a = input('Choose: ')
            
            a, z = in_err_ch(a, len(temp_menu)-1, 1)

            if z == 1:
                continue
            elif z == 3:
                m += 1
                continue
            elif z == 4:
                m -= 1
                continue
            
            if a == 1:
                while True:
                    temp_menu = [
                    'Available mechanic explainations:',
                    ' 1. Damage type modifiers',
                    ' 2. Experience system',
                    ' 3. Battle system',
                    ' 4. Special attacks'
                    ]
                    
                    menu_print(temp_menu)
                    
                    o = input('Choose(type "ex" to exit): ')
                    
                    o, z = in_err_ch(o, len(temp_menu)-1, 1)

                    if z == 1:
                        continue
                    elif z == 2:
                        break
                    elif z == 3:
                        m += 1
                        continue
                    elif z == 4:
                        m -= 1
                        continue
                    
                    if o == 1:
                        temp_menu = [
                        '--Damage type modifier--',
                        'As of writing this help, only working damage types are blunt, slash, pierce and none.',
                        '',
                        'Blunt and slash type damage modifiers are dependent on character damage and opponent defence.',
                        'Pierce and slash damage type modifiers are independent from opponent defence value.',
                        '',
                        'Blunt works better(than none type) versus enemies with medium to high armor value.',
                        'Slash on the other hand excels at defeating enemies with light to no armor.',
                        'Pierce applies low damage modifier that is unaffected by defence of the opponent',
                        'None does not apply any damage modifier.',
                        '',
                        'Damage modifiers for blunt and piercecan not be bigger that oponents defence.',
                        'These will be forcefully lowered. Slash is unaffected by this.'
                        ]
                        sec_menu = ['///written in 0.1.005///']
                        
                    if o == 2:
                        temp_menu = [
                        '--Experience system--',
                        'At the end o feach succesful battle player will receive certain amount of experience. How much is determined either by enemies in enemy team or set manually.',
                        '',
                        'Then experience is divided by number of characters, tha player fought with and distributed evenly between them.',
                        '',
                        'Once enough experience points are gained, character will gain a new level.',
                        'Levels increase statistics (health and maximal mana) but also decrease experience gain a bit and increase experience required to gain another level.',
                        'Additionally, every 5 levels (for now) each character, that has special attacks will have them upgraded.'
                        ]
                        sec_menu = ['///written in 0.4.005///']
                    
                    if o == 3:
                        temp_menu = [
                        '--Battle system--',
                        'Battle is divided by turns in which each character from both teams acts once.',
                        'Enemy actions are set by functions.',
                        '',
                        'Actions are divided on attacking, using item and fleeing.',
                        'Damage dealt is calculated by damage and damage variable of attacker and is then reduced by defenders defence.',
                        '',
                        'Special attacks are in developmet and may not work correctly,',
                        '',
                        'Items usage and effect depend on type of item. One can heal, other apply buffs.',
                        '',
                        'Fleeing does nothing more than quitting current fight.',
                        '',
                        'Battle is ended by either fleeing or when health points of all characters in a team are reducedd to zero.',
                        'At the beginning of each fight health and mana is restored. At the end of turn some mana is restored'
                        ]
                        sec_menu = ['///written in 0.3.004d///']
                        
                    if o == 4:
                        temp_menu = [
                        '--Special attacks--',
                        'Currently there are 3 distinct special attacs: skills, magic and passives.',
                        '',
                        'Skills currently are intended to be stronger versions of normal attacks, meaning that they apply some effect to single target attack.(in future they may apply buffs, debuffs)',
                        'Before using a skill one must wait for its coolown to expire(cooldown is counted in turns).',
                        'At the beginning of each battle skills are put on initial cooldown. After using skills it is also put on cooldown.',
                        '',
                        'Magic is currently being focused arround applying healing and dealing area of effect damage.',
                        'Each character capable of using magic has its own mana storage and each spell takes some of it to take effect.',
                        'Mana storage is filled a bit each turn indicated by "(+5)" in display of team statistics.',
                        '',
                        'Passives have minor effect like healing, dealing damage, debuffing(not yet though).',
                        'Effect of passives is shown after turn(after everyone has attacked).',
                        'They are in effect as long as character, that is source of it is alive.',
                        ]
                        sec_menu = ['///written is 0.4.000e///']
                        
                    if o != 0:
                        menu_print(temp_menu, 0, 2, sec_menu)
                        pause()
                
            if a == 2:
                while True:
                    y = 0
                    temp_menu = [
                    'Available options(1 means enabled, 0 means disabled):',
                    f' 1. Damage type modifiers: {settings["1"]}',
                    f' 2. Better enemy AI: {settings["2"]}',
                    ]
                    menu_print(temp_menu)
                    
                    o = input('Choose(type "ex" to exit): ')
                    
                    o, z = in_err_ch(o, len(temp_menu)-1, 1)
                    
                    o = str(o)

                    if z == 1:
                        continue
                    elif z == 2:
                        break
                    elif z == 3:
                        m += 1
                        continue
                    elif z == 4:
                        m -= 1
                        continue

                    menu_print([])
                    
                    if settings[o] == 1:
                        l = input('Do you want to disable this option?(type "yes" to confirm) ')
                        if l == 'yes':
                            settings[o] = 0
                    elif settings[o] == 0:
                        l = input('Do you want to enable this option?(type "yes" to confirm) ')
                        if l == 'yes':
                            settings[o] = 1
                
                
            if a == 3:
                with open(savename, 'w') as save:
                    t_lis = []
                    
                    save.write(version + '\n')
                    for char in team_1:
                        exp_save = stat_len(char.total_exp, 8, 1, '0')
                        
                        save.write('char')
                        save.write(stat_len(char.ID, 4, 1, '0'))
                        save.write(stat_len(char.weapon.ID, 4, 1, '0'))
                        save.write(stat_len(char.armor.ID, 4, 1, '0'))
                        save.write(exp_save[:-4])   #splitting total exp into two sets
                        save.write(exp_save[4:])
                        save.write('---\n')
                    for item in held_items:
                        save.write('item')
                        save.write(stat_len(item.ID, 4, 1, '0'))
                        save.write('---\n')
                    for weap in held_weapons:
                        save.write('weap')
                        save.write(stat_len(weap.ID, 4, 1, '0'))
                        save.write('---\n')
                    for armo in held_armor:
                        save.write('armo')
                        save.write(stat_len(armo.ID, 4, 1, '0'))
                        save.write('---\n')
                    
                    if kill_counter[0]:
                        save.write('kiid')
                        for x in kill_counter[0]:
                            save.write(stat_len(x, 4, 1, '0'))
                        save.write('---\n')
                        
                        save.write('kinm')
                        for x in kill_counter[1]:
                            save.write(stat_len(x, 4, 1, '0'))
                        save.write('---\n')
                    
                    if cmsn_kill_counter[0]:
                        save.write('ckid')            #comission kill id
                        for x in cmsn_kill_counter[0]:
                            save.write(stat_len(x, 4, 1, '0'))
                        save.write('---\n')
                        
                        save.write('cknm')         #comission kill index?
                        for x in cmsn_kill_counter[1]:
                            save.write(stat_len(x, 4, 1, '0'))
                        save.write('---\n')
                    
                    if accept_cmsn.ID != cmsn_empty.ID:
                        save.write('cmsn')
                        save.write(stat_len(accept_cmsn.ID, 4, 1, '0'))
                        save.write('---\n')
                        
                        if accept_cmsn.prog_kill:
                            t_lis = char2num(accept_cmsn.prog_kill)
                            save.write('cpkd')                #comission progress kill id
                            for x in t_lis:
                                save.write(stat_len(x, 4, 1, '0'))
                            save.write('---\n')
                            save.write('cpkc')             #comission progress kill counter
                            for x in accept_cmsn.prog_kill_cnt:
                                save.write(stat_len(x, 4, 1, '0'))
                            save.write('---\n')
                        
                        if accept_cmsn.prog_item:
                            t_lis = char2num(accept_cmsn.prog_item)
                            save.write('cpid')                #comission progress item id
                            for x in t_lis:
                                save.write(stat_len(x, 4, 1, '0'))
                            save.write('---\n')
                            save.write('cpic')             #comission progress item counter
                            for x in accept_cmsn.prog_item_cnt:
                                save.write(stat_len(x, 4, 1, '0'))
                            save.write('---\n')
                        
                        save.write('c--\n')
                        
                    save.write('gold')
                    t_gold = stat_len(gold, 8, 1, '0')
                    save.write(t_gold)
                    save.write('---\n')
                    
                    del exp_save, t_gold, x, char, t_lis
                menu_print(['Game state saved correctly'], 1)
                pause()
#for me in future:
# save writes header that corresponds to data and then said data
# data is always read with 4 bytes(letters)
# they can be written in any order(except experience in char, which after exp_time is on, reads 8 bytes), since loading operates
#  on headers to write data
# characters are taken for baseline(deepcopied characters), assigned to temporary teams and given statistics/items/exp
#  weapons, amor, items are taken from global lists and assigned to temporary lists
#  gold is plainly assigned to gold(current)
# after one package of data has been read, '---\n' is used to mark end of data pack
                    
            if a == 4:
                try:
                    with open(savename, 'r') as save:
                        save.readline()
                        temp_team = []
                        temp_weap = []
                        temp_item = []
                        temp_armo = []
                        temp_kill_cnt = [[], []]
                        temp_cmsn_kill_cnt = [[], []]
                        temp_cmsn = cmsn_empty
                        temp_prog_kill = []
                        temp_prog_kill_cnt = []
                        temp_prog_item = []
                        temp_prog_item_cnt = []
                        line = ' '
                        count = -1
                        while line != '':
                            line = save.read(4)
                            
                            if line == 'char':
                                count += 1
                                exp_count = 0
                                exp_time = 0
                                temp_exp = ''
                                while line != '---\n':
                                    line = save.read(4)
                                    
                                    try:
                                        line = int(line)
                                    except:
                                        pass
                                    else:
                                                
                                        if exp_time == 1:          #experience should always be read last
                                            if exp_count == 0:
                                                temp_exp += stat_len(line, 4, 1, '0')
                                                exp_count = 1
                                            else:
                                                temp_exp += stat_len(line, 4, 1, '0')
                                                
                                            if len(temp_exp) == 8:
                                                temp_team[count].total_exp = int(temp_exp)
                                                temp_team[count].exp = int(temp_exp)
                                                temp_team[count].level_up_check(1)
                                                exp_time = 0
                                            continue
                                        
                                        for x in global_allies_baseline:
                                            if x.ID == line:
                                                temp_team.append(deepcopy(x))
                                                
                                        for x in global_weapons:
                                            if x.ID == line:
                                                x.equip(temp_team[count])
                                                
                                        for x in global_armor:
                                            if x.ID == line:
                                                x.equip(temp_team[count])
                                                exp_time = 1      #exp_time allows to load exp and execute level up
                                                
                            elif line == 'weap':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        pass
                                    else:
                                        for x in global_weapons:
                                            if x.ID == line:
                                                temp_weap.append(x)
                                                
                            elif line == 'item':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        pass
                                    else:
                                        for y in global_items.values():
                                            for x in y:
                                                if x.ID == line:
                                                    temp_item.append(x)
                                                    
                            elif line == 'armo':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        pass
                                    else:
                                        for x in global_armor:
                                            if x.ID == line:
                                                temp_armo.append(x)
                                                
                            elif line == 'gold':
                                while line != '---\n':
                                    line = save.read(8)
                                    try:
                                        line = int(line)
                                    except:
                                        break
                                    else:
                                        gold = line
                            
                            elif line == 'kiid':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        pass
                                    else:
                                        temp_kill_cnt[0].append(line)
                               
                            elif line == 'kinm':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        pass
                                    else:
                                        temp_kill_cnt[1].append(line)
                            
                            elif line == 'ckid':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        pass
                                    else:
                                        temp_cmsn_kill_cnt[0].append(line)
                                
                            elif line == 'cknm':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        pass
                                    else:
                                        temp_cmsn_kill_cnt[1].append(line)
                            
                            elif line == 'cmsn':
                                line = save.read(4)
                                for x in global_cmsn:
                                    if x.ID == int(line):
                                        temp_cmsn = x
                                save.read(4)

                                while line != 'c--\n':
                                    line = save.read(4)
                                    if line == 'cpkd':
                                        z = 'cpkd'
                                    elif line == 'cpkc':
                                        z = 'cpkc'
                                    elif line == 'cpid':
                                        z = 'cpid'
                                    elif line == 'cpic':
                                        z = 'cpic'
                                    
                                    while line != '---\n' and line != 'c--\n':
                                        line = save.read(4)
                                        try:
                                            line = int(line)
                                        except:
                                            pass
                                        else:
                                            if z == 'cpkd':
                                                temp_prog_kill.append(num2char([line])[0])     #sorry, but num2char takes in lists, so i'm...
                                            elif z == 'cpkc':                                  #...converting back and forth between...
                                                temp_prog_kill_cnt.append(line)                #...list and int
                                            elif z == 'cpid':
                                                temp_prog_item.append(num2char([line])[0])
                                            elif z == 'cpic':
                                                temp_prog_item_cnt.append(line)
                                    
                        if len(temp_kill_cnt[0]) != len(temp_kill_cnt[1]):
                            raise(Exception('KillCounterLenNotEqual'))
                        
                        team_1 = temp_team
                        held_weapons = temp_weap
                        held_items = temp_item
                        held_armor = temp_armo
                        kill_counter = temp_kill_cnt
                        cmsn_kill_counter = temp_cmsn_kill_cnt
                        
                        accept_cmsn = temp_cmsn
                        accept_cmsn.prog_kill = temp_prog_kill
                        accept_cmsn.prog_kill_cnt = temp_prog_kill_cnt
                        accept_cmsn.prog_item = temp_prog_item
                        accept_cmsn.prog_item_cnt = temp_prog_item_cnt
                        
                    
                    del line, temp_team, temp_weap, temp_item, temp_armo, temp_exp, temp_kill_cnt, temp_cmsn_kill_cnt, exp_time, x, y, count
                    del temp_cmsn, temp_prog_kill, temp_prog_kill_cnt, temp_prog_item, temp_prog_item_cnt
                    
                    menu_print(['Game state loaded correctly'], 1)
                    pause()
                    
                except IndexError:
                    menu_print([f'File {savename} is outdated/invalid'], 1)
                    pause()
                    
                except:
                    menu_print([f'File {savename} used as save does not exist'], 1)
                    pause()

            if a == 5:
                break
    elif a == 6:
        quit()
    elif a == 7 and dev_opt == 'xel':
        while True:
            temp_menu = [
            'developer options',
            '1. gain level of exp for all and lvl_check()',
            '2. go back'
            ]
            
            menu_print(temp_menu)
            
            a = input("Choose: ")

            a, z = in_err_ch(a, len(temp_menu)-1, 1)

            if z == 1:
                continue
            elif z == 2:
                break
            elif z == 3:
                m += 1
                continue
            elif z == 4:
                m -= 1
                continue
            
            if a == 1:
                o = input('how many times ')
                temp_menu = []
                for _ in range(int(o)):
                    for x in team_1:
                        exp_needed = 200 * x.level
                        x.exp += exp_needed
                        x.total_exp += exp_needed
                        x.level_up_check()
                del exp_needed
                
                while True:
                    
                     menu_print(temp_menu)
                     a = input()
                 
                     a, z = in_err_ch(a, len(temp_menu)-1, 0, 1)
                     if z == 3:
                         m += 1
                     elif z == 4:
                         m -= 1
                     else:
                         break
            if a == 2:
                break
