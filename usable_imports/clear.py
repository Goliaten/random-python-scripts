from os import name, system

def clear():              #used to clear terminal/shell screen
    if name == 'nt':           #on windows
        system('cls')
    else:                #on linux/macOS  (Posix)
        system('clear')

if __name__ == '__main__':
    print('We write something')
    input('And after click we clear it')
    clear()
    print('See?')