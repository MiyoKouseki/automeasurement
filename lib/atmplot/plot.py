from gwpy.plot import BodePlot as GwBodePlot
import matplotlib.gridspec as gridspec
import numpy as np

class BodePlot(GwBodePlot):
    def __init__(self,*filters,**kwargs):
        label = kwargs.pop('label', True)
        super().__init__(*filters,**kwargs)
        ylims = [[-120,20],[-180,180]]
        [ax.set_ylim(*ylim) for ax,ylim in zip(self.axes,ylims)]
        self.axes[1].set_yticks(range(-180,181,90))
        [ax.legend(label,alpha=0.7,loc='upper left') for ax in self.axes]
        
    def add_coherence(self,codata,**kwargs):
        gs = gridspec.GridSpec(3,1)
        self.axes[0].set_position(gs[0:1].get_position(self.figure))
        self.axes[1].set_position(gs[1:2].get_position(self.figure))
        self.add_subplot(gs[2:3])
        self.axes[0].set_subplotspec(gs[0:1])
        self.axes[1].set_subplotspec(gs[1:2])                   
        for data in codata:
            self.axes[2].plot(data.frequencies.value,np.angle(data.value,deg=True))
        self.axes[2].set_xscale('log')
        self.axes[2].set_xlabel('Frequency [Hz]')

        print(self.axes)
        print([a for a in dir(self.axes[0]) if 'share' in a])
        print(self.axes[0].get_shared_x_axes())
        #self.axes[0].get_shared_x_axes().join(self.axes[0],self.axes[2])
        #self.axes[1].get_shared_x_axes().join(self.axes[1],self.axes[2])
        print(dir(self.axes[0]._shared_x_axes))
        self.axes[0]._shared_x_axes.remove(self.axes[1])
        #self.axes[1]._shared_x_axes.remove(self.axes[0])
        print(dir(self.axes[1].get_shared_x_axes().clean()))
        self.axes[0].sharex(self.axes[2])
        self.axes[1].sharex(self.axes[2])
        pass
        #self.clf()
        #self.add_subplot(3,1,1)
        #self.add_subplot(3,1,2,sharex=self.axes[2])
        #self.add_subplot(3,1,3,sharex=self.axes[2])
        
