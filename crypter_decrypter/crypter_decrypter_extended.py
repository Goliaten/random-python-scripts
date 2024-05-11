from random import randint
from math import factorial

cont_num = 0

def seedling2(x):
    
    global siter
    
    def t_siter_ch(t_siter):
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

print('Do you want to operate on text or a file? ')
print('Keep in mind, that some letters exclusive to certain language may be decrypted wrongly')
b = input('Choose(type "text" or "file"): ')

if b == 'text':
    print('Do you want to encrypt, or decrypt text?')
    print('1. encrypt with random seed')
    print('2. encrypt with specified seed')
    print('3. decrypt')

    a = int(input('Choose: '))

    o = 'Hello world'
    new_o = ''
    newer_o = ''

    if a == 1:
        o = input('Write message to encrypt: ')
    elif a == 2:
        o = input('Write message to encrypt: ')
        while True:
            seed = input('write 9 number seed: ')
            if len(seed) != 9:
                print('wrong seed')
                continue
            break
    if a == 1 or a == 2:
        if a == 1:
            seed = str(randint(100000000, 999999999))
        # seed = str(123456789)
        siter = 0   #seed iterator
    
        for x in o:
            seedling = seedling2(siter)
            siter += 1
            if siter == 9:
                siter = 0
                
            x = ord(x)
            x += seedling
            while x > 127:
                x -= 96
            x = chr(x)
            new_o += x
        print('Original text: ' + o)
        print('Seed: ' + seed)
        print('Encrypted message: ' + new_o)

    if a == 3:
        o = input('Write text: ')
        while True:
            seed = input('Write 9 number seed: ')
            if len(seed) != 9:
                print('wrong seed')
                continue
            break
        
        siter = 0
        for x in new_o:
            seedling = seedling2(siter)
            siter += 1
            if siter > 8:
                siter = 0
                
            x = ord(x)
            x -= seedling
            while x < 32:
                x += 96
            x = chr(x)
            newer_o += x
        print(newer_o)
        
elif b == 'file':
    print('Do you want to encrypt, or decrypt a file?')
    print('1. encrypt with random seed')
    print('2. encrypt with specified seed')
    print('3. decrypt')

    a = int(input('Choose: '))

    new_o = ''
    newer_o = ''
    print('File has to be in the same directory as this script.')
    print('Write file without extension')
    
    if a == 1:
        o = input('Write a filename to encrypt: ')
        ex = input('Write extension: ')
    if a == 2:
        o = input('Write a filename to encrypt: ')
        ex = input('Write extension: ')
        while True:
            seed = input('write 9 number seed: ')
            if len(seed) != 9:
                print('wrong seed')
                continue
            break
    
    if a == 1 or a == 2:
        o_new = o + '.' + ex + 'e7'
        o += '.' + ex
        with open(o, 'r') as file:
            with open(o_new, 'w') as new_file:
                if a == 1:
                    seed = str(randint(100000000, 999999999))
                # seed = str(123456789)
                siter = 0   #seed iterator
                
                while True:
                    line = file.readline()
                    if line == '':
                        break
                    for x in line:
                        
                        if x == '\n' or x == '\r':
                            new_file.write(x)
                            continue
                        
                        seedling = seedling2(siter)
                        siter += 1
                        if siter == 9:
                            siter = 0
                            
                        x = ord(x)
                        x += seedling
                        while x > 127:
                            x -= 96
                        x = chr(x)
                        new_file.write(x)
            print('Original file: ' + o)
            print('Seed: ' + seed)
            print('Encrypted file: ' + o_new)
            
    if a == 3:
        o = input('Write a filename: ')
        while True:
            ex = input('Write extension: ')
            if ex[-2:] != 'e7':
                print('Extension unsupported.')
                print('Use only ._e7 files in this decoder.')
                print('_ being any characters')
                continue
            break
        while True:
            seed = input('Write 9 number seed: ')
            if len(seed) != 9:
                print('wrong seed')
                continue
            break
        
        siter = 0
        o_new = o + '.' + ex[0:-2]
        o = o + '.' + ex
        
        with open(o, 'r') as file:
            with open(o_new, 'w') as new_file:
                while True:
#                     cont_num += 1
#                     print(cont_num)
#                     if cont_num == 10000:
#                         pause()
                    line = file.readline()
                    if line == '':
                        break
                    for x in line:
                        if x == '\n' or x == '\r':
                            new_file.write(x)
                            continue
                        
                        seedling = seedling2(siter)
                        siter += 1
                        if siter > 8:
                            siter = 0
                            
                        x = ord(x)
                        x -= seedling
                        while x < 32:
                            x += 96
                        x = chr(x)
                        new_file.write(x)
                        
        print('Original file: ' + o)
        print('Seed: ' + seed)
        print('Decrypted file: ' + o_new)
