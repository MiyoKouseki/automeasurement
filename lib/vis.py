typea = ['ETMX','ETMY','ITMX','ITMY']
typeb = ['SRM','SR2','SR3','BS']
typebp = ['PRM','PR2','PR3']
typeci = ['MCI','MCO','MCE','IMMT1','IMMT2']
typeco = ['OSTM','OMMT1','OMMT2']
suspensions = typea + typeb + typebp + typeci + typeco
               
stages = ['IP','GAS','BF','MN','IM']
states = ['SAFE','STANDBY','ISOLATED','DAMPED','ALIGNED','TWRFLOAT','PAYFLOAT']
refs = ['00','01','02','03','04','05','06','07','08','09']
ansnums = ['00','01','02','03','04','05','06','07','08','09']

key2dict = {'SUS':suspensions,'STG':stages,
            'STS':states,'REF':refs,
            'ANS':ansnums}

read_dict = {
    'IP':['IDAMP','BLEND_ACC','BLEND_LVDT'],
    'BF':['DAMP'],
    'GAS':['DAMP'],
    'MN':['DAMP'],
    'IM':['DAMP']
}
