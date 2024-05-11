from random import randint
from copy import deepcopy

#z is for while loops(error protection)
#o is for returns/data to be used outside of function AND targeting AND choices
#l is secondary/placeholder for choices
#p is secondary for targeting  AND better looking inventory prints(see item.buy_item) AND better looking class t_comm
#x and y are for 'for' loops
#y is for counter in for loop
#v is for empty input(not in pause func) AND a placeholder
#c is for choosing which option of function run
#a is for choosing what to do(in wide/main function)
#d is for choosing in dictionaries(see shope>buy items)
#p is for better looking inventory prints(see item.buy_item)

#function zone

#function zone

def pause():
    emptyinput = input("Press anything to continue")

def sortid(y):
    return y.ID

def stat_len(x, y, c=0):      #x is value to be lengthened, y is length, c is option choosing
    if c == 0:   #add to the end
        x = str(x)
        while len(x) < y:
            x += ' '
        return x
    if c == 1:     #add to the beginning
        x = str(x)
        while len(x) < y:
            x = ' ' + x
        return x
        

def stat(char, c=0):
    if c == 0:
        print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence)
    elif c == 1:
        x = ''
        if char.weapon == basic and char.armor == basal:
            x = stat_len(x, 18, 1)
            print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' armor:' + char.armor.stat_name + x + ' weapon:' + char.weapon.stat_name)
        elif char.weapon != basic and char.armor == basal:
            x = stat_len(x, 18, 1)
            print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' armor:' + char.armor.stat_name + x + ' weapon:' + char.weapon.stat_name + ' dmg:' + str(char.weapon.dmg) + ' var:' + str(char.weapon.dmg_var))
        elif char.weapon == basic and char.armor != basal:
            print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' armor:' + char.armor.stat_name + ' armor defence:' + char.armor.stat_defence + ' weapon:' + char.weapon.stat_name)
        else:
            print(char.stat_name + '- health:' + char.stat_hp + '/' + char.stat_maxhp + ' attack:' + char.atkmin + '-' + char.atkmax + ' total defence:' + char.stat_defence + ' armor:' + char.armor.stat_name + ' armor defence:' + char.armor.stat_defence + ' weapon:' + char.weapon.stat_name + ' dmg:' + str(char.weapon.dmg) + ' var:' + str(char.weapon.dmg_var))


def EoT_summ():                                      #End of Turn summary
    print()
    for x in all_fghtr:
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

def team_target(c):
    global o
    z = 0
    if c==1:
        while z == 0:
            o = 0
            for y in team_1:                                       #printing team_1 members with indexes
                if y==False:
                    continue
                if y.hp <= 0:
                    o += 1
                    continue
                print(str(o) + '. ' + y.stat_name + ' ' + y.stat_hp + '/' + y.stat_maxhp)
                o += 1
            l = o
            o = input('Choose: ')
            
            try:
                o = int(o)
            except:
                print('Wrong input')
                print()
                continue
            else:
                l -= 1
                if o < 0 or o > l:
                    print('Choice out of range')
                    print()
                    continue
                else:
                    z = 1
                    
    if c==2:
        while z == 0:
            o = 0
            for y in team_2:
                if y==False:
                    continue
                if y.hp <= 0:
                    o += 1
                    continue
                print(str(o) + '. ' + y.stat_name + ' ' + y.stat_hp + '/' + y.stat_maxhp)
                o += 1
            l = o
            o = input('Choose: ')
            
            try:
                o = int(o)
            except:
                print('Wrong input')
                print()
                continue
            else:
                l -= 1
                if o < 0 or o > l:
                    print("Choice out of range")
                    print()
                    continue
                else:
                    z = 1

def fight_end(c, y=0):            #c is just to choose which side won, y is for gold obtained input
    if c == 1:
        if y == 0:
            v = 0
            for x in team_2:
                if x == False:
                    continue
                v += x.g_drop
            stat_print()
            print('You won the fight')
            print('You gained', v, 'gold')
            global gold
            gold += v
        elif y != 0:
            stat_print()
            print('You won the fight')
            print('You gained', y, 'gold')
            gold += y
    if c == 2:
        stat_print()
        print('You lost the fight')
        print('What a shame...')
        print()
        
def fight_end_check(v=0):
    x = 0
    for y in team_1:
        if y == False:
            continue
        x += y.hp
    if x <= 0:
        EoT_summ()
        fight_end(2)
        return 'end'
    
    x = 0
    for y in team_2:
        if y == False:
            continue
        x += y.hp
    if x <= 0:
        EoT_summ()
        fight_end(1, v)
        return 'end'

def fight(ally, enem):
    global team_1, team_2, o, p, all_fghtr, turn
    team_1 = ally
    team_2 = enem
    all_fghtr = team_1 + team_2
    turn = 0
    
    for x in all_fghtr:                    #heal for next battle
        if x == False:
            continue
        x.heal_up()

    for x in team_1:
        x.team = 'allies'
    for x in team_2:
        x.team = 'monsters'
    global held_items
    
    z = 0
    print()
    while z == 0:
        turn += 1
        for x in all_fghtr:
            print()
            while True:
                if x == False:
                    break
                if x.hp <= 0:
                    break
                if x.team == 'allies':
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
                        dmg = x.deal_dmg()
                        team_2[o].take_dmg(dmg)
                        e = fight_end_check()
                        break
                    elif a == 2:
                        print('Available items:')
                        y = -1
                        for x in held_items:
                            y += 1
                            print(str(y) + '. ' + x.stat_name + ' ' + x.fnc_name + ' ' + str(x.x))
                        
                        o = input('Choose (type "ex" to quit):')
                            
                        try:                             #error checking
                            o = int(o)
                        except:
                            if o == 'ex':
                                z = 1
                                continue
                            else:
                                print('Wrong input')
                                print()
                                continue
                        else:
                            if o < 0 or o > y:
                                print('Choice out of range')
                                print()
                                continue
                        held_items[o].use_item()
                        break
                    elif a == 3:
                        print('You fleed from battle')
                        print()
                        z = 1
                        pause()
                        break
                elif x.team == 'monsters':
                    o = randint(0,len(team_1)-1)                                                  #enemy choosing random target
                    while team_1[o] == False or team_1[o].hp <= 0:
                        o = random.randint(0,len(team_1)-1)                                 #enemy choosing random target again if chose empty fighter place or fighter dead
                    p = team_1[o]
                    dmg = x.deal_dmg()
                    team_1[o].take_dmg(dmg)
                    e = fight_end_check()
                    break
            if e == 'end':
                z = 1
                break
        if z == 1:
            break
        EoT_summ()
        stat_print()

#item function
def heal(x):                ####### works only for team_1
    print("Who do you want to heal? ")
    team_target(1)
    
    a = team_1[o].hp                                      #for print measures
    team_1[o].hp += x
    
    if team_1[o].hp > team_1[o].maxhp:                     #prevent overheal
        team_1[o].hp = team_1[o].maxhp
    team_1[o].stat_hp = stat_len(team_1[o].hp, 3, 1)
    
    b = team_1[o].hp                                      #for print measures
    print(team_1[o].name + ' has been healed for', b-a, 'health up to current', team_1[o].hp, 'health points')


class Weapon:
    ID = 1000
    def __init__ (self, name, cost, dmg, dmg_var, dmg_type_1, dmg_type_2='none'):
        
        self.name = name
        self.stat_name = stat_len(name, 10)
        Weapon.ID += 1
        self.ID = Weapon.ID
        self.cost = cost
        self.dmg = dmg
        self.stat_dmg = stat_len(dmg, 2, 1)
        self.dmg_var = dmg_var
        self.dmg_type_1 = dmg_type_1
        self.dmg_type_2 = dmg_type_2
    def equip(self, char):
        char.weapon = self
        char.atk += self.dmg
        char.atk_var += self.dmg_var
        
        char.atkmin = char.atk - char.atk_var           #atkmin and atkmax are for status display
        char.atkmax = char.atk + char.atk_var
        char.atkmin = stat_len(char.atkmin, 2, 1)       # adding spaces for nicer comment(stat)
        char.atkmax = stat_len(char.atkmax, 2)
        
        char.dmg_type_1 = self.dmg_type_1
        char.dmg_type_2 = self.dmg_type_2
    def buy_equipment(self):
        global gold          #accesing held gold outside of function
        p = 'Are you sure you want to buy: ' + self.name + '? (type "yes" or "no") '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:        #checking if enough gold is held
                gold -= self.cost
                held_weapons.append(self)    #adding itself to held items
                
                print('You bought', self.name)
                print('You currently have', gold, 'gold')
                
                p = 'You are currently holding '
                held_weapons.sort(key = sortid)        #sorting held items
                for x in held_weapons:
                    p = p + x.name + ', '           #and displaying all of them
                print(p)
            else:
                print('You do not have enough gold')
        elif a == 'no':
            print()
        else:
            print('You discovered a secret, everything besides "yes" works to not buy')

class Armor:
    ID = 1500

    def __init__(self, name, cost, defence, defence_type='none'):
        self.name = name
        self.stat_name = stat_len(name, 10)
        Armor.ID += 1
        self.ID = Armor.ID
        self.cost = cost
        self.defence = defence
        self.stat_defence = stat_len(defence, 2, 1)
        self.defence_type = defence_type
    def equip(self, char):
        char.armor = self
        char.defence += self.defence
        if char.defence_type_1 =='none':
            char.defence_type_1 = self.defence_type
        else:
            char.defence_type_2 = self.defence_type
        char.stat_defence = stat_len(char.defence, 3, 1)
    def buy_equipment(self):
        global gold          #accesing held gold outside of function
        p = 'Are you sure you want to buy: ' + self.name + '? (type "yes" or "no") '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:        #checking if enough gold is held
                gold -= self.cost
                held_armor.append(self)    #adding itself to held armor
                
                print('You bought', self.name)
                print('You currently have', gold, 'gold')
                
                p = 'You are currently holding '
                held_armor.sort(key = sortid)        #sorting held armor
                for x in held_armor:
                    p = p + x.name + ', '           #and displaying all of them
                print(p)
            else:
                print('You do not have enough gold')
        elif a == 'no':
            print()
        else:
            print('You discovered a secret, everything besides "yes" works to not buy')

basic = Weapon('None', 0, 0, 0, 'blunt')        #(name, cost, dmg, dmg_var, dmg_type_1, dmg_type_2='None')
bat = Weapon('Bat', 50, 1, 1, 'blunt')
sword = Weapon('Sword', 120, 4, 0, 'slash')
hammer = Weapon('Hammer', 120, 3, 1, 'blunt')

imp_bas_wep = Weapon('None', 0, 0, 0, 'slash')
imp_lig_wep = Weapon('Light', 0, 1, 2, 'slash', 'fire')
imp_med_wep = Weapon('Medium', 0, 2, 3, 'blunt', 'fire')
imp_goo_wep = Weapon('Good', 0, 4, 0, 'pierce')

global_weapons = [bat, sword, hammer]
global_weapons.sort(key = sortid)

basal = Armor('None', 0, 0)  #name cost defence defence_type='none'
light = Armor('Light', 50, 2)
medial = Armor('Medial', 120, 4)
heavy = Armor('Heavy', 250, 6)

imp_bas_arm = Armor('None', 0, 0)
imp_lig_arm = Armor('Light', 0, 1)
imp_med_arm = Armor('Medium', 0, 3)
imp_goo_arm = Armor('Good', 0, 5)
imp_vgo_arm = Armor('Very good', 0, 8, 'shadow')

global_armor = [light, medial, heavy]
global_armor.sort(key = sortid)

global_equipment = {
    'Weapons': global_weapons,
    'Armor': global_armor
    }

held_weapons = [sword]
held_armor = [light]

class Char:
    def __init__ (self, name, maxhp, atk, atk_var, g_drop=0, defence=0, defence_type_1='none', weapon=basic, armor=basal):
        self.name = name
        self.stat_name = stat_len(name, 12)
        self.maxhp = maxhp
        self.hp = maxhp
        self.stat_maxhp = stat_len(self.maxhp, 3)
        self.stat_hp = stat_len(self.hp, 3, 1)
        
        self.atk = atk
        self.g_drop = g_drop                                                   #gold drop variable
        
        self.defence = defence                             #setting base for armor
        self.stat_defence = stat_len(self.defence, 3, 1)
        self.defence_type_1 = defence_type_1
        self.defence_type_2 = 'none'
        self.armor = armor
        armor.equip(self)
        
        self.atk_var = atk_var                                                 #attack variable
        self.atkmin = atk - atk_var
        self.atkmax = atk + atk_var
        self.atkmin = stat_len(self.atkmin, 2, 1)           #adding spaces for nice comment(stat)
        self.atkmax = stat_len(self.atkmax, 2)
        
#         self.dmg_type_1 = dmg_type_1                                     #damage type for future(?) elemental system
#         self.dmg_type_2 = dmg_type_2                #these are defined by weapon.equip() and char.unequip weapon()
        
        self.base_maxhp = maxhp
        self.base_atk = atk
        self.base_armor = armor
        self.base_atk_var = atk_var
        
        self.t_comm = self.name + ' did not have a chance to attack'          #turn comment
        self.weapon = weapon
        weapon.equip(self)
    def take_dmg (self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        self.stat_hp = stat_len(self.hp, 3, 1)
    def deal_dmg (self):
        atk_var = randint(0,self.atk_var*2) - self.atk_var             #making variable for damage
        atk_dmg = self.atk + atk_var - p.defence                                          #calculating damage from atk and variable
        if atk_dmg <= 0:
            atk_dmg = 0
            self.t_comm = (self.name + ' dealt no damage to ' + p.name)                     #turn comment used in EoT_summ
        else:
            self.t_comm = (self.name + ' dealt ' + str(atk_dmg) + ' damage to ' + p.name)                      #turn comment used in EoT_summ
        return atk_dmg
    def heal_up(self):
        self.hp = self.maxhp
        self.stat_hp = stat_len(self.hp, 3, 1)
    def unequip_weapon(self):
        self.atk -= self.weapon.dmg
        self.atk_var -= self.weapon.dmg_var
        
        self.atkmin = self.atk - self.atk_var
        self.atmax = self.atk + self.atk_var
        self.atkmin = stat_len(self.atkmin, 2, 1)           #adding spaces for nicer comment(stat)
        self.atkmax = stat_len(self.atkmax, 2)
        
        self.dmg_type_1 = 'blunt'
        self.dmg_type_2 = 'none'
        basic.equip(self)
    def unequip_armor(self):
        self.defence -= self.armor.defence
        self.stat_defence = stat_len(self.defence, 3, 1)
        if self.defence_type_2 != 'none':
            self.defence_type_2 = 'none'
        else:
            self.defence_type_1 = 'none'
        if self.armor != basal:
            held_armor.append(self.armor)
        basal.equip(self)
            

class Item:
    ID = 100
    def __init__ (self, name, cost, fnc_name, fnc, x):
        #fnc is a function, that said item will do. These functions have to be defined.
        self.name = name
        self.stat_name = stat_len(name, 10)
        Item.ID += 1
        self.ID = Item.ID
        self.cost = cost
        
        self.fnc_name = stat_len(fnc_name, 5)
        self.fnc = fnc
        self.x = x
    def use_item (self):
        self.fnc(self.x)
    def buy_item (self):
        global gold          #accesing held gold outside of function
        p = 'Are you sure you want to buy: ' + self.name + '? (type "yes" or "no") '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:        #checking if enough gold is held
                gold -= self.cost
                held_items.append(self)    #adding itself to held items
                
                print('You bought', self.name)
                print('You currently have', gold, 'gold')
                
                p = 'You are currently holding '
                held_items.sort(key = sortid)        #sorting held items
                for x in held_items:
                    p = p + x.name + ', '           #and displaying all of them
                print(p)
            else:
                print('You do not have enough gold')
        elif a == 'no':
            print()
        else:
            print('You discovered a secret, everything besides "yes" works to not buy')




print('Functions defined')

#weapons are defined with class

potion = Item('Potion', 12, 'heal', heal, 10)        #Item(name, ID, cost, fnc_name, fnc, x(fnc_attrib)) 
potionv1 = Item('Potion v1', 23, 'heal', heal, 20)
potionv2 = Item('Potion v2', 45, 'heal', heal, 30)

held_items = [potionv1]                      #defining held items
healing_items = [potionv1, potion, potionv2]        #defining list of healing items
healing_items.sort(key = sortid)

global_items = {                                            #using dictionary for easier manipulation
    'Healing items': healing_items
    }

gold = 100

Hero = Char('Hero', 70, 10, 1)        #name maxhp atk atk_var g_drop=0 defence=0 defence_type='none' weapon=basic armor='basic'
Champion = Char('Champion', 90, 9, 2)

monster = Char('Monster', 120, 8, 0, 50, armor=light)
demon = Char('Demon', 40, 12, 4, 50, armor=light)

imp_1 = Char('Lesser Imp', 40, 4, 2, 30, 0, 'Subdemon', imp_bas_wep, imp_bas_arm)
imp_2 = Char('Imp Servant', 40, 4, 2, 40, 0, 'Subdemon', imp_lig_wep, imp_lig_arm)
imp_3 = Char('Imp', 60, 7, 1, 50, 0, 'Subdemon', imp_lig_wep, imp_lig_arm)
imp_4 = Char('Imp Soldier', 60, 7, 1, 60, 0, 'Subdemon', imp_med_wep, imp_med_arm)
imp_5 = Char('Higher Imp', 120, 10, 0, 100, 0, 'Demon', imp_lig_wep, imp_med_arm)
imp_6 = Char('Imp General', 120, 10, 0, 150, 0, 'Demon', imp_med_wep, imp_goo_arm)
imp_7 = Char('Imp Outcast', 120, 10, 0, 220, 0, 'Demon', imp_goo_wep, imp_vgo_arm)

# team_1 = [imp_1,imp_2,imp_3,imp_4,imp_5,imp_6,imp_7]
# team_1 = [Hero, Champion]                                                  #defining team 1
# team_2 = [imp_7]                                                  #defining team 2
# all_fghtr = team_1 + team_2
    #defining battle teams
imp_1b = deepcopy(imp_1)      #copying class instance
allies = [Hero, Champion]
enem_1 = [imp_1]      #remember to define more of the same char type as different entities

print("defined")

while True:
    

    
    print("What do you want to do?")
    print("1.Fight a monster 2.Go to shop 3. Check items/character")
    a = input("Choose: ")
    
    try:              #error checking
        a = int(a)
    except:
        print('Wrong input')
        print()
    else:
        if a < 1 or a > 3:
            print('Choice out of range')
            print()
            continue

# def fight(team_1, team_2)
    

    if a == 1:
        fight(allies, enem_1)
                 
    elif a == 2:
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
            
            a = input('Choose:')
            
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
                    y = 0
                    d = []
                    for x in global_items:
                        print(y, '.', x)
                        y += 1
                        d.append(x)
                    o = input('Choose (type "ex" to quit):')
                    
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
                        y -= 1
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
                    v = global_items[d[l]]
                    for x in v:
                        y += 1
                        print(y, '. ', x.stat_name, 'function:' + x.fnc_name, 'cost:' + str(x.cost))
                    o = input('Choose (type "ex" to quit):')
                    
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
                print('Not available(no one wants to buy a thing')
                print()
            
            elif a == 3:
                while True:
                    print('Equipment for sale:')
                    y = -1
                    d = []
                    for x in global_equipment:
                        y += 1
                        print(str(y) + '. ' + x)
                        d.append(x)
                    o = input('Choose (type "ex" to quit):')
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
                v = global_equipment[d[l]]
                while z == 0:
                    if v == global_weapons:
                        y = -1
                        for x in v:
                            y += 1
                            print(str(y) + '. ' + x.stat_name + ': cost:' + str(x.cost) + ' damage:' + x.stat_dmg + ' variable:' + str(x.dmg_var))

                    elif v == global_armor:
                        y = -1
                        for x in v:
                            y += 1
                            print(str(y) + '. ' + x.stat_name + ': cost:' + str(x.cost) + ' defence:' + x.stat_defence)
                    
                    o = input('Choose(type "ex" to exit):')
                    try:
                        o = int(o)
                    except:
                        if o == 'ex':
                            break
                        else:
                            print('Wrong inpuy')
                            continue
                    else:
                        if o < 0 or o > y:
                            print('Choice out of range')
                            continue
                    v[o].buy_equipment()
                
                print()
                pause()
            elif a == 4:
                print()
            
            elif a == 5:
                print('You left the shop')
                break
            
    elif a == 3:
        while True:
            print()
            print('What do you want to do?')
            print('1. Display information')
            print('2. Equip weapons')
            print('3. Unequip weapons')
            print('4. Equip armor')
            print('5. Unequip armor')
            print('6. Exit')
            
            a = input('Choose:')
            
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
                print('Your current team consists of:')
                stat_print(3)                     #printing extended stats
                print()
                
                print('Currently held items: ')
                if held_items:                             #printing extended items
                    for x in held_items:
                        print(' ' + x.stat_name + ': function:' + x.fnc_name + ' for:' + str(x.x))
                elif not held_items:
                    print("You don't hold any items in your inventory")
                print()
                
                if held_weapons:
                    print('Currently held weapons:')
                    for x in held_weapons:              #printing weapon stats
                        print(' ' + x.stat_name + ': damage:' + x.stat_dmg + '(' + str(x.dmg_var) + ') ' + x.dmg_type_1 + ' ' + x.dmg_type_2)
                elif not held_weapons:
                    print('No weapons are being held in inventory')
                    
                if held_armor:
                    print('Currently held armor:')
                    for x in held_armor:
                        print(' ' + x.stat_name + ': defence:' + x.stat_defence + ' defence type:' + x.defence_type)
                elif not held_armor:
                        print('No armor is being held in inventory')
                        
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
                            o = input('Choose weapon to equip(type "ex" to exit)')
                            
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
                            o = input('Choose armor to equip(type "ex" to exit)')
                            
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
                            if x.weapon == basic:
                                print(' ' + str(y) + '. ' + x.stat_name + ' current weapon: ' + x.weapon.stat_name)
                            else:
                                print(' ' + str(y) + '. ' + x.stat_name + ' current weapon: ' + x.weapon.stat_name + ' damage:' + x.weapon.stat_dmg + '(' + str(x.weapon.dmg_var) + ')')
                        else:
                            if x.armor == basal:
                                print(' ' + str(y) + '. ' + x.stat_name + ' current armor: ' + x.armor.stat_name)
                            else:
                                print(' ' + str(y) + '. ' + x.stat_name + ' current armor: ' + x.armor.stat_name + ' defence:' + x.armor.stat_defence + ' defence type:' + x.armor.defence_type)
                    if a == 2:
                        l = input('Choose character that will wield this weapon(type "ex" to exit)')
                    else:
                        l = input('Choose character that will wear this armor(type "ex" to exit)')
                    
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
                            
                    
                    if a == 2 and team_1[l].weapon != basic:                         #if char already has a weapon
                        print(team_1[l].name + ' already has a ' + team_1[l].weapon.name + ' equipped')
                        x = input('Do you want to unequip ' + team_1[l].weapon.name + ' and equip ' + held_weapons[o].name + '? (yes to confirm) ')
                        if x != 'yes':         #only yes will allow  to equip a weapon
                            continue
                    elif a == 4 and team_1[l].armor != basal:
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
                        if v != basic:             #if old weapon existed(wasnt basic)
                            held_weapons.append(v)                    #add old weapon to held weapons
                        held_weapons.sort(key = sortid)
                    else:
                        v = team_1[l].armor             #setting placeholder for armor
                        team_1[l].unequip_armor()           #unequipping old armor
                        
                        held_armor[o].equip(team_1[l])      #equipping new one
                        print(team_1[l].name + ' now wears ' + held_armor[o].name)  #comment
                        
                        held_armor.pop(o)           #deleting new one from held armor
                        if v != basal:          #if old weapon wasn't basal(was normal armor)
                            held_armor.append(v)            #add old one to held armor
                        held_armor.sort(key = sortid)       #sort

                
            elif a == 3:
                while True:
                    print()
                    if y == -1:
                        print('None of your characters hold a weapon')
                        break
                    print('Characters currently wielding a weapon:')
                    y = -1
                    v = []
                    for x in team_1:
                        if x == False:
                            continue
                        if x.weapon == basic:    #if holds basic weapon then doesnt count
                            continue
                        v.append(x)
                        y += 1
                        print(str(y) + '. ' + x.stat_name + ': ' + x.weapon.stat_name + ' damage:' + x.weapon.stat_dmg + '(' + str(x.weapon.dmg_var) + ')')

                    print('Choose one, that will unequip his weapon')                    
                    o = input('Choose(type "ex" to quit):')
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
                    held_weapons.append(v[o].weapon)       #adding ld weapon to eq
                    held_weapons.sort(key = sortid)      #sorting
                    v[o].unequip_weapon()               #unequipping weapon
                
            elif a == 6:
                print()
                break

