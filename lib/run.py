#!/usr/bin/env python
import numpy as np
from pcaspy import Driver, SimpleServer
import random

from search import search

from db import pvdb
from vis import suspensions,stages,states,key2dict

from atmplot import plot

prefix = 'K1:'

def is_pushed(self,key1,key2):
    return self.getParam('ATM-VIS_SELECT_BUTTON_{0}_{1}_BIT'.format(key1,key2))%4

def get_pushed_list(self,key1):
    '''
    '''
    if key1=='REF': 
        _list = [ self.getParam('ATM-VIS_SELECT_BUTTON_REF_{key2}_VAL'.format(key2=key2)) for key2 in key2dict[key1] if is_pushed(self,key1,key2)]
        _list = list(map(str,_list))
    else:
        _list = [ key2 for key2 in key2dict[key1] if is_pushed(self,key1,key2)]    
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
    [self.setParam('ATM-VIS_SELECT_BUTTON_REF_{0:02d}_VAL'.format(i),
                   str(val)) for i,val in zip(range(10),['---']*10)]
    [self.setParam('ATM-VIS_SELECT_BUTTON_REF_{0:02d}_VAL'.format(i),
                   str(val)) for i,val in zip(range(10),np.unique(reflist))]
    # init answers 
    [self.setParam('ATM-VIS_ANS_{0:02d}_SUS'.format(i),
                   str('---')) for i in range(10)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_STS'.format(i),
                   str('---')) for i in range(10)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_STG'.format(i),
                   str('---')) for i in range(10)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_EXC'.format(i),
                   str('---')) for i in range(10)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_DOF'.format(i),
                   str('---')) for i in range(10)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_REF'.format(i),
                   str('---')) for i in range(10)]        
    # write answers
    [self.setParam('ATM-VIS_ANS_{0:02d}_SUS'.format(i),
                   str(ans[i][0])) for i in range(num)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_STS'.format(i),
                   str(ans[i][1])) for i in range(num)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_STG'.format(i),
                   str(ans[i][2])) for i in range(num)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_EXC'.format(i),
                   str(ans[i][3])) for i in range(num)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_DOF'.format(i),
                   str(ans[i][4])) for i in range(num)]
    [self.setParam('ATM-VIS_ANS_{0:02d}_REF'.format(i),
                   str(ans[i][5])) for i in range(num)] 
    

read_dict = {'IP':['IDAMP','BLEND_ACC','BLEND_LVDT'],
             'BF':['DAMP'],
             'GAS':['DAMP'],
             'MN':['DAMP'],
             'IM':['DAMP'],                          
}
    
def make_plot(self):
    ansnum = get_pushed_list(self,'ANS')            
    suslist = set([self.getParam('ATM-VIS_ANS_%s_SUS'%(num)) for num in ansnum])
    stglist = set([self.getParam('ATM-VIS_ANS_%s_STG'%(num)) for num in ansnum])
    stslist = set([self.getParam('ATM-VIS_ANS_%s_STS'%(num)) for num in ansnum])
    exclist = set([self.getParam('ATM-VIS_ANS_%s_EXC'%(num)) for num in ansnum])
    doflist = set([self.getParam('ATM-VIS_ANS_%s_DOF'%(num)) for num in ansnum])
    reflist = set([self.getParam('ATM-VIS_ANS_%s_REF'%(num)) for num in ansnum])
    if len(stglist)*len(stslist)*len(exclist)*len(doflist)==1:
        print(suslist,stglist,stslist,exclist,doflist,reflist)
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
        #suslist,stslist,stglist,exclist,doflist,reflist = search()
        #[self.setParam('ATM-VIS_SELECT_BUTTON_REF_{0:02d}_VAL'.format(i), int(val)) for i,val in zip(range(10),reflist)]        

    def write(self, reason, value):
        status = True
        
        self.setParam(reason, value)
        if 'ATM-VIS_PLOT' in reason:            
            print('!')
            make_plot(self)
            

        if 'ATM-VIS_SEARCH' in reason:
            suslist = self.getParam('ATM-VIS_SELECT_LIST_SUS')
            stglist = self.getParam('ATM-VIS_SELECT_LIST_STG')
            stslist = self.getParam('ATM-VIS_SELECT_LIST_STS')
        elif 'ATM-VIS_SELECT' in reason:
            # SELECT_BUTTON
            key1,key2 = reason.split('_')[-2:]
            _val = self.getParam('ATM-VIS_SELECT_BUTTON_{0}_{1}_BIT'.format(key1,key2))
            self.setParam('ATM-VIS_SELECT_BUTTON_{0}_{1}_BIT'.format(key1,key2),_val+2)
            
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
