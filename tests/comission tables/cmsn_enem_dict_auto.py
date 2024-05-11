
glob_enem = ["imp_1","imp_2","imp_3","imp_4","imp_5","imp_6",
                  "demon_1","demon_2","demon_3","demon_4","demon_5","demon_6","demon_7"]

cmsn_enem_dict = "cmsn_enem_dict = {\n"

e_1 = "imp_2"
e_2 = "imp_1"
e_3 = "imp_0"
rank = 3
spacer = "          "

while rank / 2 + 1 <= len(glob_enem):
    n_index = int(rank / 2)+1
    out = f"    '{rank}': ["
    if rank % 2 == 1:
        e_1, e_2, e_3 = glob_enem[n_index], e_1, e_2
        
        
        out += f"['', [{e_1}], [2]], "
        out += f"['', [{e_1}, {e_2}], [2, 1]], "
        out += f"['', [{e_1}, {e_3}], [2, 4]], \n"
        
        out += spacer + f"['', [{e_2}], [7]], "
        out += f"['', [{e_2}], [8]], \n"
        out += spacer + f"['', [{e_2}, {e_3}], [4, 8]], "
        out += f"['', [{e_2}, {e_3}], [4, 7]], \n"
        out += spacer + f"['', [{e_2}, {e_3}], [3, 10]], "
        out += f"['', [{e_2}, {e_3}], [3, 9]], \n"
        
        out += spacer + f"['', [{e_3}], [14]], "
        out += f"['', [{e_3}], [13]]"
    
    else:
        out += f"['', [{e_1}], [5]], "
        out += f"['', [{e_1}], [4]], \n"
        
        out += spacer + f"['', [{e_1}, {e_2}, {e_3}], [2, 6, 8]], "
        out += f"['', [{e_1}, {e_2}, {e_3}], [2, 6, 7]], \n"
        out += spacer + f"['', [{e_1}, {e_2}, {e_3}], [2, 5, 8]], "
        out += f"['', [{e_1}, {e_2}, {e_3}], [2, 5, 7]], \n"
        
        out += spacer + f"['', [{e_1}, {e_2}], [3, 6]], "
        out += f"['', [{e_1}, {e_2}], [3, 5]], \n"
        out += spacer + f"['', [{e_1}, {e_3}], [3, 8]], "
        out += f"['', [{e_1}, {e_3}], [3, 7]], \n"
        
        out += spacer + f"['', [{e_2}], [11]], "
        out += f"['', [{e_2}], [10]], \n"
        out += spacer + f"['', [{e_2}, {e_3}], [6, 12]], "
        out += f"['', [{e_2}, {e_3}], [6, 11]], \n"
        
        out += spacer + f"['', [{e_3}], [16]]"
        
    out += " ],\n"
    cmsn_enem_dict += out
    
    rank += 1
    
cmsn_enem_dict += "\n    }"

print(cmsn_enem_dict)


