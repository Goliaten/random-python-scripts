def list_2d_sort(lis, order='asc'):   #lis=list to be sorted, order='asc'(ascending) 'desc'(descending)
    out_id, out_cnt, sort_ord = [], [], []
    
    for ind_1, x in enumerate(lis[0]):
        maxx = min(lis[0])
        minx = max(lis[0])
        
        for ind2 in range(0, len(lis[0])):
            y = lis[0][ind2]
            
            if order == 'desc':
                maxx = y if y > maxx and y not in out_id else maxx    #sorted number
                s_num = maxx
            elif order == 'asc':
                minx = y if y < minx and y not in out_id else minx    #sorted number
                s_num = minx
                
        else:
            out_id.append(s_num)
            sort_ord.append(lis[0].index(s_num))
    
    for x in sort_ord:
        out_cnt.append(lis[1][x])
    out = [out_id, out_cnt]
    
    return out

if __name__ == '__main__':
    lis1 = [[80, 81, 93, 45], [1, 5, 4, 3]]
    lis2 = [[80, 81, 82, 83, 84], [2, 3, 4, 5, 6]]
    lis3 = [[93, 81], [2, 5]]
    
    list_2d_sort(lis1)
    list_2d_sort(lis1, 'asc')
    
    print(lis1)
    print(lis2)
    print(lis3)

