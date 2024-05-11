from random import randint           #for random intiger (duh...)
from copy import deepcopy            #for copying class instances

#z is for while loops(used in error protection) AND another placeholder used in for loop (used first in fight_choose print)
#s is secondary for while loops(also used in error protection)
#o is for returns/data to be used outside of function AND targeting AND choices
#l is secondary/placeholder for choices
#p is secondary for targeting  AND better looking inventory prints(see item.buy_item) AND better looking class t_comm
#X AND Y AND W are for 'for' loops
#y is for counter in for loop
#v is for empty input(not in pause func) AND a mostly used placeholder
#k is tertiary placeholder
#c is for choosing which option of function run
#a is for choosing what to do(in wide/main function)
#d is for choosing in dictionaries(see shop>buy items)
#p is for better looking inventory prints(see item.buy_item)
#t_target used for getting out of item_fnc targets

#function zone

def pause():
    emptyinput = input("Press anything to continue ")      #function for pausing

#-------------sort_keys_here----------------------------
sortid = lambda y : y.ID


def stat_len(x, y=1, c=0):      #x is value to be lengthened, y is length, c is option choosing
    x = str(x)
    while len(x) < y and c == 0:           #adds ' ' to the end
        x += ' '
    while len(x) < y and c == 1:          #adds ' ' to the beginning
        x = ' ' + x
    return x
        
def type_check(char, enem, atk_dmg):    #(character that attacks, enemy that defends, attack damage)
                                        #depending on weapon.dmg_type returns dmg_bonus and dmg_reduction
    bon = 0         #these two are for weapons that have no dmg_type
    red = 0
    x = char.weapon.dmg_type_1
    z = char.weapon.dmg_type_2
    y = enem.defence
    if x == 'blunt' or z == 'blunt':    #blunt
        bon = int(atk_dmg*0.4)
        red = int(atk_dmg*0.2)
        if bon > y:      #prevents bon or red from going over the defence
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
    return bon, red   #for none types

def stat(char, c=0):      #(character, c=0:basic stats c=1:extended stats)
    if c == 0:                   #displays statictics
        print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence)
    elif c == 1:             #displays statistics with weapons and armor
        x = ''
        if char.weapon.ID == basic.ID and char.armor.ID == basal.ID:
            x = stat_len(x, 18, 1)
            print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' armor:' + char.armor.stat_name + x + ' weapon:' + char.weapon.stat_name)
        elif char.weapon.ID != basic.ID and char.armor.ID == basal.ID:
            x = stat_len(x, 18, 1)
            print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' armor:' + char.armor.stat_name + x + ' weapon:' + char.weapon.stat_name + ' dmg:' + str(char.weapon.dmg) + ' var:' + str(char.weapon.dmg_var))
        elif char.weapon.ID == basic.ID and char.armor.ID != basal.ID:
            print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' armor:' + char.armor.stat_name + ' armor defence:' + char.armor.stat_defence + ' weapon:' + char.weapon.stat_name)
        else:
            print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' armor:' + char.armor.stat_name + ' armor defence:' + char.armor.stat_defence + ' weapon:' + char.weapon.stat_name + ' dmg:' + str(char.weapon.dmg) + ' var:' + str(char.weapon.dmg_var))


def EoT_summ():                                      #End of Turn summary
    print()
    print('Turn ' + str(turn) + ' summary:')
    for x in all_fghtr:      #prints what character did in a turn
        if x == False:
            continue
        print(x.t_comm)
        if x.hp <= 0:
            x.t_comm = x.name + ' died'
        else:
            x.t_comm = x.name + ' did not do a thing'

def stat_print(c=0):                # 0=print everyone, 1=print friendly team, 2=print enemy team, 3=print more about friendly team
    print()
    if c==0 or c==1 or c==3:
        for x in team_1:
            if x == False:
                continue
            if c==3:
                stat(x, 1)
            else:
                stat(x)
    if c==0 or c==2:
        for x in team_2:
            if x == False:
                continue
            stat(x)

def team_target(c):        #used for choosing target  #(c=0 target is team_1 c=1 target is team_2)
    global o          #no returns instead working on global o
    z = 0
    if c==1:               #target is team_1
        while True:
            y = -1
            for x in team_1:
                y += 1
                if x == False:
                    continue
                if x.hp <= 0:         #can't target for attack/buff/debuff/heal deadman (not here at least)
                    continue
                print(str(y) + '. ' + x.stat_name + ' ' + x.stat_hp + '/' + x.stat_maxhp)            #printing team_1 members with indexes
                
            o = input('Choose: ')
            
            try:                     #error check
                o = int(o)
            except:
                print('Wrong input')
                print()
                continue
            else:
                if o < 0 or o > y:
                    print('Choice out of range')
                    print()
                    continue
                if team_1[o].hp <= 0:
                    print(team_1[o].name + ' is already dead')
                    p = input('Do you want to act upon a dead body?(type "yes" to confirm) ')
                    if p == 'yes':
                        break
                    else:
                        continue
                break
                    
    if c==2:
        while True:
            y = -1
            for x in team_2:
                if x == False:
                    continue
                if x.hp <= 0:      #can't target for attack/buff/debuff/heal deadman (not here at least)  ######actually you can
                    y += 1
                    continue
                y += 1
                print(str(y) + '. ' + x.stat_name + ' ' + x.stat_hp + '/' + x.stat_maxhp)   #printing team_1 members with indexes
                
            o = input('Choose: ')
            
            try:           #error check
                o = int(o)
            except:
                print('Wrong input')
                print()
                continue
            else:
                if o < 0 or o > y:
                    print("Choice out of range")
                    print()
                    continue
                else:
                    if team_2[o].hp <= 0:
                        print(team_2[o].name + ' is already dead')
                        p = input('Do you want to act upon a dead body?(type "yes" to confirm) ')
                        if p == 'yes':
                            break
                        else:
                            continue
                    else:
                        break

def fight_end(c, y=0, z=0):            #c is just to choose which side won, y is for gold obtained input
    global gold
    
    if c == 1:         #if team_1 won
        stat_print()
        print()
        print('You won the fight')       #print some info
        v = 0   #gold gained
        l = 0   #exp gained
        if y == 0:                #if gold is not specified
            for x in team_2:         #get gold gained from monster gold_drop
                v += x.g_drop
            print('You gained ' + str(v) + ' gold')
            gold += v     #add gained gold
            
        elif y != 0:        #if gold was specified
            print('You won the fight')
            print('You gained ' + str(y) + ' gold')
            gold += y        #gain set amount f gold
            
        if z == 0:
            for x in team_2:
                l += x.exp_drop
            l = int(l/len(team_1))
            
            for x in team_1:
                x.exp += l - int(l*(x.level-1)/100)
                x.total_exp += l - int(l*(x.level-1)/100)
                print(x.name + ' gained ' + str(l) + ' experience points')
        
        elif z != 0:
            l = int(z/len(team_1))
            for x in team_1:
                x.exp += l - int(l*(x.level-1)/100)
                x.total_exp += l - int(l*(x.level-1)/100)
                print(x.name + ' gained ' + str(l) + ' experience points')
        
        for x in team_1:
            x.level_up_check()

    if c == 2:        #if team_2 won
        stat_print()
        print('You lost the fight')
        print('What a shame...')
        print()
        
def fight_end_check(v=0, z=0):          #checking if battle ended V is for setting gold gained, Z is for experience obtained
    x = 0
    for y in team_1:
        if y == False:
            continue
        x += y.hp       #summing up hp of team_1 fighters
    if x <= 0:     #if it's less or equal than 0
        EoT_summ()    #summarise the turn
        fight_end(2)    #use <- function
        return 'end'    #used for breaking loops
    
    x = 0
    for y in team_2:
        if y == False:
            continue
        x += y.hp       #summng hp of team_2 fighters
    if x <= 0:   #if it's less or equal 0
        EoT_summ()    #summarise turn
        fight_end(1, v, z)   #use <- function with v for gained g
        return 'end'   #used for breaking loops

def fight(ally, enem, g_gain=0, exp_gain=0):
    global team_1, team_2, o, p, all_fghtr, all_fghtr_dict, turn, held_items, l, x
    team_1 = ally          #setting teams from input
    team_2 = enem
    all_fghtr = team_1 + team_2   #ading all fighters to a list
    
    all_fghtr_dict = {}        #for buff.char access
    for x in all_fghtr:
        key = x.name
        all_fghtr_dict[key] = x

    turn = 0
    
    for x in all_fghtr:                    #heal for next battle
        if x == False:
            continue
        x.heal_up()

    for x in team_1:        #setting variable for turn fighting
        x.team = 'allies'
    for x in team_2:
        x.team = 'monsters'
    
    e = ''  #for end check
    z = 0
    s = 0
    while z == 0:
        print()
        turn += 1
        print('Turn: ' + str(turn))
            
        for x in all_fghtr:
            while z == 0:
                if x == False or x.hp <= 0:
                    break
                if x.team == 'allies':
                    print()
                    print(x.name + ' turn')
                    print("1.Attack 2.Use item 3.Flee")
                    a = input("choose a number: ")
                    
                    try:              #error checking
                        a = int(a)
                    except:
                        print('Wrong input')
                        continue
                    else:
                        if a <= 0 or a > 3:
                            print('Choice out of range')
                            continue
                    
                    if a == 1:
                        print('Who does ' + x.name + ' attack? ')
                        team_target(2)                              #choosing target
                        p = team_2[o]                                           #defining p for class comment in deal_dmg
                        dmg = x.deal_dmg()                              #setting damage
                        team_2[o].take_dmg(dmg)                 #target receiving damage
                        e = fight_end_check(g_gain, 500)      #end check
                        break
                    elif a == 2:
                        print('Available items:')
                        y = -1
                        for w in held_items:
                            y += 1
                            print(str(y) + '. ' + w.stat_name +': function:' + w.fnc_name + ' for:' + str(w.x))
                        
                        l = input('Choose (type "ex" to quit): ')
                            
                        try:                             #error checking
                            l = int(l)
                        except:
                            if l == 'ex':
                                continue
                            else:
                                print('Wrong input')
                                print()
                                continue
                        else:
                            if l < 0 or l > y:
                                print('Choice out of range')
                                print()
                                continue
                        v = held_items[l].name
                        x.t_comm = held_items[l].use_item()
                        
                        print(x.t_comm)
                        
                        pause()
                        e = fight_end_check(g_gain, exp_gain)
                        break
                    elif a == 3:
                        print('You fleed from battle')
                        print()
                        z = 1
                        pause()
                        break
                elif x.team == 'monsters':
                    if settings['2'] == 0:      #setting for better AI
                        o = randint(0,len(team_1)-1)                                                  #enemy choosing random target
                        while team_1[o] == False or team_1[o].hp <= 0:
                            o = randint(0,len(team_1)-1)                                 #enemy choosing random target again if chose empty fighter place or fighter dead
                    else:
                        o, secondary = x.AI(x)
                                
                        o = team_1.index(o)
                        
                        for y in team_2:              #telling helpers who to attack
                            if y.AI == AI_helper:
                                y.sugtarget = o
                        
                    p = team_1[o]
                    dmg = x.deal_dmg()
                    team_1[o].take_dmg(dmg)
                    e = fight_end_check(g_gain, exp_gain)
                    break
            if e == 'end':
                z = 1
                break
        if z == 1:
            break
        
        EoT_summ()
        active_effects_cp = deepcopy(active_effects)      #making copy since it is impossible to change dict while iterating
        for x in active_effects_cp.values():         #loop checking for this turn effects and their duration
            x.check()
        stat_print()

def shop(items, weapons, armor, red=0):
    global o, sell_red
    sell_red = red    #sell_reduction = percernage value reducing gold acquired from selling
    while True:
        print()
        print('Welcome to the shop')
        print('Current gold:' + str(gold))
        print('What do you want to do here?')
        print('1. Buy items')
        print('2. Sell items')
        print('3. Buy equipment')
        print('4. Sell equipment')
        print('5. Exit shop')
        
        a = input('Choose: ')
        
        try:
            a = int(a)
        except:
            print('Wrong input')
            print()
        else:
            if a < 1 or a > 5:
                print('Choice out of range')
                print()
        
        if a == 1:
            while True:
                print()
                print('Types of items available for sale:')
                y = -1
                d = []
                for x in items:
                    y += 1
                    print(y, '.', x)
                    d.append(x)
                o = input('Choose (type "ex" to quit): ')
                
                try:
                    o = int(o)
                except:
                    if o == 'ex':
                        z = 1
                        break
                    else:
                        print('Wrong input')
                        print()
                else:
                    if o > y or o < 0:
                        print('Choice out of range')
                        print()
                        continue
                    else:
                        z = 0
                        break
            l = o
            while z == 0:
                print()
                print('Which item do you want to buy?')
                y = -1
                v = items[d[l]]
                for x in v:
                    y += 1
                    print(str(y) + '. ' + x.stat_name + ' function:' + x.fnc_name + ' for:' + str(x.x) + ' cost:' + str(x.cost))
                o = input('Choose (type "ex" to quit): ')
                
                try:
                    o = int(o)
                except:
                    if o == 'ex':
                        break
                    else:
                        print('Wrond input')
                        print()
                else:
                    if o > y or o < 0:
                        print('Choice out of range')
                        print()
                        continue
                    else:
                        v[o].buy_item()
            pause()
        
        elif a == 2:
            while True:
                print()
                print('Value of items is reduced by ' + str(sell_red) + '% of basic cost')
                if held_items:
                    print('Your items:')
                    y = -1
                    for x in held_items:
                        y += 1
                        v = int(x.cost - x.cost * sell_red / 100)
                        print(str(y) + '. ' + x.stat_name + ': value:' + stat_len(v, 3, 1) + ' function:' + x.fnc_name + ' for:' + str(x.x))
                    o = input('Choose item for sale(type "ex" to quit): ')
                    try:
                        o = int(o)
                    except:
                        if o == 'ex':
                            break
                        else:
                            print('Wrong input')
                            continue
                    else:
                        if o < 0 or o > y:
                            print('Choice out of range')
                            continue
                    
                    held_items[o].sell_item(sell_red)
                    
                elif not held_items:
                    print("But it doesn't matter right now since you don't hold any item that can be sold")
                    pause()
                    break
        elif a == 3:
            while True:
                print('Equipment for sale:')
                y = -1
                d = []
                for x in global_equipment:
                    y += 1
                    print(str(y) + '. ' + x)
                    d.append(x)
                o = input('Choose (type "ex" to quit): ')
                try:
                    o = int(o)
                except:
                    if o == 'ex':
                        z = 1
                        break
                    else:
                        print('Wrong input')
                        print()
                else:
                    if o > y or o < 0:
                        print('Choice out of range')
                        print()
                        continue
                    else:
                        z = 0
                        break
            if z == 1:
                continue
            l = o
            v = global_equipment[d[l]]
            while z == 0:
                if v == weapons:
                    y = -1
                    for x in v:
                        y += 1
                        print(str(y) + '. ' + x.stat_name + ': cost:' + stat_len(x.cost, 3, 1) + ' damage:' + x.stat_dmg + ' variable:' + str(x.dmg_var))
    
                elif v == armor:
                    y = -1
                    for x in v:
                        y += 1
                        print(str(y) + '. ' + x.stat_name + ': cost:' + stat_len(x.cost, 3, 1) + ' defence:' + x.stat_defence)
                
                o = input('Choose(type "ex" to exit): ')
                try:
                    o = int(o)
                except:
                    if o == 'ex':
                        break
                    else:
                        print('Wrong input')
                        continue
                else:
                    if o < 0 or o > y:
                        print('Choice out of range')
                        continue
                v[o].buy_equipment()
            
            print()
            pause()
        elif a == 4:
            while True:
                print()
                print('Value of equipment is reduced by ' + str(sell_red) + '% of basic cost')
                held_equipment = held_armor + held_weapons
                if held_equipment:
                    y = -1
                    v = 0
                    for x in held_equipment:
                        y += 1
                        if y == 0:
                            print('Held equipment:')
                        value = stat_len(int(x.cost - x.cost * sell_red / 100), 3, 1)
                        if type(x) == Weapon:
                            if v == 0:
                                print(' Weapons:')
                            print('  ' + str(y) + '. ' + x.stat_name + ' value:' + value + ' damage:' + x.stat_dmg + '(' + str(x.dmg_var) + ')')
                            v += 1
                        else:
                            if y == 0:
                                print(' Armor:')
                            print('  ' + str(y) + '. ' + x.stat_name + ' value:' + value + ' defence:' + x.stat_defence)
                    
                    o = input('Choose equipment to sell(type "ex" to quit): ')
                    
                    try:
                        o = int(o)
                    except:
                        if o == 'ex':
                            break
                        else:
                            print('Wrong input')
                            continue
                    else:
                        if o < 0 or o > y:
                            print('Choice out of range')
                            continue
                        
                    if type(held_equipment[o]) == Weapon:
                        o -= v
                        held_weapons[o].sell_equipment()
                    else:
                        held_armor[o].sell_equipment()
                if not held_equipment:
                    print("But you don't have anything to sell")
                    break
                
        
        elif a == 5:
            print('You left the shop')
            break


#item function
        #return None, target   #use when item used properly
        #return not_used    #use when not used
        
def revival(hp, c=0):  #hp for health after revivalion, c=0 for ally ress c=1 for enem ress
    global k
    while True:
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
                    print('Who do you want to revive?')
                print(' ' + str(y) + '. ' + char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence)
                z.append(y)
                
        if not z:         #-------------this may be used often in future-----------------------------
            print('No one is dead')
            return(x.name + ' tried to find anyone that may be in dead need, but he just lost time(and a turn)')
            #------------------return-when-unused--------------
        
        o = input('Choose: ')
        try:
            o = int(o)
        except:
            print('Wrong input')
            continue
        else:
            if o < 0 or o > y:
                print('Choice out of range')
                continue
            
        if o in z:
            target[o].hp += hp
            if target[o].hp > target[o].maxhp:
                target[o].hp = target[o].maxhp
            target[o].stat_hp = stat_len(target[o].hp, 3, 1)
            print(target[o].name + ' has been revived and has ' + str(target[o].hp) + ' health points')
            return None, target[o]
            #-------------return-when-all-good------------
        else:
            print('This character is not dead')
            continue

def heal(x, c=0): #x for heal amount, c=0 for ally heal, c=2 for enem heal
    global t_target
    while True:
        print("Who do you want to heal? ")
        team_target(1)
        if c == 0:
            if team_1[o].hp == 0:
                print("You can't heal dead with this")
                continue
            y = team_1[o]
        elif c == 1:
            if team_2[o].hp == 0:
                print("You can't heal dead with this")
                continue
            y = team_2[o]
        v = y.hp                                      #for print measures
        y.hp += x
        
        if y.hp > y.maxhp:                     #prevent overheal
            y.hp = y.maxhp
        y.stat_hp = stat_len(y.hp, 3, 1)
        
        l = y.hp                                      #for print measures
        print(y.name + ' has been healed for ' + str(l-v) + ' health up to current ' + str(y.hp) + ' health points')
        return None, y
        #----------------return-if-good-------------


#to correctly use this in Item:
    #define (l_fnc that serves as a core of effect and does all the math
    #define (effect instance that takes in default duration, l_fnc and x)
    #define (i_fnc that begins effect circulation and adds effect to active_effects)
    #define (item with i_fnc as its function)
class Effect:           #consider doing deepcopies of it so multiple instances of the same effects can stack
    def __init__ (self, fnc):
#         self.dur = dur    #duration
        self.fnc = fnc    #function
#         self.x = x        #use in funcion
    def start(self, char, dur=0):
#         self.bturn = turn     #turn that effect had begun
#         if dur != 0:#
        self.dur = dur
        self.time = self.dur
        self.char = char
        self.fnc(self.x, char, 1)   #1 being option to begin effect
    def check(self):
        self.fnc(self.x, self.char)         #no secong arg to check for effect(if exists)
        active_effects[self.key].time -= 1     #time left
        self.time -= 1
        if self.time == 0:
            self.end()
    def end(self):
        print(self.char.name)
        self.fnc(self.x, self.char, 2)   #2 being option to cancel effect(weaken/strengthen)
        del active_effects[self.key]

#----loop-fnc-used-in-Effect----
def l_atk_upp(x, char, c=0):
    key = char.name             #why the hell does it work but global doesnt????
    char = all_fghtr_dict[key]
    if c == 1:   #start
        char.atk += x
        char.atkmin = stat_len(int(char.atkmin)+x, 2, 1)
        char.atkmax = stat_len(int(char.atkmax)+x, 2, 1)
        print(char.name + ' attack was increased by ' + str(x))
        
    elif c == 2:   #end
        char.atk -= x
        char.atkmin = stat_len(int(char.atkmin)-x, 2, 1)
        char.atkmax = stat_len(int(char.atkmax)-x, 2, 1)
        print(char.name + ' attack buff has ended')
    else:    #check
        True

def l_atk_down(x, char, c=0):
    key = char.name
    char = all_fghtr_dict[key]
    if c == 1:
        char.atk -= x
        char.atkmin = stat_len(int(char.atkmin)-x, 2, 1)
        char.atkmax = stat_len(int(char.atkmax)-x, 2, 1)
        print(char.name + ' attack was decreased by ' + str(x))
    if c == 2:
        char.atk += x
        char.atkmin = stat_len(int(char.atkmin)+x, 2, 1)
        char.atkmax = stat_len(int(char.atkmax)+x, 2, 1)
        print(char.name + ' attack debuff has ended')
    else:
        True

#_effect_fnc_
atk_up = Effect(l_atk_upp)     #Effect(dur, fnc, x)
atk_down = Effect(l_atk_down)

active_effects = {}
buff_count = 0

#_item_fnc_
def i_atk_up(x, y):            #works only for team_1
    global buff_count, t_target
    buff_count += 1        #for creating keys
    key = str(buff_count)  #creating new key
    active_effects[key] = deepcopy(atk_up)    #making copy of effect+adding it to active_effects
    active_effects[key].x = x       #assigning new x
    active_effects[key].key = key    #giving effect it's place in active effects to manipulate itself
    team_target(1)
    v = team_1[o]         #choosing target for effect
    active_effects[key].start(v, y)     #giving target to effect and starting it
    return None, v
    #------------return-if-good-----------

def i_atk_down(x, y):            #works only for team_1
    global buff_count, t_target
    buff_count += 1        #for creating keys
    key = str(buff_count)  #creating new key
    active_effects[key] = deepcopy(atk_down)    #making copy of effect+adding it to active_effects
    active_effects[key].x = x       #assigning new x
    active_effects[key].key = key    #giving effect it's place in active effects to manipulate itself
    team_target(2)
    v = team_2[o]         #choosing target for effect
    active_effects[key].start(v, y)     #giving target to effect and starting it
    return None, v
    #---------------------return-if-good----------------

print('Effects defined')

class Weapon:
    ID = 1000
    def __init__ (self, name, cost, dmg, dmg_var, dmg_type_1, dmg_type_2='none'):
        self.name = name
        self.stat_name = stat_len(name, 10)   #for stat purpose
        self.ID = Weapon.ID       #for sorting
        Weapon.ID += 1
        
        self.cost = cost
        self.dmg = dmg
        self.stat_dmg = stat_len(dmg, 3, 1)   #for stat purpose
        self.dmg_var = dmg_var
        
        self.dmg_type_1 = dmg_type_1
        self.dmg_type_2 = dmg_type_2
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
        p = 'Are you sure you want to buy: ' + self.name + '? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:        #checking if enough gold is held
                gold -= self.cost
                held_weapons.append(self)    #adding itself to held weapons
                
                print('You bought ' + self.name)
                print('You currently have ' + str(gold) + 'gold')
                
                p = 'You are currently holding '
                held_weapons.sort(key = sortid)        #sorting held weapons
                for x in held_weapons:
                    p = p + x.name + ', '           #and displaying all of them
                print(p)
            else:
                print('You do not have enough gold')
    def sell_equipment(self):
        global gold, held_weapons
        p = 'Are you sure you want to sell: ' + self.name + '? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            g_gained = int(self.cost - self.cost * sell_red / 100)
            gold += g_gained
            held_weapons.pop(o)
            print('You sold ' + self.name + ' and gained ' + str(g_gained) + ' gold')
            
            

class Armor:
    ID = 1500
    def __init__(self, name, cost, defence, defence_type='none'):
        self.name = name
        self.stat_name = stat_len(name, 10)   #for stat purpose
        self.ID = Armor.ID  #for sorting
        Armor.ID += 1
        
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
        p = 'Are you sure you want to buy: ' + self.name + '? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:        #checking if enough gold is held
                gold -= self.cost
                held_armor.append(self)    #adding itself to held armor
                
                print('You bought' + self.name)
                print('You currently have' + str(gold) + 'gold')
                
                p = 'You are currently holding '
                held_armor.sort(key = sortid)        #sorting held armor
                for x in held_armor:
                    p = p + x.name + ', '           #and displaying all of it
                print(p)
            else:
                print('You do not have enough gold')
    def sell_equipment(self):
        global gold, held_armor
        p = 'Are you sure you want to sell: ' + self.name + '? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            g_gained = int(self.cost - self.cost * sell_red / 100)
            gold += g_gained
            held_armor.pop(o)
            print('You sold ' + self.name + ' and gained ' + str(g_gained) + ' gold')
            

#-----Weapon-----
#----user-weapons----
basic = Weapon('None', 0, 0, 0, 'blunt')        #(name, cost, dmg, dmg_var, dmg_type_1, dmg_type_2='None')
bat = Weapon('Bat', 50, 1, 1, 'blunt')
sword = Weapon('Sword', 150, 4, 0, 'slash')
hammer = Weapon('Hammer', 120, 3, 1, 'blunt')
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

global_weapons = [bat, sword, hammer, creator_touch]   #for shop display
global_weapons.sort(key = sortid)

#-----Armor------
#----user-armor----
basal = Armor('None', 0, 0)  #name cost defence defence_type='none'
light = Armor('Light', 50, 2)
medial = Armor('Medial', 120, 4)
heavy = Armor('Heavy', 250, 6)
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

global_equipment = {
    'Weapons': global_weapons,
    'Armor': global_armor
    }

held_weapons = [hammer, hammer, creator_touch]
held_armor = [light, heavy, heavy, creator_skin]

print('Equipment defined')

#-------------------------------------enemy-AI----------------------------
#AI only work for enemies

# def AI_name(char):     #char is for passing down attack directive
#     AI_target, AI_secon = None, None  #AI_target is for character target of attack, AI_secon may be used in commander/soldier AI
#
#     here put what it does
#
#     return AI_target, AI_secon

def AI_random(char):       #'if i wound anyone, i will be satisfied'
    AI_target, AI_secon = None, None
    
    while True:
        y = randint(0,len(team_1)-1)                              #automatic choose of random target
        if team_1[y].hp == 0:
            continue                 #if chosen fighter is dead
        break
    team_1[y]
    
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

class Char:
    ID = 400
    def __init__ (self, name, maxhp, atk, atk_var, recr_cost=0, g_drop=0, exp_drop=0, defence=0, defence_type_1='none', weapon=basic, armor=basal, AI=AI_helper):
        self.ID = Char.ID                               #instance ID
        Char.ID += 1                                    #increasing class ID counter
        self.name = name                                 #name(duh...)

        self.maxhp = maxhp                              #maximum health
        self.hp = maxhp                                 #current health
        
        self.atk = atk                                 #attack variable
        self.atk_var = atk_var                         #attack variable variable (try to comprehand this)
        self.atkmin = atk - atk_var                    #minimal attack possibility(used only in stat)
        self.atkmax = atk + atk_var                    #maximal attack possibility(used only in stat)
        
        self.g_drop = g_drop                                                   #gold drop variable
        
        self.exp_drop = exp_drop                      #experience gained for killing
        self.total_exp = 0          #total experience used in save/load
        self.exp = 0              #experience on current level
        self.level = 1       #current level (duh...)
        
        self.recr_cost = recr_cost                    #recruitment cost
        
        self.defence = defence                             #setting innate defence

        self.defence_type_1 = defence_type_1              #future elemental system?
        self.defence_type_2 = 'none'
        self.armor = armor               #default armor
        armor.equip(self)
                
#         self.dmg_type_1 = dmg_type_1                                     #damage type for future(?) elemental system
#         self.dmg_type_2 = dmg_type_2                #these are defined by weapon.equip() and char.unequip weapon() and same for armor
        
        self.base_maxhp = maxhp         #base/starting values for when something will bet out of control or when i will ne too lazy
        self.base_atk = atk
        self.base_armor = armor
        self.base_atk_var = atk_var
        
        self.t_comm = self.name + ' did not have a chance to attack'          #turn comment if character died without taking action
        self.weapon = weapon        #default weapon
        weapon.equip(self)
        
        self.AI = AI
        self.sugtarget = None          #suggested target for 'advanced' AI
        
        self.stat_set()
    def take_dmg (self, damage):
        self.hp -= damage
        if self.hp < 0:                             #health can't be lower than zero
            self.hp = 0
        self.stat_set()
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
            self.t_comm = (self.name + ' dealt no damage to ' + p.name)                     #turn comment used in EoT_summ
        else:
            self.t_comm = (self.name + ' dealt ' + str(atk_dmg) + ' damage to ' + p.name)                      #turn comment used in EoT_summ
        return atk_dmg
    def heal_up(self):
        self.hp = self.maxhp
        self.stat_hp = stat_len(self.hp, 3, 1)  #for stat purpose
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
        print()
        if gold >= self.recr_cost:
            p = 'Are you sure you want to recruit ' + self.name + ' for ' + str(self.recr_cost) + '? '
            o = input(p)
            if o == 'yes':
                gold -= self.recr_cost
                team_1.append(self)
                global_allies.remove(self)
                print(self.name + 'has been recruited')
        else:
            print("You don't have enough money to recruit" + self.name)
    def level_up_check(self, a=0):
        exp_needed = 200*self.level     #formula for calculating
#         print('self exp ' + str(self.exp) + ' , exp needed ' + str(exp_needed))
        
        if self.exp >= exp_needed:       #if required experience is gained
            self.level += 1
            self.exp -= exp_needed    #reducing total exp by amount needed for previous level
            if a == 0:
                print(self.name + ' reached ' + str(self.level) + ' level')
            
            lvl_change_dict = {
                'hp': [0, self.base_maxhp, self.maxhp, 20, 10],   #zero serves as index, first in list is stat without equipment/buff/skill
                'atk': [1, self.base_atk, self.atk, 3, 2]       #, second is stat that is used commonly
                }                                           # , third is maximum gain, when it is met it is reduced by fourth value
            for x in lvl_change_dict:
                index     = lvl_change_dict[x][0]
                stat      = lvl_change_dict[x][1]
                limit     = lvl_change_dict[x][3]
                decrease  = lvl_change_dict[x][4]
            
                y = int(stat*0.1)
                if y == 0:      #prevents from gain being 0
                    y = 1
                while y > limit:    #limits gain
                    y -= decrease
                    
                if index == 0:           #adds gain to stat
                    self.base_maxhp += y
                    self.maxhp += y
                elif index == 1:
                    self.base_atk += y
                    self.atk += y
                
#                 print(x, stat, base_stat)
                print(x, lvl_change_dict[x][1], lvl_change_dict[x][0])
                print(lvl_change_dict[x])
                
            print(self.maxhp, self.atk)
            self.stat_set()
            self.heal_up()
            print(self.maxhp, self.atk)
    def stat_set(self):
        self.stat_name = stat_len(self.name, 12)            #for stat purpose
        self.stat_maxhp = stat_len(self.maxhp, 3)       #for stat purpose
        self.stat_hp = stat_len(self.hp, 3, 1)          #for stat purpose
        self.atkmin = stat_len(self.atk - self.atk_var, 2, 1)       #for stat purpose
        self.atkmax = stat_len(self.atk + self.atk_var, 2)      #for stat purpose
        self.stat_defence = stat_len(self.defence, 3, 1)    #for stat purpose



class Item:
    ID = 100
    def __init__ (self, name, cost, fnc_name, fnc, x, w=0):
        #fnc is a function, that said item will do. These functions have to be defined.
        self.name = name
        self.stat_name = stat_len(name, 20) #for stat purpose
        self.ID = Item.ID   #for sorting
        Item.ID += 1

        self.cost = cost
        
        self.fnc_name = stat_len(fnc_name, 8)   #for stat purpose
        self.fnc = fnc
        self.x = x
        self.w = w
    def use_item (self):
        global held_items
        t_comm, o = self.fnc(self.x, self.w)    #using function assigned to itself
        try:
            if t_comm == None:                   #if item was actually used
                return(x.name + ' used ' + self.name + ' on ' + o.name)
                held_items.pop(l)   #deleting self from list
        except:
            return t_comm
    def buy_item (self):
        global gold          #accesing held gold outside of function
        p = 'Are you sure you want to buy: ' + self.name + '? (type "yes" to confirm) '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:        #checking if enough gold is held
                gold -= self.cost
                held_items.append(self)    #adding itself to held items
                
                print('You bought' + self.name)
                print('You currently have' + str(gold) + 'gold')
                
                p = 'You are currently holding '
                held_items.sort(key = sortid)        #sorting held items
                for x in held_items:
                    p = p + x.name + ', '           #and displaying all of them
                print(p)
            else:
                print('You do not have enough gold')
    def sell_item(self, sell_red):     #red == value reduction
        global gold, held_items
        p = 'Are you sure you want to sell: ' + self.name + '? (type yes to confirm) '
        a = input(p)
        if a == 'yes':
            g_gained = int(self.cost - self.cost * sell_red / 100)
            gold += g_gained
            held_items.pop(o)
            print('You sold ' + self.name + ' and gained ' + str(g_gained) + ' gold')

print('Functions defined')


#------------------------------settings----------------------------
typecheck = 1
enemAI = 1
settings = {
    '1': typecheck,     #for damage type calculation
    '2': enemAI       #for enemy AI
    }

savename = 'savefilev2.txt'

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

held_items = [potionv2, potion, weak_potion]
# held_items = [potionv2, atk_potion, weak_potion, revivalfull_potion, revival_potion]                      #defining held items
held_items.sort(key = sortid)

buff_items = [atk_potion, atk_potionv2]
debuff_items = [weak_potion, weak_potionv2]
healing_items = [potionv2, potion, potionv3, revival_potion, revivalv2_potion, revivalfull_potion]        #defining list of healing items
# healing_items.sort(key = sortid)


global_items = {                                            #using dictionary for easier manipulation
    'Healing items': healing_items,
    'Buff items': buff_items,
    'Debuff items': debuff_items
    }
for x in global_items.values():
    x.sort(key=sortid)

gold = 100

#--------------------------Characters-------------------------------
Hero = Char('Hero', 70, 10, 1, 100, defence=1)        #(name maxhp atk atk_var recruitment_cost=0 g_drop=0 exp_drop=0
Champion = Char('Champion', 90, 9, 2, 100)            #  defence=0 defence_type='none' weapon=basic armor='basic')
Assasin = Char('Assasin', 55, 11, 4, 100)
test_boi_1 = Char('_test_boi_', 1, 1, 0)
test_boi_2 = Char('_test_boi_', 1, 1, 0)

global_allies = [Hero, Champion, Assasin, test_boi_1, test_boi_2]
global_allies_baseline = []                         #used in loading from file
for x in global_allies:
    global_allies_baseline.append(deepcopy(x))

# monster = Char('Monster', 120, 8, 0, 50, armor=light)   #old char used in first battles /unused
# demon = Char('Demon', 40, 12, 4, 50, armor=light)  #second old char /unused

#(name maxhp atk atk_var recruitment_cost=0 g_drop=0 exp_drop=0
#  defence=0 defence_type='none' weapon=basic armor='basic')

#----imps----
imp_1 = Char('Lesser Imp',  40, 4, 2, 0, 20, 10, 0, 'Subdemon', imp_bas_wep, imp_bas_arm)
imp_2 = Char('Imp Servant', 40, 4, 2, 0, 30, 20, 0, 'Subdemon', imp_lig_wep, imp_lig_arm, AI=AI_servant)
imp_3 = Char('Imp',         60, 7, 1, 0, 50, 35, 0, 'Subdemon', imp_lig_wep, imp_lig_arm, AI=AI_weakfirst)
imp_4 = Char('Imp Soldier', 60, 7, 1, 0, 60, 45, 0, 'Subdemon', imp_med_wep, imp_med_arm, AI=AI_servant)
imp_5 = Char('Higher Imp',  120, 10, 0, 0, 100, 65, 0, 'Demon', imp_lig_wep, imp_med_arm, AI=AI_onetarg)
imp_6 = Char('Imp General', 120, 10, 0, 0, 150, 80, 0, 'Demon', imp_med_wep, imp_goo_arm, AI=AI_command)
imp_7 = Char('Imp Outcast', 120, 10, 0, 0, 220, 120, 0, 'Demon', imp_goo_wep, imp_vgo_arm, AI=AI_strongfirst)

#----demons----
demon_1 = Char('demon_1', 100, 7, 2, 0, 180, 100, 0, 'Demon', dem_bas_wep, dem_bas_arm)
demon_2 = Char('demon_2', 100, 7, 2, 0, 0, 0, 0, 'Demon', dem_lig_wep, dem_lig_arm)
demon_3 = Char('demon_3', 150, 11, 1, 0, 0, 0, 1, 'Demon', dem_lig_wep, dem_lig_arm)
demon_4 = Char('demon_4', 150, 11, 1, 0, 0, 0, 1, 'Demon', dem_med_wep, dem_med_arm)
demon_5 = Char('demon_5', 270, 16, 2, 0, 0, 0, 1, 'High Demon', dem_lig_wep, dem_med_arm)
demon_6 = Char('demon_6', 270, 16, 2, 0, 0, 0, 1, 'High Demon', dem_med_wep, dem_goo_arm)
demon_7 = Char('demon_7', 270, 16, 2, 0, 0, 0, 1, 'High Demon', dem_goo_wep, dem_vgo_arm)

global_enemies = [imp_1,imp_2,imp_3,imp_4,imp_5,imp_6,imp_7,demon_1,demon_2,demon_3,demon_4,demon_5,demon_6,demon_7]

#-----------------------------Character-copies--------------------------------
imp_1b = deepcopy(imp_1)      #copying class instance
imp_2b = deepcopy(imp_2)
imp_3b = deepcopy(imp_3)
imp_4b = deepcopy(imp_4)
imp_4c = deepcopy(imp_4)
imp_5b = deepcopy(imp_5)
imp_5c = deepcopy(imp_5)
imp_6b = deepcopy(imp_6)

#---------------------------fighting-groups--------------------------------
allies = [Hero, Champion]
# allies = [Hero, Champion, test_boi_1, test_boi_2]

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
enem_11 = []
for x in global_enemies:      #im too lazy to write it on its own
    enem_11.append(x)

all_enem_fight = [enem_1, enem_2, enem_3, enem_4, enem_5, enem_6, enem_7, enem_8, enem_9, enem_10, enem_11]

team_1 = allies     #needs to be defined for info display(check items/characters, option 4 in main while)
# team_1 = enem_11

for x in allies:    #loop for removing allies already it team from 'recruit' roster
    if x in global_allies:
        global_allies.remove(x)

print("Instances defined")

while True:
    allies = team_1     #making sure these 2 values are the same
    print()
    print('What do you want to do?')
    print(' 1. Fight a monster')
    print(' 2. Go to shop')
    print(' 3. Go to tavern')
    print(' 4. Check items/characters')
    print(' 5. Menu')
    a = input("Choose: ")
    
    try:              #error checking
        a = int(a)
    except:
        print('Wrong input')
        print()
    else:
        if a < 1 or a > 5:
            print('Choice out of range')
            print()
            continue

    if a == 1:
        print()
        print('Available fights:')
        y = -1
        for x in all_enem_fight:
            y += 1
            v = stat_len(y, 2, 1) + '. enemies: '
            for z in x:
                v += z.stat_name + ' ,'
            print(v)
            
        o = input('Choose one that you wish to participate(type "ex" to quit): ')
        
        try:
            o = int(o)
        except:
            if o == 'ex':
                continue
            else:
                print('Wrong input')
                continue
        else:
            if o < 0 or o > y:
                print('Choice out of range')
                continue
        
        fight(team_1, all_enem_fight[o])
                 
    elif a == 2:
        shop(global_items, global_weapons, global_armor, 10)
        
    elif a == 3:
        while True:
            print()
            print('Welcome to the tavern')
            print('What do you seek here?')
            print(' 1. Recruit aventurers to your team')
            print(' 2. Go to the quest counter')
            print(' 3. Exit tavern')
            
            a = input('Choose: ')
            try:
                a = int(a)
            except:
                print('Wrong input')
                continue
            else:
                if a < 0 or a > 3:
                    print('Choice out of range')
                    continue
            
            if a == 1:
                while True:
                    print()
                    if global_allies:
                        y = -1
                        if len(global_allies) > 1:
                            print('Currently awaiting or recruitment are:')
                            for char in global_allies:
                                y += 1
                                print(' ' + str(y) + '. ' + char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' recruit cost: ' + str(char.recr_cost))
                        else:
                            print('Currently awaiting recruitment is:')
                            y += 1
                            char = global_allies[0]
                            print(' ' + str(y) + '. ' + char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' recruit cost: ' + str(char.recr_cost))
                        
                        o = input('Choose one to recruit(type "ex" to exit) ')
                        
                        try:
                            o = int(o)
                        except:
                            if o == 'ex':
                                break
                            else:
                                print('Wrong input')
                                continue
                        else:
                            if o < 0 or o > y:
                                print ('Choice out of range')
                                continue
                            
                        global_allies[o].recruit()
                    else:
                        print('There is no one to recruit at this tavern')
                        pause()
                        break
                
            if a == 2:
                print('Quest counter does not exist(yet)')
            if a == 3:
                pause()
                break
                
    elif a == 4:
        while True:
            print()
            print('What do you want to do?')
            print(' 1. Display information')
            print(' 2. Equip weapons')
            print(' 3. Unequip weapons')
            print(' 4. Equip armor')
            print(' 5. Unequip armor')
            print(' 6. Exit')
            
            a = input('Choose: ')
            
            try:
                a = int(a)
            except:
                print('Wrong input')
                continue
            else:
                if a < 0 or a > 6:
                    print('Choice out of range')
                    continue
            
            if a == 1:
                while True:
                    print()
                    print('Display information about')
                    print(' 1. statistics about team')
                    print(' 2. level and experience of team')
                    print(' 3. items')
                    print(' 4. equipment')
                    print(' 5. exit')
                    
                    a = input('Choose: ')
                    
                    try:
                        a = int(a)
                    except:
                        print('Wrong input')
                        continue
                    else:
                        if a < 0 or a > 5:
                            print('Choice out of range')
                            continue
                    if a == 1:
                        print()
                        print('Your current team consists of:')
                        stat_print(3)                     #printing extended stats
                        pause()
                        
                    elif a == 2:
                        for char in team_1:
                            print(char.stat_name + ': level: ' + stat_len(char.level, 2, 1) + ' experience points: ' + stat_len(char.exp, 6,1) + ' required exp points: ' + stat_len(200*char.level, 6, 1))
                        pause()
                            
                    elif a == 3:
                        print()
                        print('Currently held items: ')
                        if held_items:                             #printing extended items
                            for x in held_items:
                                print(' ' + x.stat_name + ': function:' + x.fnc_name + ' for:' + str(x.x))
                        elif not held_items:
                            print("You don't hold any items in your inventory")
                        pause()
                            
                    elif a == 4:
                        print()
                        if held_weapons:
                            print('Currently held weapons:')
                            for x in held_weapons:              #printing weapon stats
                                print(' ' + x.stat_name + ': damage:' + x.stat_dmg + '(' + str(x.dmg_var) + ') ' + x.dmg_type_1 + ' ' + x.dmg_type_2)
                        elif not held_weapons:
                            print('No weapons are being held in inventory')
                            
                        print()
                        if held_armor:
                            print('Currently held armor:')
                            for x in held_armor:
                                print(' ' + x.stat_name + ': defence:' + x.stat_defence + ' defence type:' + x.defence_type)
                        elif not held_armor:
                            print('No armor is being held in inventory')
                        pause()
                        
                    elif a == 5:
                        break

            elif a == 2 or a == 4:
                while True:
                    print()
                    if a == 2:
                        if held_weapons:         #if you hav any weapon in eq
                            y = -1
                            print('Currently held weapons:')
                            for x in held_weapons:                 #printing weapons with stats
                                y += 1
                                print(' ' + str(y) + '. ' + x.stat_name + ': damage:' + x.stat_dmg + '(' + str(x.dmg_var) + ') ' + x.dmg_type_1 + ' ' + x.dmg_type_2)
                            o = input('Choose weapon to equip(type "ex" to exit) ')
                            
                        else:
                            print("You don't hold any weapons in inventory")
                            break
                    else:
                        if held_armor:
                            y = -1
                            print('Currently held armor:')
                            for x in held_armor:
                                y += 1
                                print(' ' + str(y) + '. ' + x.stat_name + ': defence' + x.stat_defence + ' defence type:' + x.defence_type)
                            o = input('Choose armor to equip(type "ex" to exit) ')
                            
                        else:
                            print("Youd don't any armor in inventory")
                            break
                        
                    try:
                        o = int(o)
                    except:
                        if o == 'ex':
                            print()
                            break
                        else:
                            print('Wrong input')
                            continue
                    else:
                        if o < 0 or o > y:
                            print('Choice out of range')
                            
                    y = -1
                    for x in team_1:                         #printing char with info about weapon
                        if x == False:
                            continue
                        y += 1
                        if a == 2:
                            if x.weapon.ID == basic.ID:
                                print(' ' + str(y) + '. ' + x.stat_name + ' current weapon: ' + x.weapon.stat_name)
                            else:
                                print(' ' + str(y) + '. ' + x.stat_name + ' current weapon: ' + x.weapon.stat_name + ' damage:' + x.weapon.stat_dmg + '(' + str(x.weapon.dmg_var) + ')')
                        else:
                            if x.armor.ID == basal.ID:
                                print(' ' + str(y) + '. ' + x.stat_name + ' current armor: ' + x.armor.stat_name)
                            else:
                                print(' ' + str(y) + '. ' + x.stat_name + ' current armor: ' + x.armor.stat_name + ' defence:' + x.armor.stat_defence + ' defence type:' + x.armor.defence_type)
                    if a == 2:
                        l = input('Choose character that will wield this weapon(type "ex" to exit) ')
                    else:
                        l = input('Choose character that will wear this armor(type "ex" to exit) ')
                    
                    try:
                        l = int(l)
                    except:
                        if l == 'ex':
                            print()
                            break
                        else:
                            print('Wrong input')
                            continue
                    else:
                        if l < 0 or l > y:
                            print('Choice out of range')
                            continue
                            
                    
                    if a == 2 and team_1[l].weapon.ID != basic.ID:                         #if char already has a weapon
                        print(team_1[l].name + ' already has a ' + team_1[l].weapon.name + ' equipped')
                        x = input('Do you want to unequip ' + team_1[l].weapon.name + ' and equip ' + held_weapons[o].name + '? (yes to confirm) ')
                        if x != 'yes':         #only yes will allow  to equip a weapon
                            continue
                    elif a == 4 and team_1[l].armor.ID != basal.ID:
                        print(team_1[l].name + ' already wears ' + team_1[l].armor.name + ' armor')
                        x = input('Do you want to unequip ' + team_1[l].armor.name + ' armor and equip ' + held_armor[o].name + ' armor? (yes to confirm) ')
                        if x != 'yes':
                            continue
                    if a == 2:
                        v = team_1[l].weapon                                 #settin placeholder for weapon
                        team_1[l].unequip_weapon()                  #unequipping weapon old
                        
                        held_weapons[o].equip(team_1[l])            #equipping new weapon
                        print(team_1[l].name + ' now wields ' + held_weapons[o].name)     #comment
                        
                        held_weapons.pop(o)            #deleting new weapon from held weapons
                        if v.ID != basic.ID:             #if old weapon existed(wasnt basic)
                            held_weapons.append(v)                    #add old weapon to held weapons
                        held_weapons.sort(key = sortid)
                    else:
                        v = team_1[l].armor             #setting placeholder for armor
                        team_1[l].unequip_armor()           #unequipping old armor
                        
                        held_armor[o].equip(team_1[l])      #equipping new one
                        print(team_1[l].name + ' now wears ' + held_armor[o].name)  #comment
                        
                        held_armor.pop(o)           #deleting new one from held armor
                        if v.ID != basal.ID:          #if old weapon wasn't basal(was normal armor)
                            held_armor.append(v)            #add old one to held armor
                        held_armor.sort(key = sortid)       #sort

                
            elif a == 3 or a == 5:
                while True:
                    print()
                    y = -1
                    v = []
                    for x in team_1:
                        if x == False:
                            continue
                        if a == 3 and x.weapon.ID == basic.ID:       #if holds basic weapon then doesnt count
                            continue
                        elif a == 5 and x.armor.ID == basal.ID:
                            continue
                        v.append(x)
                        y += 1
                        if y == 0:
                            if a == 3:
                                print('Characters currently wielding a weapon:')
                            if a == 5:
                                print('Characters with their armor equipped:')
                        if a == 3:
                            print(str(y) + '. ' + x.stat_name + ': ' + x.weapon.stat_name + ' damage:' + x.weapon.stat_dmg + '(' + str(x.weapon.dmg_var) + ')')
                        if a == 5:
                            print(str(y) + '. ' + x.stat_name + ': ' + x.armor.stat_name + ' defence:' + x.armor.stat_defence)
                    if y == -1:
                        if a == 3:
                            print('None of your characters hold a weapon')
                            break
                        if a == 5:
                            print('None of your characters is armored')
                            break
                    if a == 3:
                        print('Choose one that will unequip his weapon')                    
                    if a == 5:
                        print('Choose one that will take off his armor')
                        
                    o = input('Choose(type "ex" to quit): ')
                    try:
                        o = int(o)
                    except:
                        if o == 'ex':
                            break
                        else:
                            print('Wrong input')
                            continue
                    else:
                        if o < 0 or o > y:
                            print('Choice out of range')
                            continue
                    if a == 3:
                        held_weapons.append(v[o].weapon)       #adding old weapon to eq
                        held_weapons.sort(key = sortid)      #sorting
                        v[o].unequip_weapon()               #unequipping weapon
                    elif a == 5:
                        held_armor.append(v[o].armor)
                        held_armor.sort(key = sortid)
                        v[o].unequip_armor()

            elif a == 6:
                print()
                break
    elif a == 5:
        while True:
            print()
            print('Menu')
            print(' 1. Show help')
            print(' 2. Settings')
            print(' 3. Save gamestate')
            print(' 4. Load gamestate')
            print(' 5. Exit')
            
            
            a = input('Choose: ')
            
            try:
                a = int(a)
            except:
                print('Wrong input')
                continue
            else:
                if a < 0 or a > 5:
                    print('Choice out of range')
                    continue
            
            if a == 1:
                while True:
                    print()
                    print('Available mechanic explainations:')
                    print(' 1. Damage type modifiers')
                    print(' 2. Experience system')
                    print(' 3. Battle system')
                    
                    o = input('Choose(type "ex" to exit): ')
                    
                    try:
                        o = int(o)
                    except:
                        if o == 'ex':
                            break
                        print('Wrong input')
                        continue
                    else:
                        if o < 0 or o > 3:
                            print('Choice out of range')
                            continue
                    #Width of help is 80 characters
                    #Length is 23 + 1(reserved for the pause)
                    if o == 1:
                        print('----------------------------Damage type modifier help---------------------------')
                        print('As of writing this help, only working damage types are blunt, slash, pierce')
                        print('and none.')
                        print()
                        print('Blunt and slash type damage modifiers are dependent on character damage and')
                        print('opponent defence.')
                        print('Pierce and slash damage type modifiers are independent from opponent defence')
                        print('value.')
                        print()
                        print('Blunt works better(than none type) versus enemies with medium to high armor')
                        print('value.')
                        print('Slash on the other hand excels at defeating enemies with light to no armor.')
                        print('Pierce applies low damage modifier that is unaffected by defence of the opponent')
                        print('None does not apply any damage modifier.')
                        print()
                        print('Damage modifiers for blunt and piercecan not be bigger that oponents defence.')
                        print('these will be forcefully lowered. Slash is unaffected by this.')
                        print()
                        print()
                        print()
                        print()
                        print('///written in 0.1.005///')
                        pause()
                        
                    if o == 2:
                        #width 80
                        #lenght 23 + 1
                        print('--------------------------------Experience system-------------------------------')
                        print('At the end o feach succesful battle player will receive certain amount of')
                        print('experience. How much is determined either by enemies in enemy team or')
                        print('set manually.')
                        print()
                        print('Then experience is divided by number of characters, tha player fought with and')
                        print('distributed evenly between them.')
                        print()
                        print('Once enough experience points are gained, character will gain a new level.')
                        print('Levels increase statistics (health and attack) but also decrease experience gain')
                        print('a bit and increase experience required to gain another level.')
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print('///written in 0.1.005///')
                        pause()
                    
                    if o == 3:
                        #width 80
                        #length 23+1
                        print('---------------------------------Battle system----------------------------------')
                        print('Battle is divided by turns in which each character from both teams acts once.')
                        print('Enemy actions are set by functions.')
                        print()
                        print('Actions are divided on attacking, using item and fleeing.')
                        print('Damage dealt is calculated by damage and damage variable of attacker and is')
                        print('then reduced by defenders defence.')
                        print()
                        print('Items usage and effect depend on type of item. One can heal, other apply buffs.')
                        print()
                        print('Fleeing does nothing more than quitting current fight.')
                        print()
                        print('Battle is ended by either fleeing or when health points of all characters in a')
                        print('team are reducedd to zero.')
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print('///written in 0.1.005///')
                        pause()
                        
                
                
            if a == 2:
                while True:
                    y = 0
                    print()
                    print('Available options(1 means enabled, 0 means disabled):')
                    print(' 1. Damage type modifiers: ' + str(settings['1']))
                    print(' 2. Better enemy AI: ' + str(settings['2']))
                        
                    o = input('Choose(type "ex" to exit): ')
                    try:
                        o = int(o)
                    except:
                        if o == 'ex':
                            break
                        print('Wrong input')
                        continue
                    else:
                        if o < 0 or o > len(settings):
                            print('Choice out of range')
                            continue
                        o = str(o)
                        
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
                    for char in team_1:
                        exp_sav = stat_len(char.total_exp, 8, 1)
                        exp_save = ''
                        for x in exp_sav:
                            if x == ' ':
                                x = '0'
                            exp_save += x
                        save.write('char')
                        save.write('0' + str(char.ID))
                        save.write(str(char.weapon.ID))
                        save.write(str(char.armor.ID))
                        save.write(exp_save[:-4])   #splitting total exp into two sets
                        save.write(exp_save[4:])
                        save.write('---\n')
                    for item in held_items:
                        save.write('item')
                        save.write('0' + str(item.ID))
                        save.write('---\n')
                    for weap in held_weapons:
                        save.write('weap')
                        save.write(str(weap.ID))
                        save.write('---\n')
                    for armo in held_armor:
                        save.write('armo')
                        save.write(str(armo.ID))
                        save.write('---\n')
                    save.write('gold')
                    t_gold_t = stat_len(gold, 4, 1)
                    t_gold = ''
                    for x in t_gold_t:
                        if x == ' ':
                            v = '0'
                        else:
                            v = x
                        t_gold += v
                    save.write(str(t_gold))
                    save.write('---\n')
                    
#for me in future:
#save writes header that corresponds to data and then said data
#data is always read with 4 bytes(letters)
#they can be written in any order, since loading operates on headers to write data
#characters are taken for baseline(deepcopied characters), assigned to temporary teams and given statistics/items
#weapons, amor, items are taen from global lists and assigned to temporary lists
#gold is plainly assigned to gold(current)
#after data has been read, '---\n' is used to mark end of data
                    
            if a == 4:
                try:
                    with open(savename, 'r') as save:
                        temp_team = []
                        temp_weap = []
                        temp_item = []
                        temp_armo = []
                        temp_exp = ''
                        exp_time = 0
                        line = ' '
                        count = -1
                        while line != '':
                            line = save.read(4)
                            
                            if line == 'char':
                                count += 1
                                while line != '---\n':
                                    line = save.read(4)
                                    
                                    try:
                                        line = int(line)
                                    except:
                                        True
                                    else:
                                        for x in global_allies_baseline:
                                            if x.ID == line:
                                                temp_team.append(x)
        #                                         print('yes char')
                                        for x in global_weapons:
                                            if x.ID == line:
                                                x.equip(temp_team[count])
        #                                         print('yes weapon')
                                        for x in global_armor:
                                            if x.ID == line:
                                                x.equip(temp_team[count])
        #                                         print('yes armor')
                                                exp_time = 1      #exp_time allows to load exp and execute level up
                                        if exp_time == 1:          #experience should always be read last
                                            temp_exp += str(line)
                                            if len(temp_exp) == 8:
                                                x.total_exp = int(temp_exp)
                                                x.exp = int(temp_exp)
                                                x.level_up_check(1)
                                        
                            elif line == 'weap':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        True
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
                                        True
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
                                        True
                                    else:
                                        for x in global_armor:
                                            if x.ID == line:
                                                temp_armo.append(x)
                                                
                            elif line == 'gold':
                                while line != '---\n':
                                    line = save.read(4)
                                    try:
                                        line = int(line)
                                    except:
                                        break
                                    else:
                                        gold = line
                                    
                        team_1 = temp_team
                        held_weapons = temp_weap
                        held_items = temp_item
                        held_armor = temp_armo
    #                     for x in team_1:
    #                         print(x.name + ' atk:' + str(x.atk) + ' atk_var:' + str(x.atk_var))
                    print('Save loaded correctly')
                except:
                    print()
                    print('File ' + savename + ' used as save does not exist')
                        
            if a == 5:
                break
            
