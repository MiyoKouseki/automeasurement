#!/usr/bin/env python
import itertools
from pcaspy import Driver, SimpleServer

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
#pvdb.update({'ATM-VIS_{sus}'.format(sus=sus):{'type':'enum','enums':['o','x']} for sus in suspensions})
pvdb.update({'ATM-VIS_{sus}'.format(sus=sus):{'type':'int','value':0} for sus in suspensions})
pvdb.update({'ATM-VIS_{sus}_BIT'.format(sus=sus):{'type':'int','value':0} for sus in suspensions})
pvdb.update({'ATM-VIS_STGLIST':{'type':'enum','enums':stages}})
pvdb.update({'ATM-VIS_STSLIST':{'type':'enum','enums':states}})
pvdb.update({'HOGE':{'type':'float'}})

class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)
