from time import time         #time and time_check are reserved

class time_check():
    def __init__(self):      #starts time tracking
        self.start_t = time()
    def check(self):         #prints current time from start
        end_t = time()
        t = end_t - self.start_t
        
        t_sec = int(t % 60)
        t_min = int(((t - t_sec) / 60) % 60)
        t_hr = int(((((t - t % 60) / 60) - t_min) / 60) % 24)
        
        print(f'Operation took {t_hr} hours {t_min} minuts {t_sec} seconds.')

a = '1'
b = '3'
t1 = time()
print('Hello ' + a + b)
print(time() - t1)
t2 = time()
print(f'Hello {a} {b}')
print(time() - t2)