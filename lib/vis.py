typea = ['ETMX','ETMY','ITMX','ITMY']
typeb = ['SRM','SR2','SR3','BS']
typebp = ['PRM','PR2','PR3']
typeci = ['MCI','MCO','MCE','IMMT1','IMMT2']
typeco = ['OSTM','OMMT1','OMMT2']
suspensions = typea + typeb + typebp + typeci + typeco
               
stages = ['IP','GAS','BF','MN','IM']
states = ['SAFE','STANDBY','ISOLATED','DAMPED','ALIGNED','TWRFLOAT','PAYFLOAT']
refs = ['00','01','02','03','04']
ansnums = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14']

susdict = {'TYPE-A':typea,
           'TYPE-B':typeb,
           'TYPE-Bp':typebp,
           'TYPE-Ci':typeci,
           'TYPE-Co':typeco}

key2dict = {'SUS':suspensions,'STG':stages,
            'STS':states,'REF':refs,
            'ANS':ansnums}
key2dict = {'SUS':refs,'STG':refs,
            'STS':refs,'REF':refs,
            'TYP':refs,
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
        return 'TYPE-Bp'
    elif sus in typeci:
        return 'TYPE-Ci'
    elif sus in typeco:
        return 'TYPE-Co'
    else:
        raise ValueError('Invalid %s'%(sus))
    
def get_sustype(suslist):
    return [ _sustype_is(sus) for sus in suslist]

def get_suslist_belong_sustype(suslist,typlist): # fix me
    _suslist = [sus for typ in typlist for sus in susdict[typ]]    
    if suslist and _suslist:
        _susset = set(_suslist)
        susset = set(suslist)
        union = _susset & susset
        return union
    elif suslist and not _suslist:
        return suslist
    elif not suslist and _suslist:
        return _suslist
    elif not suslist and not _suslist:
        return []
    else:
        raise ValueError('A')
    

