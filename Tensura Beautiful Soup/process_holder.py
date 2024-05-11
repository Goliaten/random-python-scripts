import subprocess
import time
import psutil
import cfscrape
from fnctime import time_check

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

ttime = time_check()

#begin process
p0 = subprocess.Popen('cd /home/pi/scripts/"Tensura Beautiful soup" && python3.8 "new Tensura download.py"', stderr=subprocess.PIPE, text=True, shell=True)
#define variable for checking if p0 is alive
status = p0.poll()

try:
    while True:
        if status != None:          #if process is dead  start it again
            print('\nStart it again')
            p0 = subprocess.Popen('cd /home/pi/scripts/"Tensura Beautiful soup" && python3.8 "new Tensura download.py"', stderr=subprocess.PIPE, text=True, shell=True)
            status = p0.poll()      #and renew status
            
        while status == None:                        #while it is alive
            print(p0.stdout if p0.stdout else '', end='')     #print what it has printed
            time.sleep(1)                    #wait(so that this holder does not slow down OS)
            status = p0.poll()              #check again
            
        a, b = p0.communicate()              #after it has ended(or was killed) communicate with what was left
        
        if b == 'Segmentation fault\n':        #if Segmentation fault occured: 
            print('--Segmentation fault--')
            continue                           #go again
        if 'UnicodeDecodeError' in b:                     #some other errors, that occured for me
            print('Unicode Decode Error')
            continue
        if 'Illegal instruction' in b:
            print('Illegam instruction')
            continue
        if 'ConnectionError' in b:
            print('Connection Error')
            continue
        if 'Fatal Python error' in b:
            print('Fatal Python error')
            print(f'--b: {b} --')
            continue
        if 'Aborted' in b:
            print('Aborted?')
            print(f'--b: {b} --')
            continue
        
        print(f'--b: {b} --')                       #if no error was found print potential error message
        print('--all done--')
        break                        #and break whole loop
except KeyboardInterrupt:          #if ctrl^C was clicked
    try:
        kill(p0.pid)           #kill the process
    except:
        print('already dead')      #unless it's dead already

ttime.check()