def lis2cnt(lis):
    counter = [[], []]
    for x in lis:
        if not x in counter[0]:
            counter[0].append(x)
            counter[1].append(0)

        ind = counter[0].index(x)
        counter[1][ind] += 1
    
    return counter

if __name__ == '__main__':
    
    a = [1,2,3,3,5,1,2,2,6,7]
    
    print(f'{a} lis2cnt:{lis2cnt(a)}')
    