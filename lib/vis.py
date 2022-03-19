typea = ['ETMX','ETMY','ITMX','ITMY']
typeb = ['SRM','SR2','SR3','BS']
typebp = ['PRM','PR2','PR3']
typeci = ['MCI','MCO','MCE','IMMT1','IMMT2']
typeco = ['OSTM','OMMT1','OMMT2']
suspensions = typea + typeb + typebp + typeci + typeco
sustypes = ['TYPE-A','TYPE-B','TYPE-BP','TYPE-CI','TYPE-CO']
stages = ['IP','GAS','BF','MN','IM']
states = ['SAFE','STANDBY','ISOLATED','DAMPED','ALIGNED','TWRFLOAT','PAYFLOAT']
excites = ['TEST','COILOUTF']
refs = ['00','01','02','03','04','05','06','07','08','09']
ansnums = ['00','01','02','03','04','05','06','07','08','09']
key1s = ['SUS','STS','STG','EXC','DOFS','REF']
class VisError(Exception):
    pass

vis_dofs = {
    'TYPE-A': {'IP':['L','T','Y'],
               'GAS':['F0','F1','F2','F3','BF'],
               'BF':['L','T','V','P','Y','R'],
               'MN':['L','T','V','P','Y','R'],
               'IM':['L','T','V','P','Y','R'],
               'TM':['L','P','Y']},        
    'TYPE-B': {'IP':['L','T','Y'],
               'GAS':['F0','F1','BF'],
               'IM':['L','T','V','P','Y','R'],
               'TM':['L','P','Y']},        
    'TYPE-BP': {'GAS':['SF','BF'],
                'BF':['L','T','V','P','Y','R'],
                'IM':['L','T','V','P','Y','R'],
                'TM':['L','P','Y']},    
    'TYPE-CI': {'TM':['L','P','Y']},
    'TYPE-CO': {'TM':['L','P','Y']}
}

def get_dofs(sus,stg):
    try:
        return vis_dofs[_sustype_is(sus)][stg]
    except KeyError as e:
        return []
    except:
        raise VisError('{sus} does not have {stg}.'.format(sus=sus,stg=stg))

susdict = {'TYPE-A':typea,
           'TYPE-B':typeb,
           'TYPE-BP':typebp,
           'TYPE-CI':typeci,
           'TYPE-CO':typeco}

key2dict = {'SUS':refs,'STG':refs,
            'STS':refs,'REF':refs,
            'TYP':refs,'EXC':refs,'DOF':refs,
            'ANS':ansnums}

read_dict = {
    'IP':['IDAMP','LVDTINF','BLEND_ACC','BLEND_LVDT'],
    'BF':['DAMP','LVDTINF'],
    'GAS':['DAMP','LVDTINF'],
    'MN':['DAMP','OSEMINF'],
    'IM':['DAMP','OSEMINF']
}

def _sustype_is(sus):
    if sus in typea:
        return 'TYPE-A'
    elif sus in typeb:
        return 'TYPE-B'
    elif sus in typebp:
        return 'TYPE-BP'
    elif sus in typeci:
        return 'TYPE-CI'
    elif sus in typeco:
        return 'TYPE-CO'
    else:
        raise ValueError('Invalid %s'%(sus))
    
def get_sustype(suslist):
    return [ _sustype_is(sus) for sus in suslist]

def _get_correct_typlist(typlist):
    return [ typ for typ in typlist if typ in sustypes]        

def _get_correct_suslist(suslist):
    return [ sus for sus in suslist if sus in suspensions]        

def _get_correct_stglist(stglist):
    return [ stg for stg in stglist if stg in stages]        

def _get_correct_stslist(stslist):
    return [ sts for sts in stslist if sts in states]        

def get_suslist_belong_sustype(suslist,typlist): # fix me
    typlist = _get_correct_typlist(typlist)
    _suslist = [sus for typ in typlist for sus in susdict[typ]]
    print(suslist,_suslist)
    if suslist and _suslist:
        _susset = set(_suslist)
        susset = set(suslist)
        union = _susset & susset
        print('!!!')        
        return _suslist
    #return list(union)
    elif suslist and not _suslist:
        return suslist
    elif not suslist and _suslist:
        return _suslist
    elif not suslist and not _suslist:
        return []
    else:
        raise ValueError('A')
    
def get_stglist_belong_sus(suslist): # fix me
    stglist = stages
    return stglist

def get_stslist(): # fix me
    return states

def get_exclist(): # fix me
    return excites
