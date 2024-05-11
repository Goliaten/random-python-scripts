import subprocess

p1 = subprocess.Popen(['ls', '/home/pi/Documents/Katalog/0_normal sauce'], stdout=subprocess.PIPE, text=True)

norm, err = p1.communicate()
norm = norm.split('\n')
norm = [x.split(' ')[0] for x in norm]
print(norm)

out = ''
for x in norm:
    out += x + ' '
print(out)
