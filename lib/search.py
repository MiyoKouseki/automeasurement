#
#! coding:utf-8
import argparse
import settings

import re
import glob

plant_pattern = '.*/PLANT_([A-Z]+[1-2]?)_([A-Z]+)_([A-Z]+)_([A-Z]+)_([A-Z]+[0-3]?)_([0-9]{12})\.xml'


def _get_params(fname):
    sus,sts,stg,exc,dof,ref = re.findall(plant_pattern,fname)[0]
    return sus,sts,stg,exc,dof,ref

    
def are_in(sus,stg,sts,exc,dof,ref,fpath):
    ''' 各パラメータが fliepath に含まれているか判定する
    '''
    # key同士はANDだがkey自身はORで検索
    if re.search('.*PLANT_({0})_({1})_({2})_({3})_({4})_({5}).xml'.\
                 format('|'.join(sus),'|'.join(sts),'|'.join(stg),
                        '|'.join(exc),'|'.join(dof),'|'.join(ref))
                 ,fpath):
        return True
    else:
        return False    
    
def _search_or(**kwargs):
    '''
    '''
    prefix = kwargs.get('prefix','./')
    sus = kwargs.get('sus',['.*'])
    stg = kwargs.get('stg',['.*'])
    sts = kwargs.get('sts',['.*'])
    exc = kwargs.get('exc',['.*'])
    dof = kwargs.get('dof',['.*'])
    ref = kwargs.get('ref',['.*'])
    cache  = kwargs.get('cache',True)
    if not sus: sus=['.*']
    if not stg: stg=['.*']
    if not sts: sts=['.*']
    if not exc: exc=['.*']
    if not dof: dof=['.*']
    if not ref: ref=['.*']    

    if cache:
        with open('flist.txt','r') as f:
            ans = f.readlines()    
    else:
        fname = '/*/*/*/PLANT_*_*_*_*_*_*.xml'
        ans = glob.glob(prefix+fname)
        with open('flist.txt','w') as f:
            f.write('\n'.join(ans))
        print('reloaded')
        exit()
        
    if not ans:
        raise ValueError('No file list')

    # key同士はANDだがkey自身はORで検索
    ans = [_ans for _ans in ans if are_in(sus,stg,sts,exc,dof,ref,_ans)]
    return ans

import numpy as np

def compress_dof(ans):
    col = 4 # means dof    
    func = lambda _ans: '_'.join(_ans)
    ans_u = np.unique([func(_ans) for _ans in np.delete(ans,col,axis=1)])
    ans_dof = np.array([" ".join(np.sort(list([ _ans[col] for _ans in ans if func(np.delete(_ans,col))==txt]))) for txt in ans_u])
    ans_u = np.array(list(map(lambda _ans: _ans.split("_"),ans_u)))
    ans = np.insert(ans_u,4,ans_dof,axis=1)    
    return ans

def search(maxlist=10,**kwargs):
    sus = kwargs.get('sus',['.*'])
    stg = kwargs.get('stg',['.*'])
    sts = kwargs.get('sts',['.*'])
    exc = kwargs.get('exc',['.*'])
    dof = kwargs.get('dof',['.*'])
    ref = kwargs.get('ref',['.*'])    

    ans = np.array([_get_params(fname) for fname in _search_or(**kwargs)])
    try:
        row,col = ans.shape
    except:
        return [],[],[],[],[],[]
    
    ans = compress_dof(ans)
    
    suslist = list(np.unique(ans[:,0]))
    stslist = list(np.unique(ans[:,1]))
    stglist = list(np.unique(ans[:,2]))
    exclist = list(np.unique(ans[:,3]))
    doflist = list(np.unique(ans[:,4]))        
    reflist = list(np.unique(ans[:,5]))
    reflist.sort(reverse=True)
    return ans
    
if __name__=='__main__':
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
    kwargs = {'sus':args.sus, 'stg':args.stg, 'sts':args.sts, 'exc':args.exc,
              'ref':args.ref, 'dof':args.dof, 'prefix':args.prefix, 'cache':args.nocache}
    suslist,stslist,stglist,exclist,doflist,reflist = search(**kwargs)
    print(suslist,stslist,stglist,exclist,doflist,reflist)    
