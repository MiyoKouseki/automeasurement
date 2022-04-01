#from gwpy.plot import BodePlot as GwBodePlot
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt

from .mybode import BodePlot
from .base import TransferFunctionSpectrum, CrossSpectrum, CoherenceSpectrum

import re
import itertools

exct_fmt = 'K1:VIS-{SUS}_{STAGE}_{EXCT}_{DOF}_IN2'
read1_fmt = 'K1:VIS-{SUS}_{STAGE}_{READ}_{DOF}_IN1_DQ'
read2_fmt = 'K1:VIS-{SUS}_{STAGE}_{READ}_{DOF}_OUT_DQ'
prefix = '/kagra/Dropbox/Measurements/VIS/PLANT/{SUS}/{YYYY}/{MM}/'
prefix = '/diagdata/PLANT/{SUS}/{YYYY}/{MM}/'
fname_fmt = 'PLANT_{SUS}_{STATE}_{STAGE}_{EXCT}_{DOF}_{YYYY}{MM}{DD}{HH}{mm}.xml'


def plot(suspensions,ch_from,ch_tos,refnumbers,state):
    if isinstance(ch_tos,str):
        ch_tos = [ch_tos]
    
    for ch_to in ch_tos:
        print(ch_from,ch_to)
        _plot(suspensions,ch_from,ch_to,refnumbers,state)
    
        
    
def _plot(suspensions,ch_from,ch_to,refnumbers,state):    
    # Parse Parameters from Arguments
    exct_kwargs = dict(zip(['STAGE','EXCT','DOF'],ch_from.split('_')))
    read_kwargs = dict(zip(['STAGE','READ','DOF'],ch_to.split('_')))
    pattern = '([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})'    
    datetime_kwargs = [dict(zip(['YYYY','MM','DD','HH','mm'],
                               re.findall(pattern,refnum)[0]))
                       for refnum in refnumbers]
    # Fix me -------------------------------------
    _exct_kwargs = exct_kwargs.copy()
    _read_kwargs = read_kwargs.copy()
    if read_kwargs['STAGE']=='GAS':
        _read_kwargs['STAGE'] = _read_kwargs['DOF']
        _read_kwargs['DOF'] = 'GAS'
    if exct_kwargs['STAGE']=='GAS':
        _exct_kwargs['STAGE'] = _exct_kwargs['DOF']
        _exct_kwargs['DOF'] = 'GAS'        
    # Fix me -------------------------------------    
    
    # Fix me ---------------------------------------------
    from datetime import datetime
    huga = [datetime.strptime(refnum, '%Y%m%d%H%M').strftime('%Y %b %d %H:%m')
            for refnum in refnumbers]
    # Fix me ---------------------------------------------
    
    # Set File Name and Channel Name from Parameters
    hoge = list(itertools.product(suspensions,datetime_kwargs)) # need list()?
    huge = list(itertools.product(suspensions,huga)) # need list()?
    _from = [exct_fmt.format(SUS=sus,**_exct_kwargs) for sus,_ in hoge]
    if 'INF' in ch_to:
        _to = [read2_fmt.format(SUS=sus,**_read_kwargs)for sus,_ in hoge]
    else:
        _to = [read1_fmt.format(SUS=sus,**_read_kwargs)for sus,_ in hoge]        

    sources = [(prefix+fname_fmt).\
               format(STATE=state,SUS=sus,
                      **exct_kwargs,**datetime_kwargs)
               for sus,datetime_kwargs in hoge]    
    label = [sus+' ('+refnum+')' for sus,refnum in huge]
    title = ch_from + ' -> ' + ch_to    
    tfdata = [TransferFunctionSpectrum(source,read_channel,exctitation_channel) for \
              source,read_channel,exctitation_channel in zip(sources,_to,_from)]
    codata = [CoherenceSpectrum(source,read_channel,exctitation_channel) for \
               source,read_channel,exctitation_channel in zip(sources,_to,_from)]
    
    # Plot
    plot = BodePlot(*tfdata,coherence=codata,figsize=(8,8),title=title,label=label)

    figname = '/figures/{refnums}_{ch_from}_{ch_to}.png'.format(refnums="_".join(refnumbers),ch_from=ch_from,ch_to=ch_to)    
    plot.savefig(figname)
    plot.savefig('/figures/now.png')    
    plot.close()    
    return plot
