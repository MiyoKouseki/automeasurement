import re
import settings
import itertools
from vis import suspensions,stages,states,key2dict

key1s = ['SUS','STS','STG','EXC','DOFS','REF'] # 順番が大事

pvdb = {'HOGE':{'type':'float'}}

# SELECT
select_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}'
select_ptrn = 'ATM-VIS_SELECT_BUTTON_([A-Z0-9]+)_([A-Z0-9]+)'
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

def get_key1_key2(channel):
    key1,key2 = re.findall(select_ptrn,channel)[0]
    return key1,key2
    
# ---------------------------------------------------
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
        

pvdb.update({'ATM-VIS_SEARCH':{'type':'str'}})
pvdb.update({'ATM-VIS_PLOT':{'type':'str'}})
pvdb.update({'ATM-VIS_MEASURE':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_00':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_01':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_02':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_03':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_04':{'type':'str'}})
pvdb.update({'ATM-VIS_NOTIFY_05':{'type':'str'}})

