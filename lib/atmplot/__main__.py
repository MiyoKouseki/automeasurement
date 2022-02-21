import re
import argparse
import itertools
from .base import TransferFunctionSpectrum, CrossSpectrum, CoherenceSpectrum
#from .plot import BodePlot
from .mybode import BodePlot

exct_fmt = 'K1:VIS-{SUS}_{STAGE}_{EXCT}_{DOF}_IN2'
read_fmt = 'K1:VIS-{SUS}_{STAGE}_{READ}_{DOF}_IN1_DQ'
prefix = '/kagra/Dropbox/Measurements/VIS/PLANT/{SUS}/{YYYY}/{MM}/'
fname_fmt = 'PLANT_{SUS}_{STATE}_{STAGE}_{EXCT}_{DOF}_{YYYY}{MM}{DD}{HH}{mm}.xml'


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--sus','-s',nargs='+',default=['ETMX'],
                        help='suspension name')
    parser.add_argument('--exc','-i',default='IP_TEST_L',
                        help='excitation channel')
    parser.add_argument('--read','-o',default='IP_IDAMP_L',
                        help='read channel')
    parser.add_argument('--refnum','-r',nargs='+',
                        default=['202202181906','202201211941'],
                        help='reference number')    
    args = parser.parse_args()
    
    # Arguments
    suspensions = args.sus
    ch_from = args.exc
    ch_to = args.read
    refnumbers = args.refnum
    state = 'STANDBY' # should be given by refnumber
        
    # Parse Parameters from Arguments
    exct_kwargs = dict(zip(['STAGE','EXCT','DOF'],ch_from.split('_')))
    read_kwargs = dict(zip(['STAGE','READ','DOF'],ch_to.split('_')))
    pattern = '([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})'    
    datetime_kwargs = [dict(zip(['YYYY','MM','DD','HH','mm'],
                               re.findall(pattern,refnum)[0]))
                       for refnum in refnumbers]

    # Fix me ---------------------------------------------
    from datetime import datetime
    huga = [datetime.strptime(refnum, '%Y%m%d%H%M').strftime('%Y %b %d %H:%m')
            for refnum in refnumbers]
    # Fix me ---------------------------------------------
    
    # Set File Name and Channel Name from Parameters
    hoge = list(itertools.product(suspensions,datetime_kwargs)) # need list()?
    huge = list(itertools.product(suspensions,huga)) # need list()?
    _from = [exct_fmt.format(SUS=sus,**exct_kwargs) for sus,_ in hoge]
    _to = [read_fmt.format(SUS=sus,**read_kwargs)for sus,_ in hoge]
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
    figname = '/kagra/Dropbox/Measurements/VIS/figures/{refnums}_{ch_from}_{ch_to}.png'.\
        format(refnums="_".join(refnumbers),ch_from=ch_from,ch_to=ch_to)
    plot.savefig(figname)
    plot.close()
