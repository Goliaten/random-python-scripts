import random
a = int(input('Write a number from 0 to 10000 '))
i = 0
while True:
    i += 1
    b = random.randint(0, 10000)
    print(str(i) + '.' + str(b))
    if b == a:
        break