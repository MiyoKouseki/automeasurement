#!/usr/bin/env python
import itertools
from pcaspy import Driver, SimpleServer
from ezca import Ezca
import random

from search import search

prefix = 'K1:'

suspensions = ['ETMX','ETMY','ITMX','ITMY',
               'SRM','SR2','SR3','BS',
               'PRM','PR2','PR3',
               'MCI','MCO','MCE','IMMT1','IMMT2','OSTM','OMMT1','OMMT2']
stages = ['IP','GAS','BF','MN','IM']
states = ['SAFE','STANDBY','ISOLATED','DAMPED','ALIGNED']

refnum_fmt = 'ATM-VIS_{sus}_{stg}_{sts}_REFNUM' # dont need?
refnum_fmt_sdf_dummy = 'VIS-{sus}_{stg}_{sts}_REFNUM'
exec_fmt = 'ATM-VIS_{sus}_{stg}_{sts}_EXEC'
status_fmt = 'ATM-VIS_{sus}_{stg}_{sts}_STATUS'

params = list(itertools.product(suspensions,stages,states))
pvdb = {refnum_fmt.format(sus=sus,stg=stg,sts=sts):{'type':'float','value':0} for sus,stg,sts in params}
pvdb.update({refnum_fmt_sdf_dummy.format(sus=sus,stg=stg,sts=sts):{'type':'float','value':0} for sus,stg,sts in params})
pvdb.update({exec_fmt.format(sus=sus,stg=stg,sts=sts):{'type':'int'} for sus,stg,sts in params})
pvdb.update({status_fmt.format(sus=sus,stg=stg,sts=sts):{'type':'enum','enums':['RUN','STOP']} for sus,stg,sts in params})
pvdb.update({'ATM-VIS_SELECT_SUS_LIST':{'type':'str'}})
pvdb.update({'ATM-VIS_SELECT_SUS_{sus}'.format(sus=sus):{'type':'int','value':0} for sus in suspensions})
pvdb.update({'ATM-VIS_SELECT_SUS_{sus}_BIT'.format(sus=sus):{'type':'int','value':0} for sus in suspensions})
pvdb.update({'ATM-VIS_SELECT_STG_LIST':{'type':'str'}})
pvdb.update({'ATM-VIS_SELECT_STG_{stg}'.format(stg=stg):{'type':'int','value':0} for stg in stages})
pvdb.update({'ATM-VIS_SELECT_STG_{stg}_BIT'.format(stg=stg):{'type':'int','value':0} for stg in stages})
pvdb.update({'ATM-VIS_SELECT_STS_LIST':{'type':'str'}})
pvdb.update({'ATM-VIS_SELECT_STS_{sts}'.format(sts=sts):{'type':'int','value':0} for sts in states})
pvdb.update({'ATM-VIS_SELECT_STS_{sts}_BIT'.format(sts=sts):{'type':'int','value':0} for sts in states})
pvdb.update({'ATM-VIS_SELECT_REF_{0:02d}'.format(i):{'type':'int','value':0} for i in range(10)})
pvdb.update({'ATM-VIS_SELECT_REF_{0:02d}_BIT'.format(i):{'type':'int','value':0} for i in range(10)})
pvdb.update({'ATM-VIS_SELECT_REF_{0:02d}_VAL'.format(i):{'type':'float','value':0} for i in range(10)})
pvdb.update({'ATM-VIS_SELECT_REF_LIST':{'type':'str'}})
pvdb.update({'HOGE':{'type':'float'}})
pvdb.update({'ATM-VIS_SEARCH':{'type':'str'}})

ezca = Ezca('K1')

def search_reflist(suslist,stglist,stslist):
    reflist = [12354, 6696728, 2387234]
    return reflist


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
            #searched_reflist = search_reflist(suslist,stglist,stslist)
            #[self.setParam('ATM-VIS_SELECT_REF_{0:02d}_VAL'.format(i), val) for i,val in zip(range(10),searched_reflist)]
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
