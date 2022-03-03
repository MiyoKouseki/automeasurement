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

class RunError(Exception):
    pass

def is_pushed(self,key1,key2):
    # 4 で割った余りは直したい。
    return self.getParam(select_bit_fmt.format(key1,key2))%4 # fixme

def get_pushed(self,key1,key2): # Fix me
    '''
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
        get_pushed(self,key1,key2) for key2 in key2dict[key1]
        if is_pushed(self,key1,key2)
    ]
    return _list

def set_selected_items(self,key1):
    _list = get_pushed_list(self,key1)
    self.setParam('ATM-VIS_SELECT_LIST_{key1}'.format(key1=key1),' '.join(_list))    
    return _list

def hoge(self,ans):
    #
    try:
        num = min(10,ans.shape[0])                
    except:
        num = 10
        ans = np.array(['---']*10*6).reshape(10,6)
                
    # update reflist
    reflist = ans[:,-1]
    [self.setParam(select_val_fmt.format(key2=key2),
                   str(val)) for key2,val in zip(key2dict['REF'],['---']*10)]
    [self.setParam(select_val_fmt.format(key2=key2),
                   str(val)) for key2,val in zip(key2dict['REF'],np.unique(reflist))]

    # init answers
    [self.setParam(ans_fmt.format(key2=key2,key1='SUS'),
                   str('---')) for key2 in key2dict['ANS']]
    [self.setParam(ans_fmt.format(key2=key2,key1='STS'),
                   str('---')) for key2 in key2dict['ANS']]
    [self.setParam(ans_fmt.format(key2=key2,key1='STG'),
                   str('---')) for key2 in key2dict['ANS']]
    [self.setParam(ans_fmt.format(key2=key2,key1='EXC'),
                   str('---')) for key2 in key2dict['ANS']]
    [self.setParam(ans_fmt.format(key2=key2,key1='DOF'),
                   str('---')) for key2 in key2dict['ANS']]
    [self.setParam(ans_fmt.format(key2=key2,key1='REF'),
                   str('---')) for key2 in key2dict['ANS']]

    # write answers
    [self.setParam(ans_fmt.format(key2=key2,key1='SUS'),str(ans[i][0]))
     for i,key2 in enumerate(key2dict['ANS'][:num])]
    [self.setParam(ans_fmt.format(key2=key2,key1='STS'),str(ans[i][1]))
     for i,key2 in enumerate(key2dict['ANS'][:num])]
    [self.setParam(ans_fmt.format(key2=key2,key1='STG'),str(ans[i][2]))
     for i,key2 in enumerate(key2dict['ANS'][:num])]
    [self.setParam(ans_fmt.format(key2=key2,key1='EXC'),str(ans[i][3]))
     for i,key2 in enumerate(key2dict['ANS'][:num])]
    [self.setParam(ans_fmt.format(key2=key2,key1='DOF'),str(ans[i][4]))
     for i,key2 in enumerate(key2dict['ANS'][:num])]
    [self.setParam(ans_fmt.format(key2=key2,key1='REF'),str(ans[i][5]))
     for i,key2 in enumerate(key2dict['ANS'][:num])]

def get_pushed_ans_list(self,key1,ansnum):
    _list = [self.getParam(ans_fmt.format(key2=key2,key1=key1))
             for key2 in ansnum]
    return set(_list)


def make_plot(self):
    pushed_ans = get_pushed_list(self,'ANS')            
    suslist = get_pushed_ans_list(self,'SUS',pushed_ans)
    stglist = get_pushed_ans_list(self,'STG',pushed_ans)
    stslist = get_pushed_ans_list(self,'STS',pushed_ans)
    exclist = get_pushed_ans_list(self,'EXC',pushed_ans)
    doflist = get_pushed_ans_list(self,'DOF',pushed_ans)
    reflist = get_pushed_ans_list(self,'REF',pushed_ans)

    if len(stglist)*len(stslist)*len(exclist)*len(doflist)==1:
        suslist,stg,sts,exc,ref = list(suslist),list(stglist)[0],list(stslist)[0],list(exclist)[0],list(reflist)
        read = read_dict[stg][0] # fix me
        dofs = [ dof for dof in list(doflist)[0].split(" ") if not ''==dof]
        print(dofs)
        for dof in dofs:
            ch_from = '%s_%s_%s'%(stg,exc,dof)
            ch_to = '%s_%s_%s'%(stg,read,dof)
            print(suslist,ch_from,ch_to,ref,sts)            
            plot(suslist,ch_from,ch_to,ref,sts)            
    else:
        print('Can not compair.')
    
    
class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()
        self.tid = None

    def write(self, reason, value):
        status = True
        
        self.setParam(reason, value)
        if 'ATM-VIS_PLOT' in reason:            
            make_plot(self)
            
        if 'ATM-VIS_SEARCH' in reason:
            suslist = self.getParam('ATM-VIS_SELECT_LIST_SUS')
            stglist = self.getParam('ATM-VIS_SELECT_LIST_STG')
            stslist = self.getParam('ATM-VIS_SELECT_LIST_STS')
        elif 'ATM-VIS_SELECT' in reason:
            # SELECT_BUTTON
            key1,key2 = reason.split('_')[-2:]
            _val = self.getParam(select_bit_fmt.format(key1,key2))
            self.setParam(select_bit_fmt.format(key1,key2),_val+2)
            
            # push されているボタンのリストを取得
            suslist = set_selected_items(self,'SUS')
            stglist = set_selected_items(self,'STG')
            stslist = set_selected_items(self,'STS')
            reflist = set_selected_items(self,'REF')
            kwargs = {'sus':suslist, 'stg':stglist, 'sts':stslist, 'ref':reflist}
            
            ans = search(**kwargs)
            hoge(self,ans)
            
        else:
            pass
        
        self.updatePVs()        
        return True


if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)
