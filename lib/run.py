#!/usr/bin/env python
import numpy as np
from pcaspy import Driver, SimpleServer
import random

from search import search

from db import pvdb
from vis import suspensions,stages,states,key2dict

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

class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()
        self.tid = None
        #suslist,stslist,stglist,exclist,doflist,reflist = search()
        #[self.setParam('ATM-VIS_SELECT_BUTTON_REF_{0:02d}_VAL'.format(i), int(val)) for i,val in zip(range(10),reflist)]        

    def write(self, reason, value):
        status = True
        
        self.setParam(reason, value)

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
            #
            try:
                num = min(10,ans.shape[0])                
            except:
                num = 10
                ans = np.array(['---']*10*6).reshape(10,6)    
            #
            reflist = ans[:,-1]
            print(reflist)
            [self.setParam('ATM-VIS_SELECT_BUTTON_REF_{0:02d}_VAL'.format(i), str(val)) for i,val in zip(range(10),['---']*10)]
            [self.setParam('ATM-VIS_SELECT_BUTTON_REF_{0:02d}_VAL'.format(i), str(val)) for i,val in zip(range(10),np.unique(reflist))]
            #
            [self.setParam('ATM-VIS_ANS_{0:02d}_SUS'.format(i), str('---')) for i in range(10)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_STS'.format(i), str('---')) for i in range(10)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_STG'.format(i), str('---')) for i in range(10)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_EXC'.format(i), str('---')) for i in range(10)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_DOF'.format(i), str('---')) for i in range(10)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_REF'.format(i), str('---')) for i in range(10)]                                                            
            #
            [self.setParam('ATM-VIS_ANS_{0:02d}_SUS'.format(i), str(ans[i][0])) for i in range(num)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_STS'.format(i), str(ans[i][1])) for i in range(num)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_STG'.format(i), str(ans[i][2])) for i in range(num)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_EXC'.format(i), str(ans[i][3])) for i in range(num)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_DOF'.format(i), str(ans[i][4])) for i in range(num)]
            [self.setParam('ATM-VIS_ANS_{0:02d}_REF'.format(i), str(ans[i][5])) for i in range(num)]                                                
            #
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
