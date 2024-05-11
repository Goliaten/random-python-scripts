def AI_mage_heal(char):
    AI_target, AI_secon = None, None
    ST_heals, MT_heals, AT_heals = [], [], []
    psbl_heals = [[], []]    #possible to use/be worth using heals; [magic], [target]
    loss_toler = 5       #increases border of loss(if heal would be 5 too big, it would still heal)
    opt_atk = 0           #option for not using attack
    
    print(char.name)
    
    #----------ordering healing magic--------------
    for magic in char.magic:
        f_n = magic.fnc_name     #f_n = function name/fnc_name
        if 'heal' in f_n:                                 #this AI is focused on healing magic - PLACE FOR DIFFERENT VERSIONS
            if 'ST' in f_n:
                ST_heals.append(magic)
            elif 'MT' in f_n:
                MT_heals.append(magic)
            elif 'AT' in f_n:
                AT_heals.append(magic)
    print('-----')
    print('ST', [x.name for x in ST_heals], 'MT', [x.name for x in MT_heals], 'AT', [x.name for x in AT_heals])
    
    #------getting team-------
    if char.team == 'team 1':
        team = team_1
        team_enem = team_2
    else:
        team = team_2
        team_enem = team_1
    print('team', [x.name for x in team])
    
    #--------choosing possible targets--------
    team_m_h = 0      #sum of missing health points of the team
    
    for y, ally in enumerate(team):
        m_h = ally.hp_max - ally.hp   #m_h = missing health points
        team_m_h += m_h
        print(f'{team_m_h=} {m_h=}')
        
        for magic in ST_heals:
            print(f'ST {magic.name} {magic.value_1=} {m_h + loss_toler=}')
            if magic.value_1 <= m_h + loss_toler:    #if value healed is less or equal to missing hp + loss tolerancy #ST rule 1
                psbl_heals[0].append(magic)
                psbl_heals[1].append(y)
    
    for magic in MT_heals:
        AT_m_h = 0
        for x in team:
            m_h = x.hp_max - x.hp
            print(f'{m_h=}', end=' ')
            if m_h > magic.value_1:
                print(magic.value_1)
                AT_m_h += magic.value_1
            else:
                print(m_h)
                AT_m_h += m_h
        AT_m_h = int(AT_m_h / len(team))
        print(f'{AT_m_h=}')
        
        print(f'MT {magic.name} {magic.value_1=} {(team_m_h + loss_toler) / len(team)=}')
        print(f'   {magic.value_1 / 2 + loss_toler=} {AT_m_h=}')
        if magic.value_1 <= (team_m_h + loss_toler) / len(team):       #MT rule 1
            if magic.value_1 / 2 + loss_toler > AT_m_h:                #MT rule 2
                psbl_heals[0].append(magic)
                psbl_heals[1].append(team)

    for magic in AT_heals:
        AT_m_h = 0
        for x in team:
            m_h = x.hp_max - x.hp
            print(f'{m_h=}', end=' ')
            if m_h > magic.value_1:
                print(magic.value_1)
                AT_m_h += magic.value_1
            else:
                print(m_h)
                AT_m_h += m_h
        AT_m_h = int(AT_m_h / len(team))
        print(f'{AT_m_h=}')
        
        print(f'AT {magic.name} {magic.value_1=} {(team_m_h + loss_toler) / len(team)=}')
        print(f'   {magic.value_1 / 2=} {AT_m_h=}')
        if magic.value_1 <= (team_m_h + loss_toler) / len(team):       #AT rule 1
            if magic.value_1 / 2 <= AT_m_h:                            #AT rule 2
                psbl_heals[0].append(magic)
                psbl_heals[1].append(team)
    
    print('psbl_heals[0]', [x.name for x in psbl_heals[0]])
    print('psbl_heals[1]', psbl_heals[1])
    
    #--------using magic--------
    if psbl_heals[0]:
        
        for magic, targ in zip(psbl_heals[0][::-1], psbl_heals[1][::-1]):
            print(f'{char.mana=}, {magic.m_cost=}')
            if char.mana >= magic.m_cost:                 #tweak this to make different versions of AI - PLACE FOR DIFFERENT VERSIONS
                AI_target = targ
                AI_secon = magic
                break
        else:                                 #if no magic can be used
            opt_atk = 1                   #allow use of attack
    else:
        opt_atk = 1
    
    #--------using attack if can't use magic--------
    print(f'{opt_atk=}')
    if opt_atk == 1:
        while True:                        #here AI_random is used - PLACE FOR DIFFERENT VERSIONS
            y = randint(0,len(team_enem)-1)                              #automatic choose of random target
            if team_1[y].hp == 0:
                continue                 #if chosen fighter is dead
            break
        AI_target = team_1[y]
    
    try:
        print(f'{AI_target=} {AI_secon.name=}')
    except:
        print(f'{AI_target=} {AI_secon=}')
    print('-----')
    pause()
    
    return AI_target, AI_secon