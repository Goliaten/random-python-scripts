
with open('cmsn_deliv_dict_json.py', 'r') as file:
    with open('cmsn_deliv_dict_json2.py', 'w') as n_file:
        y = 0
        focus = ' '
        skip = 0
        
        while focus != '':
            if y == 0:
                focus = file.read(2)
                y += 1
            else:
                while skip > 0:
                    focus = focus[1] + file.read(1)
                    skip -= 1
                    
                focus = focus[1] + file.read(1)
            
            if focus == ' "':
                skip = 1
            elif focus == '" ':
                skip = 1
            
            else:
                n_file.write(focus[0])
            
            
            
