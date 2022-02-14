import itertools
from vis import suspensions,stages,states,key2dict

refnum_fmt = 'ATM-VIS_{sus}_{stg}_{sts}_REFNUM'
refnum_fmt_sdf_dummy = 'VIS-{sus}_{stg}_{sts}_REFNUM'

params = list(itertools.product(suspensions,stages,states))
pvdb = {refnum_fmt.format(sus=sus,stg=stg,sts=sts):
        {'type':'float','value':0} for sus,stg,sts in params}
pvdb.update({refnum_fmt_sdf_dummy.format(sus=sus,stg=stg,sts=sts):
             {'type':'float','value':0} for sus,stg,sts in params})

list_fmt = 'ATM-VIS_SELECT_LIST_{key1}'
select_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}'
select_bit_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}_BIT'
for key1 in ['SUS','STG','STS','REF']:
    pvdb.update({list_fmt.format(key1=key1):{'type':'str'}})
    pvdb.update({select_fmt.format(key1=key1,key2=key2):
                 {'type':'int','value':0} for key2 in key2dict[key1]})
    pvdb.update({select_bit_fmt.format(key1=key1,key2=key2):
                 {'type':'int','value':0} for key2 in key2dict[key1]})
    
    if 'REF'==key1: # fixme
        pvdb.update({'ATM-VIS_SELECT_BUTTON_{key1}_{key2}_VAL'.format(key1=key1,key2=key2):
                     {'type':'float',
                      'value':0} for key2 in key2dict[key1]})

pvdb.update({'HOGE':{'type':'float'}})
pvdb.update({'ATM-VIS_SEARCH':{'type':'str'}})

