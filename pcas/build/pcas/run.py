#!/usr/bin/env python
import itertools
from pcaspy import Driver, SimpleServer
from ezca import Ezca

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
pvdb.update({'ATM-VIS_RN{0:02d}'.format(i):{'type':'float','value':0} for i in range(10)})
pvdb.update({'ATM-VIS_SELECT_{sus}'.format(sus=sus):{'type':'int','value':0} for sus in suspensions})
pvdb.update({'ATM-VIS_SELECT_{sus}_BIT'.format(sus=sus):{'type':'int','value':0} for sus in suspensions})
pvdb.update({'ATM-VIS_SELECT_{stg}'.format(stg=stg):{'type':'int','value':0} for stg in stages})
pvdb.update({'ATM-VIS_SELECT_{stg}_BIT'.format(stg=stg):{'type':'int','value':0} for stg in stages})
pvdb.update({'ATM-VIS_SELECT_{sts}'.format(sts=sts):{'type':'int','value':0} for sts in states})
pvdb.update({'ATM-VIS_SELECT_{sts}_BIT'.format(sts=sts):{'type':'int','value':0} for sts in states})
pvdb.update({'HOGE':{'type':'float'}})
pvdb.update({'ATM-VIS_SELECT_SUS':{'type':'str'}})
pvdb.update({'ATM-VIS_SELECT_STG':{'type':'str'}})
pvdb.update({'ATM-VIS_SELECT_STS':{'type':'str'}})

ezca = Ezca('K1')

def get_suslist():
    suslist = ['ETMX','ETMY']
    print(ezca['ATM-VIS_SELECT_ETMX'])
    return suslist

class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()
        self.tid = None

    def write(self, reason, value):
        status = True
        self.setParam(reason, value)
        for key in suspensions:
            if reason=='ATM-VIS_SELECT_{key}'.format(key=key):
                _val = self.getParam('ATM-VIS_SELECT_{key}_BIT'.format(key=key))
                self.setParam('ATM-VIS_SELECT_{key}_BIT'.format(key=key),_val+2)
                suslist = get_suslist()
                self.setParam('ATM-VIS_SELECT_SUS'," ".join(suslist))
            else:
                status = False
        self.updatePVs()
        
        return True


if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)
