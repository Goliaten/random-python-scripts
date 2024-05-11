import subprocess, random, time, psutil

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

proc = subprocess.Popen(["ls", "/home/pi/Music/Muzyka/Tier_1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

o, e = proc.communicate()
# o = o.decode('utf-8')

n_o = []
y = -1
z = 0
for x in range(0, len(o)):
    y += 1
    if o[x] == '\n':
        n_o.append(o[z:y])
        z = y+1
        
c = 0
vol = -2500
timer = 0
#'/' '?' to end
#"'" '"' for next song
#'}' ']' to replay current song
#'+' '=' to increase sound
#'-' '_' to decrease sound
output = 'local' #'hdmi' #'both'
try:
    while True:
        z = 0
        if c == 0:
            x = random.randint(0, len(n_o)-1)
        print('Now playing: ' + n_o[x])
        
        print('p1 start')
        p1 = subprocess.Popen(["omxplayer", "-o", output, '-l', str(timer), '--vol', str(vol), '/home/pi/Music/Muzyka/Tier_1/' + n_o[x]], stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
        
        print(timer)
        
        if c != 2:
            timer = 0
            timer_b = time.time()
        timer_b = time.time() - timer + 0.7
        
        while p1.poll() == None:
            
            o = input(':')
            
            if o in ['/', '?']:     #end program
                z = 1
                try:
                    print('end kill')
                    kill(p1.pid)
                    break
                except:
                    print('end wait')
                    p1.wait()
                    
            elif o in ["'", '"']:     #play next song
                z = 0
                try:
                    print('next kill')
                    kill(p1.pid)
                    timer = 0
                    break
                except:
                    print('next wait')
                    p1.wait()
                    
            elif o in [']', '}']:         #replay same song
                c = 1
                z = 2
                try:
                    print('replay kill')
                    kill(p1.pid)
                    timer = 0
                    break
                except:
                    print('replay wait')
                    p1.wait()
            
            elif o == '+' or o == '=':       #increase volume
                c, z = 2, 2
                try:
                    vol += 300
                    timer = time.time() - timer_b
                    out, err = p1.communicate('+', 0)
                except:
                    print('+ except kill')
                    kill(p1.pid)
                    break
            elif o == '-' or o == '_':        #decrease volume
                c, z = 2, 2
                try:
                    vol -= 300
                    timer = time.time() - timer_b
                    out, err = p1.communicate('-', 0)
                except:
                    print('- except kill')
                    kill(p1.pid)
                    break
        
        print('z gate')
        if z == 1:
            break
        if z == 2:
            continue
        
        print('last p1 wait')
        p1.wait()
        c = 0
        print('ended')
except:
    print('last except kill')
    kill(p1.pid)
