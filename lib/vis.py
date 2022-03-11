typea = ['ETMX','ETMY','ITMX','ITMY']
typeb = ['SRM','SR2','SR3','BS']
typebp = ['PRM','PR2','PR3']
typeci = ['MCI','MCO','MCE','IMMT1','IMMT2']
typeco = ['OSTM','OMMT1','OMMT2']
suspensions = typea + typeb + typebp + typeci + typeco
sustypes = ['TYPE-A','TYPE-B','TYPE-BP','TYPE-CI','TYPE-CO']
stages = ['IP','GAS','BF','MN','IM']
states = ['SAFE','STANDBY','ISOLATED','DAMPED','ALIGNED','TWRFLOAT','PAYFLOAT']
refs = ['00','01','02','03','04']
ansnums = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14']

susdict = {'TYPE-A':typea,
           'TYPE-B':typeb,
           'TYPE-BP':typebp,
           'TYPE-CI':typeci,
           'TYPE-CO':typeco}

key2dict = {'SUS':refs,'STG':refs,
            'STS':refs,'REF':refs,
            'TYP':refs,'EXC':refs,
            'ANS':ansnums}

read_dict = {
    'IP':['IDAMP','BLEND_ACC','BLEND_LVDT'],
    'BF':['DAMP'],
    'GAS':['DAMP'],
    'MN':['DAMP'],
    'IM':['DAMP']
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
    

