import random

#z is for while loops(error protection)
#o is for returns/data to be used outside of function AND targeting AND choices
#l is secondary/placeholder for choices
#p is secondary for targeting  AND better looking inventory prints(see item.buy_item)
#x and y are for 'for' loops
#y is for counter in for loop
#v is for empty input(not in pause func) AND a placeholder
#c is for choosing which option of function run
#a is for choosing what to do(in wide/main function)
#d is for choosing in dictionaries(see shope>buy items)
#p is for better looking inventory prints(see item.buy_item)

#function zone

def pause():
    emptyinput = input("Press anything to continue")

def sortid(y):
    return y.ID

def stat(char):
    print(char.name, '- health:', str(char.hp) + '/' + str(char.maxhp), ' attack:', str(char.atkmin) + '-' + str(char.atkmax), ' armor:', char.armor)

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
    if c==0 or c==1:
        for x in team_1:
            if x == False:
                continue
            stat(x)
    if c==0 or c==2:
        for x in team_2:
            if x == False:
                continue
            stat(x)

def team_target(x):
    global o
    z = 0
    if x==1:
        while z == 0:
            for y in team_1:                                       #printing team_1 members with indexes
                if y==False:
                    continue
                o = 0
                print(str(o) + '. ' + y.name)
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
                    
    if x==2:
        while z == 0:
            o = 0
            for y in team_2:
                if y==False:
                    continue
                print(str(o) + '. ' + y.name)
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

def fight_end(x, y=0):            #x is just to choose which side won, y is for gold obtained input
    if x == 1:
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
    if x == 2:
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
        fight_end(2)
        return 'end'
    
    x = 0
    for y in team_2:
        if y == False:
            continue
        x += y.hp
    if x <= 0:
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



class Char:
    def __init__ (self, name='unnamed', maxhp=10, atk=10, atk_var=1, armor=0, g_drop=0):
        self.name = name
        self.maxhp = maxhp
        self.hp = maxhp
        self.atk = atk
        self.g_drop = g_drop                                                   #gold drop variable
        self.armor = armor
        self.atk_var = atk_var                                                 #attack variable
        self.atkmin = atk - atk_var
        self.atkmax = atk + atk_var
    def take_dmg (self, damage):
        self.hp -= damage
        #print(self.name,' took ',damage,' damage.')
        #print()
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

class Item:
    def __init__ (self, name, ID, cost, fnc_name, fnc, x):
        #fnc is a function, that said item will do. These functions have to be defined.
        self.name = name
        self.ID = ID
        self.cost = cost
        self.fnc_name = fnc_name
        self.fnc = fnc
        self.x = x
    def use_item (self):
        x = self.x
        fnc = self.fnc
        fnc(x)
    def buy_item (self):
        global gold
        p = 'Are you sure you want to buy: ' + self.name + '? (type "yes" or "no") '
        a = input(p)
        if a == 'yes':
            if gold >= self.cost:
                gold -= self.cost
                held_items.append(self)
                
                print('You bought', self.name)
                print('You currently have', gold, 'gold')
                
                p = 'You are currently holding '
                held_items.sort(key = sortid)
                for x in held_items:
                    p = p + x.name + ', '
                print(p)
            else:
                print('You do not have enough gold')
        elif a == 'no':
            print()
        else:
            print('You discovered a secret everything besides yes works to not buy')

print('Functions defined')

#definition zone

potion = Item('Potion', 101, 12, 'heal', heal, 10)
potionv1 = Item('Potion v1', 102, 23, 'heal', heal, 20)
potionv2 = Item('Potion v2', 103, 45, 'heal', heal, 30)

held_items = [potionv1]

healing_items = [potionv1, potion, potionv2]
healing_items.sort(key = sortid)

global_items = {                                            #using dictionary for easier manipulation
    'Healing items': healing_items
    }

gold = 100

Hero = Char('Hero', 50, 10, 1, 0)        #max_hp, atk, atk_var, armor, gold_drop
monster = Char('monster', 80, 8, 0, 0, 50)
Champion = Char('Champion', 60, 9, 2, 0)
demon = Char('Demon', 30, 12, 4, 0, 50)

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
    
    try:
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
                print()
                print('Prepare for attack')

                for x in team_1:                                                                         #player choosing target
                    if x == False:
                        continue
                    if x.hp <= 0:
                        continue
                    print('Who does', x.name, 'attacks? ')
                    team_target(2)
                    p = team_2[o].name                                                                   #defining p for class comment in deal_dmg
                    dmg = x.deal_dmg()
                    team_2[o].take_dmg(dmg)

                    e = fight_end_check()                                                       #breaking infinite while if hp<=0
                if e == 'end':
                    EoT_summ()
                    print()
                    break
                

            elif a == 2:
                print()
                z = 0
                while True:
                    
                    print('Available items:')
                    y = 0
                    for x in held_items:
                        print(y,'.', x.name)
                        y += 1
                    
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
                            continue
                    else:
                        y -= 1
                        if o < 0 or o > y:
                            print('Choice out of range')
                            print()
                            continue
                    
                    held_items[o].use_item()
                    held_items.pop(o)
                    break
                if z == 1:
                    continue
                
            elif a == 3:
                print("You fleed from battle")
                pause()
                print()
                break
            
            for x in team_2:
                if x == False:
                    continue
                if x.hp <= 0:
                    continue
                o = random.randint(0,len(team_1)-1)                                                  #enemy choosing random target
                while team_1[o] == False:
                    o = random.randint(0,len(team_1)-1)                                 #enemy choosing random target again if chose empty fighter place
                p = team_1[o].name
                dmg = x.deal_dmg()
                team_1[o].take_dmg(dmg)
                
            EoT_summ()
            stat_print()
                
            e = fight_end_check()
            if e == 'end':
                break
                    
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
        print()

