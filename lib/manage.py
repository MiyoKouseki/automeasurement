import argparse
import datetime

from vis import get_dofs
import itertools
import ezca

ezca = ezca.Ezca()

prefix = '/kagra/Dropbox/Measurements/VIS'
templates_fmt = prefix + '/TEMPLATES/PLANT_{sus}_{stg}.xml'
outfile_fmt = prefix + '/PLANT/{sus}/{yyyy}/{mm}/PLANT_{sus}_{sts}_{stg}_{exc}_{dof}_{ref}.xml'

def are_same_sustype(suslist):
    pass

def get_template(sus,stg):
    return templates_fmt.format(sus=sus,stg=stg)

def get_outfile(**kwargs):
    ref = kwargs['ref']
    yyyy,mm = ref[:4],ref[4:6]
    return outfile_fmt.format(yyyy=yyyy,mm=mm,**kwargs)

def get_grdstate(sus):
    return ezca['GRD-VIS_{sus}_STATE_S'.format(sus=sus)]

def get_refnum():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%H%M')

def run_plants(**kwargs):
    kwargs['sts'] = get_grdstate(sus)
    for dof in get_dofs(sus,stg):
        outfile = get_outfile(dof=dof,**kwargs)
        template = get_template(sus=sus,stg=stg)
        cmd = 'run_plant.sh %s %s 0 0'%(template,outfile)
        print(cmd)

def get_stages(stglist):        
    return stglist
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sus',nargs='+')
    parser.add_argument('--stg',nargs='+')
    parser.add_argument('--exc',nargs='+')
    args = parser.parse_args()
    suslist = args.sus    
    stglist = get_stages(args.stg)
    exclist = args.exc
    reflist = [get_refnum()]
    
    for sus in suslist:
        print(sus)
        for stg,exc,ref in itertools.product(stglist,exclist,reflist):
            run_plants(sus=sus,stg=stg,exc=exc,ref=ref)
        
    cmd = "run_plant.sh"
    args = [prefix + '/TEMPLATES/PLANT_SR2_GAS.xml',
            prefix + '/PLANT/SR2/2022/03/PLANT_SR2_SAFE_GAS_TEST_F0_202203141038.xml']
    debug = 0
    quick = 0
    
