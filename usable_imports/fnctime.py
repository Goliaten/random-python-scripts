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

if __name__ == '__main__':
    print('Initialise timer')
    t = time_check()
    print('Now we wait for some time')
    for x in range(1, 1000000):
        x = x*x/x*x/x*x/x
    print('Now we check')
    t.check()