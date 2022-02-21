
import os
import ezca
print(ezca.__file__)

from ..lib import atmplot

os.environ['EPICS_CA_ADDR_LIST'] = '172.20.0.2'
os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'NO'    
ezca = ezca.Ezca()

if __name__=='__main__':
    ans_num = [ num for num in range(10) \
                if ezca['ATM-VIS_SELECT_BUTTON_ANS_%02d_BIT'%(num)]%4==2]
    
    for num in ans_num:
        sus = ezca['ATM-VIS_ANS_%02d_SUS'%(num)]
        stg = ezca['ATM-VIS_ANS_%02d_STG'%(num)]
        exc = ezca['ATM-VIS_ANS_%02d_EXC'%(num)]
        dof = ezca['ATM-VIS_ANS_%02d_DOF'%(num)]
        ref = ezca['ATM-VIS_ANS_%02d_REF'%(num)]                                
        print(sus,stg,exc,dof,ref)

    sus = [ezca['ATM-VIS_ANS_%02d_SUS'%(num)] for num in ans_num]
    print(sus)
    
    atmplot()
