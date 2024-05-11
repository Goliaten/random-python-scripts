import time

x = 1
eq = []
inn = []

for _ in range(1000000):
    a = time.time()

    if 1 == x:
        pass

    b = time.time()

    if 1 in [x]:
        pass

    c = time.time()

    eq.append(b-a)
    inn.append(c-b)

# print(f'==:{b-a} in:{c-b}')
eq_avg = 0
for x in eq:
    eq_avg += x
eq_avg /= len(eq)

inn_avg = 0
for x in inn:
    inn_avg += x
inn_avg /= len(inn)

print(eq_avg, inn_avg)
