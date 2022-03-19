import settings
import itertools
from vis import suspensions,stages,states,key2dict

# STATUS
refnum_fmt = 'ATM-VIS_{sus}_{stg}_{sts}_REFNUM'
refnum_fmt_sdf_dummy = 'VIS-{sus}_{stg}_{sts}_REFNUM'
params = list(itertools.product(suspensions,stages,states))
pvdb = {refnum_fmt.format(sus=sus,stg=stg,sts=sts):
        {'type':'float','value':0} for sus,stg,sts in params}
pvdb.update(
    {
        refnum_fmt_sdf_dummy.format(sus=sus,stg=stg,sts=sts):
        {'type':'float','value':0}
        for sus,stg,sts in params
    }
)

# SELECT
select_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}'
select_bit_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}_BIT'
select_val_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}_VAL'
select_find_fmt = 'ATM-VIS_SELECT_FIND_{key1}'
default_val = {'SUS':'','STG':'','STS':'','REF':'2022',
               'ANS':'',
               'TYP':'TYPE-A','EXC':'TEST'}
for key1 in ['SUS','STG','STS','REF','ANS','TYP','EXC']:
    pvdb.update(
        {
            select_find_fmt.format(key1=key1):
            {'type':'str','value':default_val[key1]}
        }
    )    
    pvdb.update(
        {
            select_fmt.format(key1=key1,key2=key2):
            {'type':'int','value':0}
            for key2 in key2dict[key1]
        }
    )
    pvdb.update(
        {
            select_bit_fmt.format(key1=key1,key2=key2):
            {'type':'int','value':0}
            for key2 in key2dict[key1]
        }
    )
    pvdb.update(
        {
            select_val_fmt.format(key1=key1,key2=key2):
            {'type':'str','value':'---'}
            for key2 in key2dict[key1]
        }
    )

# ANS
ans_fmt = 'ATM-VIS_ANS_{key2}_{key1}'
for key1 in ['SUS','STG','STS','EXC','DOF','REF']:
    pvdb.update(
        {
            ans_fmt.format(key2=key2,key1=key1):
            {'type':'str','value':'---'}
            for key2 in key2dict['ANS']
        }
    )
        
pvdb.update({'HOGE':{'type':'float'}})
pvdb.update({'ATM-VIS_SEARCH':{'type':'str'}})
pvdb.update({'ATM-VIS_PLOT':{'type':'str'}})
pvdb.update({'ATM-VIS_MEASURE':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_00':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_01':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_02':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_03':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_04':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_05':{'type':'str'}})

