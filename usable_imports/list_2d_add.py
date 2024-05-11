def list_2d_add(lis_1, lis_2):
    out = [[], []]

    for ind1, x in enumerate(lis_1[0]):        #for each in list 1
        if x in lis_2[0]:                      #if something like it is in list 2
            ind2 = lis_2[0].index(x)                 #find its index
            n_y = lis_1[1][ind1] + lis_2[1][ind2]        #sum 2 values up
            
            if n_y > 0:                 #if new value is greater then 0 (should always be, but yeah, safety)
                out[0].append(x)           #add it and its id to output
                out[1].append(n_y)
        else:                             #if its not in other list
            n_y = lis_1[1][ind1]
            out[0].append(x)             #add what was given to output
            out[1].append(n_y)
            
    for ind2, x in enumerate(lis_2[0]):     #now for each in list 2
        if x not in out[0]:                 #if it's not in output yet
            n_y = lis_2[1][ind2]           #add it
            out[0].append(x)
            out[1].append(n_y)
    
    return out

if __name__ == '__main__':
    lis1 = [[80, 81, 93, 45], [1, 5, 4, 3]]
    lis2 = [[80, 81, 82, 83, 84], [2, 3, 4, 5, 6]]
    lis3 = [[93, 81], [2, 5]]

    print(lis1)
    print(lis2)
    print(lis3)

    print(f'lis1+lis2 = {list_2d_add(lis1, lis2)}')
    print(f'lis1+lis3 = {list_2d_add(lis1, lis3)}')
    print(f'lis2+lis3 = {list_2d_add(lis2, lis3)}')
