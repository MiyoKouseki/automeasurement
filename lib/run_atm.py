import subprocess
import datetime
import os

os.environ['EPICS_CA_ADDR_LIST'] = '172.20.0.2'

import ezca as _ezca
ezca = _ezca.Ezca()
if not ezca.prefix=='K1:':
    ezca = _ezca.Ezca('K1:')
print(ezca.prefix)

from db import select_bit_fmt,select_val_fmt
from vis import key2dict
from run import get_pushed_list

select_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}'
select_bit_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}_BIT'
select_val_fmt = 'ATM-VIS_SELECT_BUTTON_{key1}_{key2}_VAL'
select_find_fmt = 'ATM-VIS_SELECT_FIND_{key1}'

class Dummy():
    def __init__(self):
        pass
    def getParam(self,chname):
        return ezca[chname.replace('K1','')]        

    def setParam(self,chname,val):    
        ret = ezca[chname.replace('K1','')] = val            
        return ret    

def get_refnum():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%H%M')


def hoge(suslist,stglist,exclist,**kawrgs):
    cmd = 'python3 manage.py --sus {sus} --stg {stg} --exc {exc}'.\
        format(sus=' '.join(suslist),stg=' '.join(stglist),exc=' '.join(exclist)) 
    ret = subprocess.run(cmd,shell=True,check=True)
    print(cmd)
    

if __name__=="__main__":
    pcas = Dummy()
    suslist = get_pushed_list(pcas,'SUS')
    stglist = get_pushed_list(pcas,'STG')
    exclist = get_pushed_list(pcas,'EXC')
    reflist = [get_refnum()]
    print(suslist,stglist,exclist)
    if input('Are you sure? [y/n]')=='y':
        hoge(suslist,stglist,exclist)
    else:
        print('abort')
