from sys import getsizeof as gs

a = {}
b = [[], []]
for x in range(100):
    a[x] = x
    b[0].append(x)
    b[1].append(x)

print(f'a:{gs(a)} b:{gs(b)}')