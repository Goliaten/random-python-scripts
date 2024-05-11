#2 dimensional list substracion with structure[[indexes/headers], [data]]
def list_2d_sub(lis_1, lis_2):
    out = [[], []]
    
    for ind1, x in enumerate(lis_1[0]):         #for each in list 1
        if x in lis_2[0]:                       #if something like that is in list 2
            ind2 = lis_2[0].index(x)                    #get its index
            n_y = lis_1[1][ind1] - lis_2[1][ind2]          #substract one from another
            
            if n_y > 0:                           #if result is greater than 0
                out[0].append(x)            #add it and its new counter to the list
                out[1].append(n_y)
        else:                                   #if there is none of it in second list
            n_y = lis_1[1][ind1]         #add it to output with original values
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

    print(f'lis1-lis2 = {list_2d_sub_id(lis1, lis2)}')
    print(f'lis1-lis3 = {list_2d_sub_id(lis1, lis3)}')
    print(f'lis2-lis3 = {list_2d_sub_id(lis2, lis3)}')
