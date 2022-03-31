#!/usr/bin/env python
import numpy as np
from pcaspy import Driver, SimpleServer
import random

from search import search

from db import pvdb
from db import select_bit_fmt,select_val_fmt,ans_fmt
from vis import suspensions,stages,states,sustypes
from vis import key2dict,get_read,get_sustype
from vis import get_suslist_belong_sustype, get_stglist_belong_sus
from vis import get_stslist, get_exclist
from vis import key1s

from atmplot import plot

prefix = 'K1:'

class RunError(Exception):
    pass

def is_pushed(self,key1,key2):
    # 4 で割った余りは直したい。
    return self.getParam(select_bit_fmt.format(key1=key1,key2=key2))%4 # fixme

def _get_pushed(self,key1,key2): # Fix me
    '''
    FIX ME
    REFの場合、番号はチャンネル名として用意できないので、_VALを使用しているが、
    他のSUSやSTGなどはあらかじめ用意しているため、_VALが必要ない。この違いの
    せいで、ifを書く必要が生じたが、SUSとかもREF方式にしたらいい気がする。将来
    サスペンションやステージが増える可能性があると思えば、そうしてもいい気
    がする。
    '''
    if not key1 in ['ANS']:
        return str(self.getParam(select_val_fmt.format(key1=key1,key2=key2)))
    elif key1 in ['ANS']:
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
    for i in range(6)[::-1]:
        if i==0:
            self.setParam('ATM-VIS_NOTIFY_00',message)
        else:
            _oldmessage = self.getParam('ATM-VIS_NOTIFY_%02d'%(i-1))
            self.setParam('ATM-VIS_NOTIFY_%02d'%(i),_oldmessage)

def set_all_val(self,key1,vals):
    for key2,val in zip(key2dict[key1],vals):
        self.setParam(select_val_fmt.format(key1=key1,key2=key2),str(val))

def set_all_ans(self,key1,vals):
    for key2,val in zip(key2dict['ANS'],vals):
        self.setParam(ans_fmt.format(key1=key1,key2=key2),str(val))        
        
def update_ans(self,ans):
    if not isinstance(ans,np.ndarray):
        raise RunError('invalid type. %s'%(type(ans)))
    if not ans.shape[1]==6:
        raise RunError('ans should have 6 cols: sus,sts,stg,exc,dof,ref.')

    
    num = min(15,ans.shape[0])                    
                
    # update reflist
    suslist = ans[:,0]
    set_all_val(self,'SUS',['---']*15)
    typlist = get_pushed_list(self,'TYP')
    suslist = get_suslist_belong_sustype(list(np.unique(suslist)),typlist)
    set_all_val(self,'SUS',np.unique(suslist)[::-1])
    typlist = get_sustype(suslist)
    set_all_val(self,'TYP',['---']*15)
    #set_all_val(self,'TYP',np.unique(typlist)[::-1])
    set_all_val(self,'TYP',sustypes)        
    #stslist = ans[:,1]
    stslist = get_stslist()
    set_all_val(self,'STS',['---']*15)
    set_all_val(self,'STS',np.unique(stslist)[::-1])            
    #stglist = ans[:,2]
    stglist = get_stglist_belong_sus(list(np.unique(suslist)))
    set_all_val(self,'STG',['---']*15)
    set_all_val(self,'STG',np.unique(stglist)[::-1])
    #exclist = ans[:,3]
    exclist = get_exclist()
    set_all_val(self,'EXC',['---']*15)
    set_all_val(self,'EXC',np.unique(exclist)[::-1])        
    reflist = ans[:,5]
    set_all_val(self,'REF',['---']*15)
    set_all_val(self,'REF',np.unique(reflist)[::-1])    

    # init answers
    set_all_ans(self,'SUS',['---']*15)
    set_all_ans(self,'STG',['---']*15)
    set_all_ans(self,'STS',['---']*15)
    set_all_ans(self,'EXC',['---']*15)
    set_all_ans(self,'DOF',['---']*15)
    set_all_ans(self,'REF',['---']*15)    
    
    # write answers
    set_all_ans(self,'SUS',ans[:,0])
    set_all_ans(self,'STS',ans[:,1])
    set_all_ans(self,'STG',ans[:,2])    
    set_all_ans(self,'EXC',ans[:,3])
    set_all_ans(self,'DOF',ans[:,4])
    set_all_ans(self,'REF',ans[:,5])    

def get_plot_params(suslist,stglist,stslist,exclist,doflist,reflist):
        
    
    
def make_plot(self):
    pushed_ans = get_pushed_list(self,'ANS')
    suslist = get_pushed_ans_list(self,'SUS',pushed_ans)
    stglist = get_pushed_ans_list(self,'STG',pushed_ans)
    stslist = get_pushed_ans_list(self,'STS',pushed_ans)
    exclist = get_pushed_ans_list(self,'EXC',pushed_ans)
    doflist = get_pushed_ans_list(self,'DOF',pushed_ans)
    reflist = get_pushed_ans_list(self,'REF',pushed_ans)

    # 同じ stage, grdstate, excitation, doflist でPlotする
    # suslist, reflist は複数選択して比較Plot可能
    if len(stglist)*len(stslist)*len(exclist)*len(doflist)==1:
        stg,sts = list(stglist)[0],list(stslist)[0]
        exc,ref = list(exclist)[0],list(reflist)
        suslist = list(suslist)
        excdofs = [ dof for dof in list(doflist)[0].split(" ") if not ''==dof] #fixme
        print('plot',suslist,stg,sts,exc,ref,excdof)
        
        # fixme: choose read point name by excitation point name
        read = get_read(stg,exc)
        
        # Plot each dofs
        for dof in excdofs:
            ch_from = '%s_%s_%s'%(stg,exc,dof)
            # fix me ----------------------
            if stg=='TM':
                readdofs = ['L','P','Y']
            else:
                readdofs = excdofs
            # fix me ----------------------
            for readdof in readdofs:
                ch_to = '%s_%s_%s'%(stg,read,readdof)
                print('Plot',suslist,ch_from,ch_to,ref,sts)
                figname = plot(suslist,ch_from,ch_to,ref,sts)
                notify(self,figname)
    else:
        # stage, grdstate, excitation, dof list, が複数選択された
        # 場合、Plotしない。
        notify(self,'can not plot.')
        print('Can not plot.')

# ------------------------------------------------------------------------------
        
def blink_select_button(self,reason):
    key1,key2 = reason.split('_')[-2:]
    self.setParam(
        select_bit_fmt.format(key1=key1,key2=key2),
        self.getParam(select_bit_fmt.format(key1=key1,key2=key2)) + 2
    )

def get_search_with_selected_items(self):
    typlist = get_pushed_list(self,'TYP')
    suslist = get_pushed_list(self,'SUS')
    if not typlist and suslist:
        pass
    elif not typlist and not suslist:
        pass
    elif typlist and not suslist:
        suslist = get_suslist_belong_sustype(suslist,typlist)
    elif typlist and suslist:
        pass
    else:
        raise ValueError('A')
        
    return search(sus=suslist,
                  stg=get_pushed_list(self,'STG'),
                  sts=get_pushed_list(self,'STS'),
                  exc=get_pushed_list(self,'EXC'),
                  ref=get_pushed_list(self,'REF'))    


def find_refs(self,reason,findkey): # fixme
    key1 = reason.split('_')[-1]
    if not key1=='TYP':
        key1num = key1s.index(key1)
        refs = get_search_with_selected_items(self)[:,key1num]
        refs = [ ref for ref in refs if findkey in ref]
        set_all_val(self,key1,['---']*15)
        set_all_val(self,key1,np.unique(refs)[::-1])

class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()
        ans = get_search_with_selected_items(self)
        update_ans(self,ans)                    

    def write(self, reason, value):
        #notify(self,'')                    
        if 'ATM-VIS_PLOT' in reason:
            make_plot(self)
        elif 'ATM-VIS_SELECT_FIND' in reason:
            find_refs(self,reason,value)
            self.setParam(reason,value)
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
