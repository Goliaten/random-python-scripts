def AI_mage_buff(char):
    AI_target, AI_secon = None, None
    buff_atk, buff_def = [], []
    debuff_atk, debuff_def = [], []
    psbl_buff = [[], []]
    psbl_debuff = [[], []]
    opt_atk = 0
    
    print(char.name, char.team)
    
    #----------ordering buff magic--------------
    for magic in char.magic:
        f_n = magic.fnc_name
        if 'buff' and 'atk' in f_n and 'debuff' not in f_n:
            buff_atk.append(magic)
        elif 'buff' and 'def' in f_n and 'debuff' not in f_n:
            buff_def.append(magic)
        elif 'debuff' and 'atk' in f_n:
            debuff_atk.append(magic)
        elif 'debuff' and 'def':
            debuff_def.append(magic)
            
    print('buff atk', [y.name for y in buff_atk], 'buff def', [y.name for y in buff_def])
    print('debuff atk', [y.name for y in debuff_atk], 'debuff def', [y.name for y in debuff_def], )
    
    #------getting team-------
    empty_team = []
    if char.team == 'team 1':
        team = team_1
        team_enem = team_2
    else:
        team = team_2
        team_enem = team_1
    print('team', [x.name for x in team], 'team_enem', [x.name for x in team_enem])
    
    #--------choosing possible targets--------
    #for more variety tweak these rules to make mage that buffs himself or others more
    print(f'{char.mana=} > {char.mana_max/2=} or {char.hp=} < {char.hp_max/2}') #  /-- PLACE FOR DIFFERENT VERSIONS
    if char.mana > char.mana_max / 2 or char.hp < char.hp_max / 2:             # <-----------character that conserves mana until situation is dire
        
        print('buff_def:')
        empty_team = [y for y in team]
        empty_team.sort(key=sortdef)
        print('empty_team:', [y.name for y in empty_team])
        for magic in buff_def:
            print(f' {magic.name}')
            for y, char in enumerate(empty_team):
                print(f'  {char.name}')
                #place for rules
                print(f'   {char.defence=} > 2')
                if char.defence > 2:                    # <--------buff defence rule 1
                    continue
                
                for eff in active_effects.values():
                    if eff.src == magic.spi and eff.char == char:  #if there is an effect made by the same magic on the same character
                        break
                else:
                    print('   chosen')
                    y = team.index(empty_team[y])
                    #place for rules
                    psbl_buff[0].append(magic)
                    psbl_buff[1].append(y)
        
        print('buff atk:')
        empty_team = [y for y in team]
        empty_team.sort(reverse=True, key=sortmaxatk)
        print('empty_team:', [y.name for y in empty_team])
        for magic in buff_atk:
            print(f' {magic.name}')
            for y, char in enumerate(empty_team):
                print(f'  {char.name}')
                print(f'   {char.atk=} > 13')
                if char.atk > 13:                    # <--------buff attack rule 1
                    continue
                
                for eff in active_effects.values():
                    if eff.src == magic.spi and eff.char == char:  #if there is an effect made by the same magic on the same character
                        break
                else:
                    print('   chosen')
                    y = team.index(empty_team[y])
                    psbl_buff[0].append(magic)
                    psbl_buff[1].append(y)
        
        print('debuff def')
        empty_team = [y for y in team_enem]
        empty_team.sort(reverse=True, key=sortdef)
        print('empty_team:', [y.name for y in empty_team])
        for magic in debuff_def:
            print(f' {magic.name}')
            for y, char in enumerate(empty_team):
                print(f'  {char.name}')
                print(f'   {char.defence=} < {magic.value_1=}')
                if char.defence < magic.value_1:                    # <--------debuff defence rule 1
                    continue
                
                for eff in active_effects.values():
                    if eff.src == magic.spi and eff.char == char:  #if there is an effect made by the same magic on the same character
                        break
                else:
                    print('   chosen')
                    y = team_enem.index(empty_team[y])
                    psbl_debuff[0].append(magic)
                    psbl_debuff[1].append(y)
        
        print('debuff atk')
        empty_team = [y for y in team_enem]
        empty_team.sort(reverse=True, key=sortmaxatk)
        print('empty_team:', [y.name for y in empty_team])
        for magic in debuff_atk:
            print(f' {magic.name}')
            for y, char in enumerate(empty_team):
                print(f'  {char.name}')
                print(f'   {char.atk=} < {magic.value_1*1.5=}')
                if char.atk < magic.value_1 * 1.5:                    # <--------debuff attack rule 1
                    continue
                
                for eff in active_effects.values():
                    if eff.src == magic.spi and eff.char == char:  #if there is an effect made by the same magic on the same character
                        break
                else:
                    print('   chosen')
                    y = team_enem.index(empty_team[y])
                    psbl_debuff[0].append(magic)
                    psbl_debuff[1].append(y)
                    
                    
#trying to compare [char, magic.spi] to something from active effects, so that same effect won't affect a creature twice at the same time
    

    #--------using magic--------
    psbl_mag = [psbl_buff[0] + psbl_debuff[0], psbl_buff[1] + psbl_debuff[1]]       #swap for debuff focused mage - PLACE FOR DIFFERENT VERSIONS
    
    print('psbl_mag[0]:', [x.name for x in psbl_mag[0]])
    print('psbl_mag[1]:', psbl_mag[1])
    
    if psbl_mag[0]:
        for magic, targ in zip(psbl_mag[0], psbl_mag[1]):
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
    if opt_atk == 1:
        while True:                        #here AI_random is used - PLACE FOR DIFFERENT VERSIONS
            y = randint(0, len(team_1)-1)                              #automatic choose of random target
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