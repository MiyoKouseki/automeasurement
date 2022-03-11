#!/usr/bin/env python
import numpy as np
from pcaspy import Driver, SimpleServer
import random

from search import search

from db import pvdb
from vis import suspensions,stages,states,key2dict,read_dict

from atmplot import plot

prefix = 'K1:'

select_bit_fmt = 'ATM-VIS_SELECT_BUTTON_{0}_{1}_BIT'
select_val_fmt = 'ATM-VIS_SELECT_BUTTON_REF_{key2}_VAL'
ans_fmt = 'ATM-VIS_ANS_{key2}_{key1}'
select_list = 'ATM-VIS_SELECT_LIST_{key1}'

class RunError(Exception):
    pass

def is_pushed(self,key1,key2):
    # 4 で割った余りは直したい。
    return self.getParam(select_bit_fmt.format(key1,key2))%4 # fixme

def _get_pushed(self,key1,key2): # Fix me
    '''
    FIX ME
    REFの場合、番号はチャンネル名として用意できないので、_VALを使用しているが、
    他のSUSやSTGなどはあらかじめ用意しているため、_VALが必要ない。この違いの
    せいで、ifを書く必要が生じたが、SUSとかもREF方式にしたらいい気がする。将来
    サスペンションやステージが増える可能性があると思えば、そうしてもいい気
    がする。
    '''
    if key1 in ['REF']:
        return str(self.getParam(select_val_fmt.format(key2=key2)))
    elif key1 in ['SUS','STG','STS','ANS']:
        return key2
    else:
        raise RunError(key1,key2)

def get_pushed_list(self,key1):
    _list = [
        _get_pushed(self,key1,key2)
        for key2 in key2dict[key1]
        if is_pushed(self,key1,key2)
    ]
    return _list

def get_pushed_ans_list(self,key1,ansnum):
    _list = [
        self.getParam(ans_fmt.format(key2=key2,key1=key1))
        for key2 in ansnum
    ]
    return set(_list)

def notify(self,message):
    self.setParam('ATM-VIS_NOTIFY_01',message)

def set_all_val(self,key1,vals):
    for key2,val in zip(key2dict[key1],vals):
        self.setParam(select_val_fmt.format(key2=key2),str(val))

def set_all_ans(self,key1,vals):
    for key2,val in zip(key2dict['ANS'],vals):
        self.setParam(ans_fmt.format(key1=key1,key2=key2),str(val))
        
def update_ans(self,ans):
    if not isinstance(ans,np.ndarray):
        raise RunError('invalid type. %s'%(type(ans)))
    if not ans.shape[1]==6:
        raise RunError('ans should have 6 cols: sus,sts,stg,exc,dof,ref.')

    num = min(10,ans.shape[0])                    
                
    # update reflist
    reflist = ans[:,5]
    set_all_val(self,'REF',['---']*10)
    set_all_val(self,'REF',np.unique(reflist)[::-1])    

    # init answers
    set_all_ans(self,'SUS',['---']*10)
    set_all_ans(self,'STG',['---']*10)
    set_all_ans(self,'STS',['---']*10)
    set_all_ans(self,'EXC',['---']*10)
    set_all_ans(self,'DOF',['---']*10)
    set_all_ans(self,'REF',['---']*10)    
    
    # write answers
    set_all_ans(self,'SUS',ans[:,0])
    set_all_ans(self,'STS',ans[:,1])
    set_all_ans(self,'STG',ans[:,2])    
    set_all_ans(self,'EXC',ans[:,3])
    set_all_ans(self,'DOF',ans[:,4])
    set_all_ans(self,'REF',ans[:,5])    
    
def make_plot(self):
    pushed_ans = get_pushed_list(self,'ANS')            
    suslist = get_pushed_ans_list(self,'SUS',pushed_ans)
    stglist = get_pushed_ans_list(self,'STG',pushed_ans)
    stslist = get_pushed_ans_list(self,'STS',pushed_ans)
    exclist = get_pushed_ans_list(self,'EXC',pushed_ans)
    doflist = get_pushed_ans_list(self,'DOF',pushed_ans)
    reflist = get_pushed_ans_list(self,'REF',pushed_ans)

    if len(stglist)*len(stslist)*len(exclist)*len(doflist)==1:
        stg,sts = list(stglist)[0],list(stslist)[0]
        exc,ref = list(exclist)[0],list(reflist)
        suslist = list(suslist)
        if not stg=='---':
            read = read_dict[stg][0] # fix me
        else:
            notify(self,'can not plot.')            
            return None
        dofs = [ dof for dof in list(doflist)[0].split(" ")
                 if not ''==dof]
        print(dofs)
        for dof in dofs:
            ch_from = '%s_%s_%s'%(stg,exc,dof)
            ch_to = '%s_%s_%s'%(stg,read,dof)
            print(suslist,ch_from,ch_to,ref,sts)            
            plot(suslist,ch_from,ch_to,ref,sts)            
    else:
        notify(self,'can not plot.')
        print('Can not compair.')
    
def blink_select_button(self,reason):
    key1,key2 = reason.split('_')[-2:]
    self.setParam(
        select_bit_fmt.format(key1,key2),
        self.getParam(select_bit_fmt.format(key1,key2)) + 2
    )

def get_search_with_selected_items(self):
    return search(sus=get_pushed_list(self,'SUS'),
                  stg=get_pushed_list(self,'STG'),
                  sts=get_pushed_list(self,'STS'),
                  ref=get_pushed_list(self,'REF'))    
        
class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()

    def write(self, reason, value):
        notify(self,'')                    
        if 'ATM-VIS_PLOT' in reason:
            make_plot(self)            
        elif 'ATM-VIS_SELECT_BUTTON' in reason:
            blink_select_button(self,reason)            
            ans = get_search_with_selected_items(self)
            update_ans(self,ans)            
        else:
            pass
        
        self.updatePVs()        
        return True

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()
    while True:
        server.process(0.1)
