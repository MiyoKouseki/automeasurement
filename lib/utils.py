import os.path
import subprocess

plant_fmt = '{pfx}/PLANT/{sus}/{yy}/{mm}/PLANT_{sus}_{sts}_{stg}_{exc}_{dof}_{ref}.xml'

DIAGGUI_CMD = ['diaggui']

class HogeError(Exception):
    pass

def get_path(**kwargs):
    kwargs['yy'] = kwargs['ref'][:4]
    kwargs['mm'] = kwargs['ref'][4:6]    
    path = plant_fmt.format(**kwargs)
    return path

def diagfile_exists(**kwargs):
    return os.path.exists(get_path(**kwargs))

def exec_diaggui(*args,**kwargs):
    cmd = DIAGGUI_CMD + list(args)
    try:
        proc = subprocess.Popen(cmd, **kwargs)  
    except subprocess.CalledProcessError as e:
        raise HogeError(e)
    return proc


if __name__=='__main__':
    prefix = '/kagra/Dropbox/Measurements/VIS'

    kwargs = {'sus':'ETMX','sts':'STANDBY','stg':'IP','exc':'TEST','dof':'L',
              'ref':'202202181906','pfx':prefix}
    fname = get_path(**kwargs)
    if os.path.exists(fname):
        proc = exec_diaggui(fname)
        print(proc)        
