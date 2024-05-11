from random import randint

print('Do you want to operate on text or a file? ')
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
            try:
                seedling = int(seed[siter]) * int(seed[siter+1]) - int(seed[siter])
            except:
                seedling = int(seed[siter]) * int(seed[0]) - int(seed[siter])
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
            try:
                seedling = int(seed[siter]) * int(seed[siter+1]) - int(seed[siter])
            except:
                seedling = int(seed[siter]) * int(seed[0]) - int(seed[siter])
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
        o_new = o + 'ex.' + ex
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
                        
                        try:
                            seedling = int(seed[siter]) * int(seed[siter+1]) - int(seed[siter])
                        except:
                            seedling = int(seed[siter]) * int(seed[0]) - int(seed[siter])
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
        ex = input('Write extension: ')
        while True:
            seed = input('Write 9 number seed: ')
            if len(seed) != 9:
                print('wrong seed')
                continue
            break
        
        siter = 0
        o_new = o + 'de.' + ex
        o = o + '.' + ex
        
        with open(o, 'r') as file:
            with open(o_new, 'w') as new_file:
                while True:
                    line = file.readline()
                    if line == '':
                        break
                    for x in line:
                        
                        if x == '\n' or x == '\r':
                            new_file.write(x)
                            continue
                        
                        try:
                            seedling = int(seed[siter]) * int(seed[siter+1]) - int(seed[siter])
                        except:
                            seedling = int(seed[siter]) * int(seed[0]) - int(seed[siter])
                        siter += 1
                        if siter > 8:
                            siter = 0
                            
                        x = ord(x)
                        x -= seedling
                        while x < 32:
                            x += 96
                        x = chr(x)
                        new_file.write(x)
        print(newer_o)
