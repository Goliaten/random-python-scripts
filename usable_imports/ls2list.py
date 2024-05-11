import subprocess

def ls2list(path="/home/pi/Music/Muzyka/Tier_1"):
    if type(path) != str:
        raise Exception('Path has to be string')
    proc = subprocess.Popen(["ls", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    o, e = proc.communicate()

    n_o = []
    y = -1
    z = 0
    for x in range(0, len(o)):
        y += 1
        if o[x] == '\n':
            n_o.append(o[z:y])
            z = y+1
            
    return(n_o)

if __name__ == '__main__':
    print(ls2list())
