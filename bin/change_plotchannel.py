

if __name__=="__main__":
    import re

    src = './PLANT_ETMX_SAFE_MN_TEST_P_202202101531.xml'
    #src = './PLANT_ETMX_SAFE_GAS_TEST_F3_202202101531.xml'
    #src = './PLANT_ETMX_SAFE_IP_TEST_Y_202202101531.xml'
    pattern = '.*/PLANT_([A-Z]+[1-2]?)_([A-Z]+)_([A-Z]+)_([A-Z]+)_([A-Z]+[0-3]?)_([0-9]*)\.xml'
    sus,sts,stg,exc,dof,ref = re.findall(pattern,src)[0]
    if stg=='GAS':
        stg = dof
        dof = 'GAS'
        print(sus,stg,dof)
        _dof = 'GAS'
    else:
        _dof = 'L'

    text = open(src,'r').read()
    exct = 'K1:VIS-%s_%s_%s_%s_IN2'%(sus,stg,exc,dof)
    red = re.findall('<.*"TracesBChannel\[0\]".*>K1:VIS-%s_%s_(.*)_%s_IN1_DQ<.*>'%(sus,stg,_dof),text)[0]
    read = 'K1:VIS-%s_%s_%s_%s_IN1_DQ'%(sus,stg,red,dof)
    #
    text,n = re.subn(r'(<.*"TracesActive\[0\]".*>).*(<.*>)',r'\1false\2',text,3)
    text,n = re.subn(r'(<.*"TracesActive\[1\]".*>).*(<.*>)',r'\1true\2',text,3)
    text,n = re.subn(r'(<.*"TracesAChannel\[1\]".*>).*(<.*>)',r'\1%s\2'%(exct),text,3)
    text,n = re.subn(r'(<.*"TracesBChannel\[1\]".*>).*(<.*>)',r'\1%s\2'%(read),text,3)
    text,n = re.subn(r'(<.*"TracesBChannel\[0\]".*)%s_IN1_DQ(<.*>)'%(_dof),r'\1%s_IN1_DQ\2'%(dof),text,3)
    text,n = re.subn(r'(<.*"StyleTitle".*>.*)%s(.*<.*>)'%(_dof),r'\1%s\2'%(dof),text,3)        
    text,n = re.subn(r'(<.*"TracesAChannel\[0\]".*)%s_IN2(<.*>)'%(_dof),r'\1%s_IN2\2'%(dof),text,9)
    text,n = re.subn(r'(<.*"StyleTitle".*>)%s (.*<.*>)'%(_dof),r'\1%s\2'%(dof),text,9)
    #
    open(src,'w').write(text)
