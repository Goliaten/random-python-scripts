from math import factorial
seed = '126385074'
siter = 0

def seedling2(x):    #input is seed iterator
    
    def t_siter_ch(t):
        if t_siter > 8:
            t_siter -= 8
        return t_siter
    
    seedling = int(seed[t_siter_ch(x)])

    seedling *= int(seed[t_siter_ch(x+1)])

    try:
        seedling /= int(seed[t_siter_ch(x+4)])
    except ZeroDivisionError:
        seedling -= int(seed[t_siter_ch(x+3)]) + int(seed[t_siter_ch(x+5)])
    
    seedling -= int(seed[t_siter_ch(x+2)])

    seedling += int(seed[t_siter_ch(x+3)])
    
    seedlinger = factorial(int(seed[t_siter_ch(x+5)]))
    
    try:
        seedling += seedlinger ** (1/(int(seed[t_siter_ch(x+6)])/2))
    except ZeroDivisionError:
        seedling += seedlinger ** (1/3) - int(seed[t_siter_ch(x+5)])

    return int(seedling)

def seedling1(x):
    siter = x
    try:
        seedling1 = int(seed[siter]) * int(seed[siter+1]) - int(seed[siter+2])
    except:
        seedling1 = int(seed[siter]) * int(seed[0]) - int(seed[siter])
    return seedling1

    
x = 0
for _ in range(10):
    seedlingb = seedling2(x)
    seedlinga = seedling1(x)
    print(seedlinga, seedlingb, x)
    x = 1 + x if x < 8 else 0
    
