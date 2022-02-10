

import re
def _parse(fname):
    pattern = '.*/PLANT_([A-Z]+[1-2]?)_([A-Z]+)_([A-Z]+)_([A-Z]+)_([A-Z]+[0-3]?)_([0-9]{12})\.xml'
    sus,sts,stg,exc,dof,ref = re.findall(pattern,fname)[0]            
    return sus,sts,stg,exc,dof,ref

import glob
import re
def is_in(items,string):
    if re.search('.*_({0})_.*'.format('|'.join(items)),string):
        if 'GAS' in string:
            print('.*_({0})_.*'.format('|'.join(items)))
            print(string)
        return True
    else:
        return False
    
def are_in(sus,stg,sts,exc,dof,ref,string):
    # fmt = '.*PLANT_({0})_({1})_({2})_({3})_({4})_({5}).xml'.\
    #     format('|'.join(sus),'|'.join(sts),'|'.join(stg),
    #            '|'.join(exc),'|'.join(dof),'|'.join(ref))
    # print(fmt,string)
    
    if re.search('.*PLANT_({0})_({1})_({2})_({3})_({4})_({5}).xml'.\
                 format('|'.join(sus),'|'.join(sts),'|'.join(stg),
                        '|'.join(exc),'|'.join(dof),'|'.join(ref))
                 ,string):
        return True
    else:
        return False
    
def are_both_in(items,string):
    return all([True for item in items if item in string])

    
def _search(prefix='./',sus=['.*'],stg=['.*'],sts=['.*'],exc=['.*'],dof=['.*'],ref=['.*'],cache=True):    
    if cache:
        with open('flist.txt','r') as f:
            ans = f.readlines()    
    else:
        fname = '/*/*/*/PLANT_*_*_*_*_*_*.xml'
        ans = glob.glob(prefix+fname)
        with open('flist.txt','w') as f:
            f.write('\n'.join(ans))
        exit()
    if not ans:
        raise ValueError('No file list')
    ans = [_ans for _ans in ans if are_in(sus,stg,sts,exc,dof,ref,_ans)]
    return ans

import numpy as np
def search(maxlist=10,**kwargs):
    print(kwargs)
    if not kwargs['sus']:
        kwargs['sus'] = ['.*']
    if not kwargs['stg']:
        kwargs['stg'] = ['.*']
    if not kwargs['sts']:
        kwargs['sts'] = ['.*']
    if not kwargs['exc']:
        kwargs['exc'] = ['.*']
    if not kwargs['dof']:
        kwargs['dof'] = ['.*']
    if not kwargs['ref']:
        kwargs['ref'] = ['.*']        
    
    ans = np.array([_parse(fname) for fname in _search(**kwargs)])
    try:
        row,col = ans.shape
    except:
        return [],[],[],[],[],[]        
    suslist = list(np.unique(ans[:,0]))
    stslist = list(np.unique(ans[:,1]))
    stglist = list(np.unique(ans[:,2]))
    exclist = list(np.unique(ans[:,3]))
    doflist = list(np.unique(ans[:,4]))        
    reflist = list(np.unique(ans[:,5]))
    reflist.sort(reverse=True)
    print(reflist)

    if not set(suslist)==set(kwargs['sus']) and not kwargs['sus']==['.*']:
        print('1')
        return [],[],[],[],[],[]
    if not set(stglist)==set(kwargs['stg']) and not kwargs['stg']==['.*']:
        print('2')        
        return [],[],[],[],[],[]        
    if not set(stslist)==set(kwargs['sts']) and not kwargs['sts']==['.*']:
        print('3')        
        return [],[],[],[],[],[]                
    if not set(exclist)==set(kwargs['exc']) and not kwargs['exc']==['.*']:
        print('4')        
        return [],[],[],[],[],[]                        
    if not set(doflist)==set(kwargs['dof']) and not kwargs['dof']==['.*']:
        print('5')        
        return [],[],[],[],[],[]                        
    if not set(reflist)==set(kwargs['ref']) and not kwargs['ref']==['.*']:
        print('6')        
        return [],[],[],[],[],[]                        
    return suslist,stslist,stglist,exclist,doflist,reflist
    
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--prefix',default='/kagra/Dropbox/Measurements/VIS/PLANT')
    parser.add_argument('--sus',nargs='+',default=['.*'])
    parser.add_argument('--sts',nargs='+',default=['.*'])
    parser.add_argument('--stg',nargs='+',default=['.*'])
    parser.add_argument('--exc',nargs='+',default=['.*'])
    parser.add_argument('--ref',nargs='+',default=['.*'])
    parser.add_argument('--dof',nargs='+',default=['.*'])
    parser.add_argument('--nocache',action='store_false')    

    args = parser.parse_args()
    prefix = args.prefix
    kwargs = {'sus':args.sus, 'stg':args.stg, 'sts':args.sts, 'exc':args.exc, 'ref':args.ref, 'dof':args.dof, 'prefix':args.prefix, 'cache':args.nocache}
    suslist,stslist,stglist,exclist,doflist,reflist = search(**kwargs)
    print(suslist,stslist,stglist,exclist,doflist,reflist)
