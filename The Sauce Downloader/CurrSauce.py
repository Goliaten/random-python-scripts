import subprocess

p1 = subprocess.Popen(['ls', '-p'], stdout=subprocess.PIPE, text=True)
lis = p1.communicate()[0].split('\n')[:-1]

lis = [x for x in lis if x[-1] == '/']

with open('The Sauce List.txt', 'w') as file:
    for cat in lis:
        p1 = subprocess.Popen(['ls', cat], stdout=subprocess.PIPE, text=True)
        sc = p1.communicate()[0].split('\n')[:-1]
        
        sc = [int(x.split(' ')[0]) for x in sc]
        sc.sort()
        
        sc = [str(x) for x in sc]
        sc = ' '.join(sc)
        
        file.write(cat[:-1] + '\n' + sc + '\n')