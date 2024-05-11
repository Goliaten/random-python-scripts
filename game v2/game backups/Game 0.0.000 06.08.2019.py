import random
print("'''''''''''''''''''''''''''''''''''''''''")
print("'                                       '")
print("'              Initialising             '")
print("'                  Game                 '")
print("'                                       '")
print("'                                       '")
print("'                                       '")
print("'                                       '")
print("'                                       '")
print("'                                       '")
print("'                                       '")
print("'''''''''''''''''''''''''''''''''''''''''")
def pause():
    emptyinput = input("Press anything to continue")

def stat(char):
    print(char.name, '- health:', str(char.hp) + '/' + str(char.maxhp), ' attack:', str(char.atkmin) + '-' + str(char.atkmax), ' armour:', char.armor)

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
    if x==1:
        for y in team_1:
            if y==False:
                continue
            o = 0
            print(str(o) + '. ' + y.name)
            o += 1
        o = int(input('Choose: '))
    if x==2:
        for y in team_2:
            if y==False:
                continue
            o = 0
            print(str(o) + '. ' + y.name)
            o += 1
        o = int(input('Choose: '))

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
    def __init__ (self, name='unnamed', maxhp=10, atk=10, g_drop=0, armor=0, atk_var=1):
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
            print(self.name, ' dealt no damage to ', p)
        else:
            print(self.name,' dealt ',atk_dmg,' damage to ', p)                      #printing info
        return atk_dmg

class Item:
    def __init__ (self, name, fnc, x):
        #fnc is a function, that said item will do. These functions have to be defined.
        self.name = name
        self.fnc = fnc
        self.x = x
    def use_item (self):
        x = self.x
        fnc = self.fnc
        fnc(x)

potion = Item('Potion', heal, 10)
items = [potion]

Hero = Char('Hero', 15, 10, 1)
monster = Char('monster', 30, 5, 1)
fghtr1 = Hero                                                      #defining characters in neutral way for turn-fighting
fghtr2 = monster                                                   #same :/
team_1 = [fghtr1,False,False]                                                  #defining team 1
team_2 = [fghtr2,False,False]                                                  #defining team 2

print("defined")

while True:
    print("What do you want to do?")
    print("1.Fight a monster 2.Go to shop 3. Check items/character")
    a = int(input("Choose: "))

    if a == 1:
        while fghtr1.hp > 0 and fghtr2.hp > 0:
            #print(Hero.name, ': ', Hero.maxhp, Hero.hp, Hero.atk, Hero.armor)
            #print(monster.name, ': ', monster.maxhp, monster.hp, monster.atk, monster.armor)
            print("what do you want to do?")
            print("1.Attack 2.Use item 3.Flee")
            a = int(input("choose a number: "))
            
            if a == 1:
                print()
                print('Prepare for attack')

                for x in team_1:                                                                         #player choosing target
                    if x == False:
                        continue
                    print("Who do you want to attack? ")
                    team_target(2)
                    p = team_2[o].name                                                                   #defining p for class comment in deal_dmg
                    dmg = x.deal_dmg()
                    team_2[o].take_dmg(dmg)
                
                if fghtr1.hp <= 0 or fghtr2.hp <= 0:                                                     #breaking infinite while if hp<=0
                    stat_print()
                    break
                

            elif a == 2:
                print()
                print('Available items:')
                for x in items:
                    y = 0
                    print(y,'.', x.name)
                    y+=1
                print('Which one do you want to use?(Type "ex" to cancel)')
                o = input('Choose: ')
                if o == 'ex':
                    continue
                else:
                    o = int(o)
                    items[o].use_item()
                
                
                
                print()
                pause()
            elif a == 3:
                print("You fleed from battle")
                pause()
                print()
                break
            else:
                print("zła akcja")
                print()
                pause()
                
            for x in team_2:
                if x == False:
                    continue
                o = random.randint(0,len(team_1)-1)                                                  #enemy choosing random target
                while team_1[o] == False:
                    o = random.randint(0,len(team_1)-1)                                 #enemy choosing random target again if chose empty fighter place
                p = team_1[o].name
                dmg = x.deal_dmg()
                team_1[o].take_dmg(dmg)
                stat_print()
                pause()
                print()                
                    
    elif a == 2:
        print()
    elif a == 3:
        print()
    else:
        print("Wrong action")
        pause()
