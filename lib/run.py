#!/usr/bin/env python
from pcaspy import Driver, SimpleServer
import random

from search import search

from db import pvdb
from vis import suspensions,stages,states,key2dict

prefix = 'K1:'

def is_pushed(self,key1,key2):
    return self.getParam('ATM-VIS_SELECT_{0}_{1}_BIT'.format(key1,key2))%4

def get_pushed_list(self,key1):
    '''
    '''
    _list = [ key2 for key2 in key2dict[key1] if is_pushed(self,key1,key2)]
    return _list

class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()
        self.tid = None
        kwargs = {'sus':['.*'], 'stg':['.*'], 'sts':['.*'], 'exc':['.*'], 'ref':['.*'], 'dof':['.*'], 'cache':True}      
        suslist,stslist,stglist,exclist,doflist,reflist = search(**kwargs)
        [self.setParam('ATM-VIS_SELECT_REF_{0:02d}_VAL'.format(i), int(val)) for i,val in zip(range(10),reflist)]        

    def write(self, reason, value):
        status = True
        
        self.setParam(reason, value)

        if 'ATM-VIS_SEARCH' in reason:
            suslist = self.getParam('ATM-VIS_SELECT_SUS_LIST')
            stglist = self.getParam('ATM-VIS_SELECT_STG_LIST')
            stslist = self.getParam('ATM-VIS_SELECT_STS_LIST')
        elif 'ATM-VIS_SELECT' in reason:
            key1,key2 = reason.split('_')[-2:]            
            _val = self.getParam('ATM-VIS_SELECT_{0}_{1}_BIT'.format(key1,key2))
            self.setParam('ATM-VIS_SELECT_{0}_{1}_BIT'.format(key1,key2),_val+2)
            
            # push されているボタンのリストを取得
            suslist = get_pushed_list(self,'SUS')
            stglist = get_pushed_list(self,'STG')
            stslist = get_pushed_list(self,'STS')                        
            self.setParam('ATM-VIS_SELECT_SUS_LIST',' '.join(suslist))            
            self.setParam('ATM-VIS_SELECT_STG_LIST',' '.join(stglist))
            self.setParam('ATM-VIS_SELECT_STS_LIST',' '.join(stslist))

            reflist = [self.getParam('ATM-VIS_SELECT_REF_{0:02d}_VAL'.format(ref)) for ref in range(10) \
                       if self.getParam('ATM-VIS_SELECT_REF_{0:02d}_BIT'.format(ref))%4]
            self.setParam('ATM-VIS_SELECT_REF_LIST',' '.join(map(str,reflist)))
            
            kwargs = {'sus':suslist, 'stg':stglist, 'sts':stslist, 'exc':['.*'], 'ref':['.*'], 'dof':['.*'], 'cache':True}            
            suslist,stslist,stglist,exclist,doflist,reflist = search(**kwargs)
            #print(suslist,stslist,stglist,exclist,doflist,reflist)
            [self.setParam('ATM-VIS_SELECT_REF_{0:02d}_VAL'.format(i), int(val)) for i,val in zip(range(10),[0]*10)]            
            [self.setParam('ATM-VIS_SELECT_REF_{0:02d}_VAL'.format(i), int(val)) for i,val in zip(range(10),reflist)]            
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
