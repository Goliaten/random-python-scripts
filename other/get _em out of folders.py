import subprocess
from os import path, listdir

cp = path.dirname(path.abspath(__file__))

out = listdir()
out = [x for x in out if "." not in x]
print(out)
input()


for x in out:
    files = listdir(x)
    #print(files, x)
    #input()
    
    for file in files:
        #print(" ".join(["copy", f'{cp}\\{x}\\{file}', f'{cp}\\{x} {file}']))
        #input()
        
        p1 = subprocess.Popen(["copy", f'{cp}\\{x}\\{file}', f'{cp}\\{x} {file}'], shell=True, text=True)
    
    
