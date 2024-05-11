def stat_len(x, y=1, c=0):      #x is value to be lengthened, y is length, c is option choosing
    x = str(x)
    while len(x) < y and c == 0:          #adds ' ' to the end
        x += ' '
    while len(x) < y and c == 1:          #adds ' ' to the beginning
        x = ' ' + x
    return x

out = None
temp_out = ''
with open('data.txt', 'r') as file:
    with open('date.txt', 'w') as n_file:
        while True:
            line = file.read(1)
            restricted = ('/', ' ', '\r', '\n', ':', '')
            
            if line not in restricted:
                if not temp_out:
                    temp_out = line
                else:
                    temp_out += line
                    
            elif line == '\n' or line == '':
                temp_out += line
                out += temp_out
                n_file.write(out)
                out, temp_out = '', ''
                
            elif line == ' ':
                temp_out += line
                out += temp_out
                temp_out = ''
                
            elif line == '/' or line == ':':
                if len(temp_out) == 1:
                    temp_out = '0' + temp_out
                temp_out += line
                if not out:
                    out = temp_out
                else:
                    out += temp_out
                temp_out = ''
            
            if line == '':
                break
            
            
time = []
for x in range(0, 24):
    x = str(x)
    if len(x) == 1:
        x = '0' + x
    time.append(x + ':00')
    time.append(x + ':30')
    
control = ' '
out = ''
t_1 = 0
t_2 = 0
t_3 = 0
y = 0
with open('date.txt', 'r') as file:
    with open('output.txt', 'w') as n_file:
        while True:
            line = ''
            z = ''
            while True:
                z = file.read(1)
                if z == '':
                    control = z
                    break
                elif z != '\n':
                    line += z
                else:
                    line += z
                    break
            if control == '':
                break
            y = 0
            t_1 = 0
            t_2 = 0
            t_3 = 0
            if len(line) < 23:
                n_file.write(line[:10] + ' 24 0 0\n')
                continue
            out = line[:10]#(file.read(10))
            begin = line[11:16]#file.read(6)[1:]
            end = line[17:22]#file.read(6)[1:]
            control = line[22]#file.read(1)
            for x in time:
                if y == 0:
                    if x != begin:
                        t_1 += 1
                    elif x == begin:
                        t_2 += 1
                        y = 1
                        continue
                if y == 1:
                    if x != end:
                        t_2 += 1
                    elif x == end:
                        t_3 += 1
                        y = 2
                        continue
                if y == 2:
                    t_3 += 1
            out += ' ' + str(t_1/2) + ' ' + str(t_2/2) + ' ' + str(t_3/2)
            n_file.write(out + '\n')
            out = None
                    