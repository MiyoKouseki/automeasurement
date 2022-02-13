#!/usr/bin/env python
from pcaspy import Driver, SimpleServer
import random

from search import search

from db import pvdb
from vis import suspensions,stages,states

prefix = 'K1:'

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
            print('-sus {0} -stg {1} -sts {2}'.format(suslist,stglist,stslist))
        elif 'ATM-VIS_SELECT' in reason:
            key1,key2 = reason.split('_')[-2:]
            _val = self.getParam('ATM-VIS_SELECT_{0}_{1}_BIT'.format(key1,key2))
            self.setParam('ATM-VIS_SELECT_{0}_{1}_BIT'.format(key1,key2),_val+2)            
            suslist = [ sus for sus in suspensions if self.getParam('ATM-VIS_SELECT_SUS_{0}_BIT'.format(sus))%4]
            self.setParam('ATM-VIS_SELECT_SUS_LIST',' '.join(suslist))
            stglist = [ stg for stg in stages if self.getParam('ATM-VIS_SELECT_STG_{0}_BIT'.format(stg))%4]
            self.setParam('ATM-VIS_SELECT_STG_LIST',' '.join(stglist))
            stslist = [ sts for sts in states if self.getParam('ATM-VIS_SELECT_STS_{0}_BIT'.format(sts))%4]
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
