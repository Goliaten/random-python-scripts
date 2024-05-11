for x in range(256):
    print(f'\033[38:5:{x}m {x}Hello there')

for x in range(256):
    print(f'\033[48:5:{x}m {x}Hello there')

print(f'\033[0mdone')
input()
for r in range(256):
    for g in range(256):
        for b in range(256):
            print(f'\033[38;2;{r};{g};{b}m█', end='')