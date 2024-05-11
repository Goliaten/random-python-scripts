def list_2d_sort(lis, order='asc'):   #lis=list to be sorted, order='asc'(ascending) 'desc'(descending)
    out_id, out_cnt, sort_ord = [], [], []
    z = 0
    
    if type(lis[0][0]) != int:           #converting first part of list from class instances to ID
        lis[0] = char2num(lis[0])
        z = 1
    
    n_lis = [x for ind1, x in enumerate(lis[0]) if ind1 not in out_id ]
    for x in n_lis:           #for each of the ID
        maxx = lis[0].index(min(n_lis))             #get minimal ID
        minx = lis[0].index(max(n_lis))             #get maximal ID
        max_lis = [x if ind1 not in sort_ord else minx for ind1, x in enumerate(lis[0])]
        min_lis = [x if ind1 not in sort_ord else maxx for ind1, x in enumerate(lis[0])]
        
        if order == 'desc':
            for ind_2, y in enumerate(max_lis):        #go over each of ID again
                    maxv = lis[0][maxx]
                    if y > maxv and ind2 not in sort_ord:
                        maxx = ind2
                    s_num = maxx

        elif order == 'asc':
            for ind2, y in enumerate(min_lis):
                minv = lis[0][minx]
                if y < minv and ind2 not in sort_ord:
                    minx = ind2
                s_num = minx
                
        out_id.append(lis[0][s_num])
        sort_ord.append(s_num)
    
    for x in sort_ord:
        out_cnt.append(lis[1][x])
    out = [out_id, out_cnt]
    
    if z == 1:
        out[0] = num2char(out[0])
    return out

if __name__ == '__main__':
    
    a = [[12,1,5,23,76,3,54,5], [1,2,3,4,5,6,7,8]]
    
    print(a)
    print(list_2d_sort(a))
    
    
    