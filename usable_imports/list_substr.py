def list_substr(lis_1, lis_2):
    #substracts values of list 2 from list 1 and outputs result and indexes with values lower than 0
    out, r_list = [], []              #r_list = 'removed' list
    maxim = 0
    
    for l, x in enumerate(zip(lis_1, lis_2)):
        maxim = l + 1
        x, y = x                    #unpacking list
        z = x - y                    #calculating new number
        if z <= 0:                    #if it's smaller than 0
            r_list.append(l)        #add index, at which it was, to 'removed' list
            continue
        out.append(z)
    else:
        for x in range(maxim, len(lis_1)):       #add those numbers, which index was bigger, than those of lis_2
            out.append(lis_1[x])
    return out, r_list

if __name__ == '__main__':
    a = [5,3,5,7,5]
    b = [1,2,5,0,7,12]
    print(a, '\n', b)
    print(list_substr(a, b))
    