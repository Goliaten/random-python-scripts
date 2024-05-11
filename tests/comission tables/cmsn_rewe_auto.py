imp_def_drop_low = ['met_nugget', '', '', '']
imp_def_drop_med = ['met_nugget', 'met_nugget', 'imp_horn', '']
imp_def_drop_hig = ['met_nugget', 'imp_bone', 'met_ingot', 'imp_heart']
dem_def_drop_low = ['met_scrap', 'met_nugget', 'dem_bone', '']
dem_def_drop_med = ['met_ingot', 'dem_skin', '', '']
dem_def_drop_hig = ['met_ingot', 'met_rod', 'dem_heart', '']

imp_prb_drop_low = ['met_nugget', 'imp_bone', 'imp_horn', '', '']
imp_prb_drop_med = ['met_nugget', 'imp_bone', 'met_ingot', 'imp_heart', '']
imp_prb_drop_hig = ['met_nugget', 'met_nugget', 'wood_plank', 'met_ingot', 'imp_soul']
dem_prb_drop_low = ['met_scrap', 'met_scrap', 'met_ingot', 'dem_skin', '']
dem_prb_drop_med = ['met_scrap', 'met_ingot', 'met_rod', 'dem_heart', '']
dem_prb_drop_hig = ['met_ingot', 'met_rod', 'dem_hskin', 'dem_soul', '']

def_lis = [[], imp_def_drop_low, imp_def_drop_med, imp_def_drop_hig, dem_def_drop_low, dem_def_drop_med, dem_def_drop_hig]
prb_lis = [[], imp_prb_drop_low, imp_prb_drop_med, imp_prb_drop_hig, dem_prb_drop_low, dem_prb_drop_med, dem_prb_drop_hig]

glob_enem = ['11', '12', '21', '22', '31', '32', '33', '41', '42', '51', '52', '61', '62', '63']
#imps 1=low 2=med 3=hig
#demons 4=low 5=med 6=hig
# *1 no prb items *2 some prb items *3 lot of prb items

e_1 = '11'
e_2 = '00'
e_3 = '00'
e = [e_1, e_2, e_3]

rank = 1
spacer = '         '
rews = 'cmsn_rewe_dict = {\n'

while rank / 2 + 1 <= len(glob_enem):
    n_index = int(rank / 2)+1
    
    if rank % 2 == 1:
        e_1, e_2, e_3 = glob_enem[n_index], e_1, e_2
        
    if e_1 != '00':
        if e_1[0] == '1':
            defd = imp_def_drop_low
            prbd = imp_prb_drop_low
        elif e_1[0] == '2':
            defd = imp_def_drop_med
            prbd = imp_prb_drop_med
        elif e_1[0] == '3':
            defd = imp_def_drop_hig
            prbd = imp_prb_drop_hig
        elif e_1[0] == '4':
            defd = dem_def_drop_low
            prbd = dem_prb_drop_low
        elif e_1[0] == '5':
            defd = dem_def_drop_med
            prbd = dem_prb_drop_med
        elif e_1[0] == '6':
            defd = dem_def_drop_hig
            prbd = dem_prb_drop_hig
    
        if e_1[1] == '1':
            rewd = [[0, 1], [0, 2], [0, 0, 0], [1, 2], [2, 2]]
            rewp = [[], [1], [2]]
        elif e_1[1] == '2':
            rewd = [[1,1,1], [1,1,2], [1,2], [1,3], [3], [2,2]]
            rewp = [[1,1], [2], [3], [0, 0, 1]]
        elif e_1[1] == '3':
            rewd = [[1,2,2], [1,2,3], [2,3], [3,3], [2,3,3], [0,1,2,3]]
            rewp = [[2, 3, 3], [1, 4, 4], [4, 4], [3, 3], [3, 4], [2, 2, 4]]
        
    rews += spacer + f'{rank}: [\n'
    b_i = []   #big items (dont ask, it 23:17)(big counter of items)
    
    for x in rewd:
        for y in rewp:
            s_i = []
            out = spacer + '  ['
            for z in x:
                t = defd[z]
                if t != '':
                    out += f"'{t}', "
                    s_i.append(t)
                else:
                    for f in defd:
                        if f != '':
                            out += f"'{f}', "
            for l in y:
                t = prbd[l]
                if t != '':
                    out += f"'{t}', "
                    s_i.append(t)
                else:
                    for f in prbd:
                        if f != '':
                            out += f"'{f}', "
            out += '],\n'
            if out != spacer + '  [],\n' and s_i not in b_i:
                rews += out
                b_i.append(s_i)
    else:
        rews += spacer + '],\n'
    
    
    rank += 1
    
rews += '}'
print(rews)
