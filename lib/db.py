import itertools
from vis import suspensions,stages,states

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

