#!/usr/bin/env python
import itertools
from pcaspy import Driver, SimpleServer

prefix = 'K1:'

suspensions = ['ETMX','ETMY','ITMX','ITMY']
stages = ['IP','GAS','BF','MN','IM']
states = ['SAFE','STANDBY','ISOLATED','DAMPED','ALIGNED']

refnum_fmt = 'ATM-VIS_{sus}_{stg}_{sts}_REFNUM'
refnum_fmt_sdf_dummy = 'VIS-{sus}_{stg}_{sts}_REFNUM'
exec_fmt = 'ATM-VIS_{sus}_{stg}_{sts}_EXEC'
status_fmt = 'ATM-VIS_{sus}_{stg}_{sts}_STATUS'

params = list(itertools.product(suspensions,stages,states))
pvdb = {refnum_fmt.format(sus=sus,stg=stg,sts=sts):{'type':'int'} for sus,stg,sts in params}
pvdb.update({refnum_fmt_sdf_dummy.format(sus=sus,stg=stg,sts=sts):{'type':'int'} for sus,stg,sts in params})
pvdb.update({exec_fmt.format(sus=sus,stg=stg,sts=sts):{'type':'int'} for sus,stg,sts in params})
pvdb.update({status_fmt.format(sus=sus,stg=stg,sts=sts):{'type':'enum','enums':['RUN','STOP']} for sus,stg,sts in params})

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
