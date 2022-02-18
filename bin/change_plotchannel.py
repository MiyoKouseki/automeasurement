

if __name__=="__main__":
    import re
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('src')

    args = parser.parse_args()
    src = args.src
    
    pattern = '.*/PLANT_([A-Z]+[1-2]?)_([A-Z]+)_([A-Z]+)_([A-Z]+)_([A-Z]+[0-3]?)_([0-9]*)\.xml'
    sus,sts,stg,exc,dof,ref = re.findall(pattern,src)[0]
    
    text = open(src,'r').read()
    if stg=='GAS':
        _tdof = 'F0'
        tdof = dof
    else:
        _tdof = 'L'
        tdof = dof        
    
    text,n = re.subn(r'(<.*"StyleTitle".*>.*)%s(.*<.*>)'%(_tdof),r'\1%s\2'%(tdof),text,3)
    text,n = re.subn(r'(<.*"StyleTitle".*>)%s (.*<.*>)'%(_tdof),r'\1%s\2'%(tdof),text,9)
    
    if stg=='GAS':
        stg = dof
        dof = 'GAS'
        print(sus,stg,dof)
        _dof = 'GAS'
        _stg = 'F0'
    else:
        _dof = 'L'
        _stg = stg

    exct = 'K1:VIS-%s_%s_%s_%s_IN2'%(sus,stg,exc,dof)
    red = re.findall('<.*"TracesBChannel\[0\]".*>K1:VIS-%s_%s_(.*)_.*_IN1_DQ<.*>'%(sus,stg),text)[0]
    read = 'K1:VIS-%s_%s_%s_%s_IN1_DQ'%(sus,stg,red,dof)
    text,n = re.subn(r'(<.*"TracesAChannel\[1\]".*>).*(<.*>)',r'\1%s\2'%(exct),text,3)
    text,n = re.subn(r'(<.*"TracesBChannel\[1\]".*>).*(<.*>)',r'\1%s\2'%(read),text,3)    
    #
    text,n = re.subn(r'(<.*"TracesActive\[0\]".*>).*(<.*>)',r'\1false\2',text,3)
    text,n = re.subn(r'(<.*"TracesActive\[1\]".*>).*(<.*>)',r'\1true\2',text,3)
    text,n = re.subn(r'(<.*"TracesBChannel\[0\]".*)%s_%s_%s_IN1_DQ(<.*>)'%(_stg,red,_dof),
                     r'\1%s_%s_%s_IN1_DQ\2'%(stg,red,dof),text,3)
    text,n = re.subn(r'(<.*"TracesAChannel\[0\]".*)%s_%s_%s_IN2(<.*>)'%(_stg,exc,_dof),
                     r'\1%s_%s_%s_IN2\2'%(stg,exc,dof),text,9)

    #
    open(src,'w').write(text)
