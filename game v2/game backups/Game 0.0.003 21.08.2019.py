import random

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

def stat(char, c=0):
    if c == 0:
        print(char.stat_name, '- health:', str(char.hp) + '/' + str(char.maxhp), ' attack:', str(char.atkmin) + '-' + str(char.atkmax), ' armor:', char.armor)
    elif c == 1:
        print(char.stat_name, '- health:', str(char.hp) + '/' + str(char.maxhp), ' attack:', str(char.atkmin) + '-' + str(char.atkmax), ' armor:', char.armor, 'weapon:', char.weapon.stat_name, 'dmg:', char.weapon.dmg, 'var', char.weapon.dmg_var)


def EoT_summ():                                      #End of Turn summary
    for x in all_fghtr:
        if x == False:
            continue
        print(x.t_comm)
        if x.hp <= 0:
            x.t_comm = x.name + ' died'
        else:
            x.t_comm = x.name + ' did not do a thing'

def stat_print(c=0):
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
                print(str(o) + '. ' + y.name + ' ' + str(y.hp) + '/' + str(y.maxhp))
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
                print(str(o) + '. ' + y.name + ' ' + str(y.hp) + '/' + str(y.maxhp))
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

#item function
def heal(x):
    print("Who do you want to heal? ")
    team_target(1)
    
    a = team_1[o].hp                                      #for print measures
    team_1[o].hp += x
    
    if team_1[o].hp > team_1[o].maxhp:                     #prevent overheal
        team_1[o].hp = team_1[o].maxhp
    
    b = team_1[o].hp                                      #for print measures
    print(team_1[o].name + ' has been healed for', b-a, 'health up to current', team_1[o].hp, 'health points')


class Weapon:
    def __init__ (self, name, ID, cost, dmg, dmg_var, dmg_type_1, dmg_type_2='none'):
        self.name = name
        while len(name) < 8:
            name += ' '
        self.stat_name = name
        self.ID = ID
        self.cost = cost
        self.dmg = dmg
        self.dmg_var = dmg_var
        self.dmg_type_1 = dmg_type_1
        self.dmg_type_2 = dmg_type_2
    def equip(self, char):
        char.weapon = self
        char.atk += self.dmg
        char.atk_var += self.dmg_var
        
        char.atkmin = char.atk - char.atk_var           #atkmin and atkmax are for status display
        char.atkmax = char.atk + char.atk_var
        
        char.dmg_type_1 = self.dmg_type_1
        char.dmg_type_2 = self.dmg_type_2

basic = Weapon('None', 1001, 0, 0, 0, 'blunt')        #(name, ID, cost, dmg, dmg_var, dmg_type_1)
bat = Weapon('Bat', 1002, 50, 1, 1, 'blunt')
sword = Weapon('Sword', 1003, 120, 4, 0, 'slash')
hammer = Weapon('Hammer', 1004, 120, 3, 1, 'blunt')

global_weapons = [bat, sword, hammer]
global_weapons.sort(key = sortid)

held_weapons = [sword, hammer]

class Char:
    def __init__ (self, name, maxhp, atk, atk_var, armor=0, g_drop=0, weapon=basic):
        self.name = name
        while len(name) < 10:
            name += ' '
        self.stat_name = name
        self.maxhp = maxhp
        self.hp = maxhp
        self.atk = atk
        self.g_drop = g_drop                                                   #gold drop variable
        self.armor = armor
        
        self.atk_var = atk_var                                                 #attack variable
        self.atkmin = atk - atk_var
        self.atkmax = atk + atk_var
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
    def deal_dmg (self):
        atk_var = random.randint(0,self.atk_var*2) - self.atk_var             #making variable for damage
        atk_dmg = self.atk + atk_var                                          #calculating damage from atk and variable
        if atk_dmg <= 0:
            atk_dmg = 0
            self.t_comm = (self.name + ' dealt no damage to ' + p)                     #turn comment used in EoT_summ
        else:
            self.t_comm = (self.name + ' dealt ' + str(atk_dmg) + ' damage to ' + p)                      #turn comment used in EoT_summ
        return atk_dmg
    def heal_up(self):
        self.hp = self.maxhp
    def unequip_weapon(self):
        self.atk -= self.weapon.dmg
        self.atk_var -= self.weapon.dmg_var
        
        self.atkmin = self.atk - self.atk_var
        self.atmax = self.atk + self.atk_var
        self.dmg_type_1 = 'blunt'
        self.dmg_type_2 = 'none'
        basic.equip(self)

class Item:
    def __init__ (self, name, ID, cost, fnc_name, fnc, x):
        #fnc is a function, that said item will do. These functions have to be defined.
        while len(name) < 10:             #for nicer item printing
            name += ' '
        
        self.name = name
        self.ID = ID
        self.cost = cost
        
        while len(fnc_name) < 6:           #for nicer item printing
            fnc_name += ' '
        
        self.fnc_name = fnc_name
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

potion = Item('Potion', 101, 12, 'heal', heal, 10)        #Item(name, ID, cost, fnc_name, fnc, x(fnc_attrib)) 
potionv1 = Item('Potion v1', 102, 23, 'heal', heal, 20)
potionv2 = Item('Potion v2', 103, 45, 'heal', heal, 30)

held_items = [potionv1]                      #defining held items
healing_items = [potionv1, potion, potionv2]        #defining list of healing items
healing_items.sort(key = sortid)

global_items = {                                            #using dictionary for easier manipulation
    'Healing items': healing_items
    }

gold = 100

Hero = Char('Hero', 70, 10, 1, 0)        #max_hp, atk, atk_var, armor, gold_drop, weapon, damage type
monster = Char('Monster', 120, 8, 0, 0, 50)
Champion = Char('Champion', 90, 9, 2, 0, weapon=bat)
demon = Char('Demon', 40, 12, 4, 0, 50)

fghtr1 = Hero                                                      #defining characters in neutral way for turn-fighting
fghtr2 = monster                                                   #same :/
team_1 = [fghtr1,Champion,False]                                                  #defining team 1
team_2 = [fghtr2,demon,False]                                                  #defining team 2
all_fghtr = team_1 + team_2

print("defined")

while True:
    
    for x in all_fghtr:                    #heal for next battle
        if x == False:
            continue
        x.heal_up()
    
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
    
    if a == 1:
        while True:
            print()
            print("what do you want to do?")
            print("1.Attack 2.Use item 3.Flee")
            a = input("choose a number: ")
            
            try:              #error checking
                a = int(a)
            except:
                print('Wrong input')
                continue
            else:
                if a < 0 or a > 3:
                    print('Choice out of range')
                    continue
            
            if a == 1:
                print()
                print('Prepare for attack')

                for x in team_1:                                                                         #player choosing target
                    if x == False:                         #if player is nonexistent choose another one
                        continue
                    if x.hp <= 0:                       #if player is dead choose another one
                        continue
                    print('Who does ' + x.name + ' attack? ')
                    team_target(2)                              #choosing target
                    p = team_2[o].name                                           #defining p for class comment in deal_dmg
                    dmg = x.deal_dmg()
                    team_2[o].take_dmg(dmg)

                    e = fight_end_check()                                                       #breaking infinite while if hp<=0
                    if e == 'end':
                        print()
                        break
                if e == 'end':
                    break

            elif a == 2:
                print()
                z = 0
                while True:
                    
                    print('Available items:')
                    y = 0
                    for x in held_items:
                        print(y,'.', x.name)                     #printing held items
                        y += 1
                    
                    o = input('Choose (type "ex" to quit):')
                    
                    try:                             #error checking
                        o = int(o)
                    except:
                        if o == 'ex':
                            z = 1
                            break
                        else:
                            print('Wrong input')
                            print()
                            continue
                    else:
                        y -= 1
                        if o < 0 or o > y:
                            print('Choice out of range')
                            print()
                            continue
                    
                    held_items[o].use_item()
                    break
                if z == 1:                        #if typed 'ex' exit from inv choosing by doing whole turn loop again
                    continue
                
            elif a == 3:
                print("You fleed from battle")
                pause()
                print()
                break
            
            for x in team_2:
                if x == False:                #if fighter is nonexistend choose another
                    continue
                if x.hp <= 0:                      #if fighter is dead choose another one
                    continue
                o = random.randint(0,len(team_1)-1)                                                  #enemy choosing random target
                while team_1[o] == False or team_1[o].hp <= 0:
                    o = random.randint(0,len(team_1)-1)                                 #enemy choosing random target again if chose empty fighter place or fighter dead
                p = team_1[o].name
                dmg = x.deal_dmg()
                team_1[o].take_dmg(dmg)
                
                
            e = fight_end_check()                  #checking if fight ended
            if e == 'end':
                break
            else:
                EoT_summ()                       #if not printing summary
                stat_print()
                
    elif a == 2:
        while True:
            print()
            print('Welcome to the shop')
            print('Current gold:', gold)
            print('What do you want to do here?')
            print('1. Buy items')
            print('2. Sell items')
            print('3. Exit shop')
            
            a = input('Choose:')
            
            try:
                a = int(a)
            except:
                print('Wrong input')
                print()
            else:
                if a < 1 or a > 3:
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
                    y = 0
                    for x in global_items[d[l]]:
                        print(y, '.', x.name, 'function:' + x.fnc_name, 'cost:' + str(x.cost))
                        y += 1
                    v = global_items[d[l]]
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
                        y -= 1
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
                print('You left the shop')
                break
            
    elif a == 3:
        while True:
            print()
            print('What do you want to do?')
            print('1. Display information')
            print('2. Equip weapons')
            print('3. Unequip weapons')
            print('4. Exit')
            
            a = input('Choose:')
            
            try:
                a = int(a)
            except:
                print('Wrong input')
                continue
            else:
                if a < 0 or a > 4:
                    print('Choice out of range')
                    continue
            
            if a == 1:
                print('Your current team consists of:')
                stat_print(3)
                print()
                
                print('Currently held items: ')
                if held_items:
                    for x in held_items:
                        print(' ' + x.name + ': function:' + x.fnc_name + ' for:' + str(x.x))
                elif not held_items:
                    print("You don't hold any items in your inventory")
                print()
                
                if held_weapons:
                    print('Currently held weapons:')
                    for x in held_weapons:
                        dmg = str(x.dmg)
                        while len(dmg) < 2:
                            dmg = ' ' + dmg
                        print(' ' + x.name + ': damage:' + dmg + '(' + str(x.dmg_var) + ') ' + x.dmg_type_1 + ' ' + x.dmg_type_2)
                elif not held_weapons:
                    print('No weapons are being held in inventory')
                    
            elif a == 2:
                while True:
                    if held_weapons:
                        y = -1
                        print('Currently held weapons:')
                        for x in held_weapons:
                            y += 1
                            print(' ' + str(y) + '. ' + x.name + ': damage:' + str(x.dmg) + '(' + str(x.dmg_var) + ') ' + x.dmg_type_1 + ' ' + x.dmg_type_2)

                        o = input('Choose weapon to equip(type "ex" to exit)')
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
                        for x in team_1:
                            if x == False:
                                continue
                            y += 1
                            print(' ' + str(y) + '. ' + x.stat_name + ' current weapon: ' + x.weapon.name)
                            
                        l = input('Choose character that will wield this weapon(type "ex" to exit)')
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
                        if team_1[l].weapon != basic:
                            print(team_1[l].name + ' already has a ' + team_1[l].weapon.name + ' equipped')
                            a = input('Do you want to unequip ' + team_1[l].weapon.name + ' and equip ' + held_weapons[o].name + '? (yes to confirm) ')
                            if a != 'yes':
                                break
                            
                        v = team_1[l].weapon
                        team_1[l].unequip_weapon()
                        held_weapons[o].equip(team_1[l])
                        print(team_1[l].name + ' now wields ' + held_weapons[o].name)
                        held_weapons.pop(o)
                        if v != basic:
                            held_weapons.append(v)
                        held_weapons.sort(key = sortid)
                            
                    elif not held_weapons:
                        print("You don't hold any items in inventory")
                        pause()
                        break
                    print()
                
            elif a == 3:
                print()
                
            elif a == 4:
                print()
                break

