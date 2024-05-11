
from random import randint

# to do: different weapons callibers, multiple ships in a squad, multiple types of ships, damage model, 


class Ship():
    
    def __init__(self, name, HEALTH_POINTS):
        
        self.name = name
        self.HEALTH_POINTS = HEALTH_POINTS
        
        pass


def calculateCombinedHealth(squad):
    combinedHealth = 0
    for x in squad:
        combinedHealth += x.HEALTH_POINTS
    
    return combinedHealth

basicHitChance = 20
basicDamage = 10

ship1 = Ship("DD 1", 100)
ship2 = Ship("DD 2", 120)

squad1 = (ship1,)
for x in squad1:
    x.squad = 1
    
squad2 = (ship2,)
for x in squad2:
    x.squad = 2

allShips = squad1 + squad2


combinedHEALTHofsquad1 = calculateCombinedHealth(squad1)
combinedHEALTHofsquad2 = calculateCombinedHealth(squad2)

conditionOfFight = combinedHEALTHofsquad1 != 0 and combinedHEALTHofsquad2 != 0

while True:
    
    for vessel in allShips:
        
        if vessel.squad == 1:
            damage = basicDamage
            hitChance = basicHitChance
            target = randint(0, len(squad2)-1)
            hitroll = randint(0, 100)
            
            if hitroll < hitChance:
                squad2[target].HEALTH_POINTS -= damage
                print(f"{vessel.name} hit {squad2[target].name} for {damage}.")
                
            else:
                print(f"{vessel.name} shot {squad2[target].name} but missed.")
            
        elif vessel.squad == 2:
            damage = basicDamage
            hitChance = basicHitChance
            target = randint(0, len(squad1)-1)
            hitroll = randint(0, 100)
            
            if hitroll < hitChance:
                squad1[target].HEALTH_POINTS -= damage
                print(f"{vessel.name} hit {squad1[target].name} for {damage}.")
                
            else:
                print(f"{vessel.name} shot {squad1[target].name} but missed.")
            
        else:
            pass #maybe an unknown vessel will enter the battle one day
        
        
    combinedHEALTHofsquad1 = calculateCombinedHealth(squad1)
    combinedHEALTHofsquad2 = calculateCombinedHealth(squad2)
    
    doContinue = False
    if combinedHEALTHofsquad1 == 0:
        print("Squad 1 has been destroyed")
    elif combinedHEALTHofsquad2 == 0:
        print("Squad 2 has been destroyed")
    else:
        doContinue = True
    
    if not doContinue:
        break
    



