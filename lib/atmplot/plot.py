#from gwpy.plot import BodePlot as GwBodePlot
import matplotlib.gridspec as gridspec
import numpy as np

from .mybode import BodePlot
from .base import TransferFunctionSpectrum, CrossSpectrum, CoherenceSpectrum

import re
import itertools


# class BodePlot(GwBodePlot):
#     def __init__(self,*filters,**kwargs):
#         label = kwargs.pop('label', True)
#         super().__init__(*filters,**kwargs)
#         ylims = [[-120,20],[-180,180]]
#         [ax.set_ylim(*ylim) for ax,ylim in zip(self.axes,ylims)]
#         self.axes[1].set_yticks(range(-180,181,90))
#         [ax.legend(label,alpha=0.7,loc='upper left') for ax in self.axes]
        
#     def add_coherence(self,codata,**kwargs):
#         gs = gridspec.GridSpec(3,1)
#         self.axes[0].set_position(gs[0:1].get_position(self.figure))
#         self.axes[1].set_position(gs[1:2].get_position(self.figure))
#         self.add_subplot(gs[2:3])
#         self.axes[0].set_subplotspec(gs[0:1])
#         self.axes[1].set_subplotspec(gs[1:2])                   
#         for data in codata:
#             self.axes[2].plot(data.frequencies.value,np.angle(data.value,deg=True))
#         self.axes[2].set_xscale('log')
#         self.axes[2].set_xlabel('Frequency [Hz]')

#         print(self.axes)
#         print([a for a in dir(self.axes[0]) if 'share' in a])
#         print(self.axes[0].get_shared_x_axes())
#         #self.axes[0].get_shared_x_axes().join(self.axes[0],self.axes[2])
#         #self.axes[1].get_shared_x_axes().join(self.axes[1],self.axes[2])
#         print(dir(self.axes[0]._shared_x_axes))
#         self.axes[0]._shared_x_axes.remove(self.axes[1])
#         #self.axes[1]._shared_x_axes.remove(self.axes[0])
#         print(dir(self.axes[1].get_shared_x_axes().clean()))
#         self.axes[0].sharex(self.axes[2])
#         self.axes[1].sharex(self.axes[2])
#         pass
#         #self.clf()
#         #self.add_subplot(3,1,1)
#         #self.add_subplot(3,1,2,sharex=self.axes[2])
#         #self.add_subplot(3,1,3,sharex=self.axes[2])

exct_fmt = 'K1:VIS-{SUS}_{STAGE}_{EXCT}_{DOF}_IN2'
read_fmt = 'K1:VIS-{SUS}_{STAGE}_{READ}_{DOF}_IN1_DQ'
prefix = '/kagra/Dropbox/Measurements/VIS/PLANT/{SUS}/{YYYY}/{MM}/'
prefix = '/diagdata/PLANT/{SUS}/{YYYY}/{MM}/'
fname_fmt = 'PLANT_{SUS}_{STATE}_{STAGE}_{EXCT}_{DOF}_{YYYY}{MM}{DD}{HH}{mm}.xml'


def plot(suspensions,ch_from,ch_to,refnumbers,state):    
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
    print(exct_kwargs)    
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
    print(exct_kwargs)
    
    # Set File Name and Channel Name from Parameters
    hoge = list(itertools.product(suspensions,datetime_kwargs)) # need list()?
    huge = list(itertools.product(suspensions,huga)) # need list()?
    _from = [exct_fmt.format(SUS=sus,**_exct_kwargs) for sus,_ in hoge]
    _to = [read_fmt.format(SUS=sus,**_read_kwargs)for sus,_ in hoge]

    print(exct_kwargs)
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
    #plot.add_coherence(codata)
    figname = '/kagra/Dropbox/Measurements/VIS/figures/{refnums}_{ch_from}_{ch_to}.png'.format(refnums="_".join(refnumbers),ch_from=ch_from,ch_to=ch_to)
    figname = '/figures/{refnums}_{ch_from}_{ch_to}.png'.format(refnums="_".join(refnumbers),ch_from=ch_from,ch_to=ch_to)    
    plot.savefig(figname)
    plot.close()
        
