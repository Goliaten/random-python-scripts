from pprint import pprint
import json

imp_bone =  'Imp bone'
imp_horn =  'Imp horn'
imp_heart = 'Imp heart'
imp_soul =  'Imp soul'
dem_bone =  'Demon bone'
dem_skin =  'Demon skin'
dem_heart = 'Demon heart'
dem_soul =  'Demon soul'
dem_hskin = 'Demon hardened skin'
dem_essence = 'Demon essence'

met_nugget = 'Metal nugget'
met_ingot = 'Metal ingot'
met_scrap = 'Metal scrap'
met_rod   = 'Metal rod'
imp_ingot = 'Imp ingot'
imp_ingot_v2 = 'Imp ingot+'
dem_ingot =    'Demon ingot'

wood_plank = 'Wooden plank'
wood_stack = 'Wooden stack'


imp_def_drop_low = [met_nugget, '', '', '' ]
imp_def_drop_med = [met_nugget, met_nugget, imp_horn, '']
imp_def_drop_hig = [met_nugget, imp_bone, met_ingot, imp_heart]
dem_def_drop_low = [met_scrap, met_nugget, dem_bone, '']
dem_def_drop_med = [met_ingot, dem_skin, '', '']
dem_def_drop_hig = [met_ingot, met_rod, dem_heart, '']

imp_prb_drop_low = [met_nugget, imp_bone, imp_horn, '', '']
imp_prb_drop_med = [met_nugget, imp_bone, met_ingot, imp_heart, '']
imp_prb_drop_hig = [met_nugget, met_nugget, wood_plank, met_ingot, imp_soul]
dem_prb_drop_low = [met_scrap, met_scrap, met_ingot, dem_skin, '']
dem_prb_drop_med = [met_scrap, met_ingot, met_rod, dem_heart, '']
dem_prb_drop_hig = [met_ingot, met_rod, dem_hskin, dem_soul, '']

def_lis = [[], imp_def_drop_low, imp_def_drop_med, imp_def_drop_hig, dem_def_drop_low, dem_def_drop_med, dem_def_drop_hig]
prb_lis = [[], imp_prb_drop_low, imp_prb_drop_med, imp_prb_drop_hig, dem_prb_drop_low, dem_prb_drop_med, dem_prb_drop_hig]

glob_enem = ['11', '12', '21', '22', '31', '32', '33', '41', '42', '51', '52', '61', '62', '63']

b_l = [
[[[met_nugget, 4, 5]], [[met_ingot, 1, 1], [met_scrap, 3, 4]], [1, 6], 'Metal ingot <- nugget'],
[[[met_scrap, 12, 13]], [[met_ingot, 1, 1]], [5, 8], 'Metal ingot <- scrap'],
[[[met_ingot, 3, 4]], [[met_rod, 1, 1]], [9, 6], 'Metal rod <- ingot'],
# [[[wood_plank', 4, 6]], [[wood_stack, 1, 1]], [11, 10], 'Wooden stack <- plank'],
[[[imp_horn, 2, 2], [met_nugget, 10, 11]], [[imp_ingot, 1, 1], [met_scrap, 4, 5]], [7, 6], 'Imp ingot <- horn + nugget'],
[[[imp_horn, 2, 2], [met_ingot, 4, 5]], [[imp_ingot, 1, 1], [met_scrap, 2, 3]], [7, 6], 'Imp ingot <- horn + nugget'],
# [[[] ], [[], ], [], ''],
]

rank = 1

cmsn_deliv_dict = {}
out = []

while rank / 2 + 1 <= len(glob_enem):
    n_index = int(rank / 2)+1
    cmsn_deliv_dict[rank] = []
    
    for l in b_l:
        if rank >= l[2][0]:
            
            #----------------
            req_dic = {}
            
            for s_req in l[0]:
                req_dic[s_req[0]] = []
                for cnt in range(s_req[1], s_req[2]+1):
                    if cnt == 0:
                        continue
                    req_dic[s_req[0]].append(cnt)
            
            rew_dic = {}
            
            for s_req in l[1]:
                rew_dic[s_req[0]] = []
                for cnt in range(s_req[1], s_req[2]+1):
                    if cnt == 0:
                        continue
                    rew_dic[s_req[0]].append(cnt)
#             if rank == 20:
#                 print('first part:')
#                 print(l[0])
#                 print(l[1])
#                 print(req_dic)
#                 print(rew_dic)
#                 input()
            #------------------------
            
            req = []
            dic_len = 1
            for x in req_dic.values():
                dic_len *= len(x)
            M1 = 1
            M2 = dic_len
            
            for y, x in enumerate(req_dic):
                value = req_dic[x]
                
                M2 = int(M2 / len(value))
                
                
                for m1 in range(0, M1):
                    pass
                    for b1, b in enumerate(value):
                        pass
                        for m2 in range(0, M2):
#                             print(M1, len(value), M2, end=')
#                             print(m1, b1*M2, m2)
                            try:
                                index = b1*M2 + m2 + m1*M2*len(value)
                                req[index] += "'" + str(b)
#                                 req.append(str(b))
                            except:
                                req.append(str(b))
#                             print(req)
#                             input()
                            
                M1 = M1 * len(value)
            
            rew = []
            dic_len = 1
            for x in rew_dic.values():
                dic_len *= len(x)
            M1 = 1
            M2 = dic_len
            
            for y, x in enumerate(rew_dic):
                value = rew_dic[x]
                
                M2 = int(M2 / len(value))
                
                
                for m1 in range(0, M1):
                    pass
                    for b1, b in enumerate(value):
                        pass
                        for m2 in range(0, M2):
                            try:
                                index = b1*M2 + m2 + m1*M2*len(value)
                                rew[index] += "'" + str(b)
                            except:
                                rew.append(str(b))
                            
                M1 = M1 * len(value)
                
#             if rank == 20:
#                 print('\nsecond part:')
#                 print(req_dic)
#                 print(rew_dic)
#                 print(f'{req=}')
#                 print(f'{rew=}')
#                 input()
            
            #--------------------------------------
            mult = []
            y = 0
            while True:
                if rank >= l[2][0] + l[2][1]*y:
                    mult.append(y+1)
                else:
                    break
                y += 1
            if len(mult) > 2:
                mult = mult[-2:]
            
#             if rank == 20:
#                 print('\nthird part:')
#                 print(f'{mult=}')
#                 input()
            
            #-----------------------------------
            out = []
            
            for m in mult:
                for z, rq in enumerate(req):
                    rq = rq.split("'")
                    rq = [int(x)*m for x in rq]
                    
                    for y, rw in enumerate(rew):
                        rw = rw.split("'")
                        rw = [int(x)*m for x in rw]
                        rqk = [x for x in req_dic.keys()]
                        rwk = [x for x in rew_dic.keys()]
                        
                        s_out = [l[3], [rqk, rq], [rwk, rw]]
#                         print(s_out)
#                         input()
                        out.append(s_out)
            
            cmsn_deliv_dict[rank].append(out)
    rank += 1
    
# pprint(cmsn_deliv_dict[20])

with open('cmsn_deliv_dict_json.py', 'w') as file:
    file.write(json.dumps(cmsn_deliv_dict))
