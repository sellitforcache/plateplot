#! /usr/bin/env python
# Script to plot proton history on the SINQ target
# Ryan M. Bergmann, Nov 17, 2014.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.colors import LogNorm, PowerNorm
import sys
import numpy
import scipy as sp

### set TeX
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

def fill_between_steps(x, y1, y2=0, h_align='post', ax=None, **kwargs):
    ''' Fills a hole in matplotlib: fill_between for step plots.

    Parameters :
    ------------

    x : array-like
        Array/vector of index values. These are assumed to be equally-spaced.
        If not, the result will probably look weird...
    y1 : array-like
        Array/vector of values to be filled under.
    y2 : array-Like
        Array/vector or bottom values for filled area. Default is 0.

    **kwargs will be passed to the matplotlib fill_between() function.

    '''
    # If no Axes opject given, grab the current one:
    if ax is None:
        ax = plt.gca()
    # First, duplicate the x values
    xx = x.repeat(2)[1:]
    # Now: the average x binwidth
    xstep = sp.repeat((x[1:] - x[:-1]), 2)
    xstep = sp.concatenate(([xstep[0]], xstep, [xstep[-1]]))
    # Now: add one step at end of row.
    xx = sp.append(xx, xx.max() + xstep[-1])

    # Make it possible to chenge step alignment.
    if h_align == 'mid':
        xx -= xstep / 2.
    elif h_align == 'right':
        xx -= xstep

    # Also, duplicate each y coordinate in both arrays
    y1 = y1.repeat(2)#[:-1]
    if type(y2) == sp.ndarray:
        y2 = y2.repeat(2)#[:-1]

    # now to the plotting part:
    ax.fill_between(xx, y1, y2=y2, **kwargs)

    return ax


fname = sys.argv[1]
datf=open(fname)
time_str=[]
date_str=[]
current=[]
z=[]
time_from_zero=[]
t=0

asp=7
fig=pl.figure(figsize=(8,asp))
ax=fig.gca()

for line in datf:
	items=line.split()
	time_str.append(items[3])
	date_str.append(items[2])
	current.append(float(items[0]))
	z.append(0.0)
	time_from_zero.append(t)
	t=t+5
	

fill_between_steps(numpy.array(time_from_zero),numpy.array(z),numpy.array(current),ax=ax,color='g')
total_charge = numpy.multiply(numpy.sum(numpy.array(current)),5.0)
total_charge_str = "{:6.1f}".format(total_charge)
ax.grid()
ylim=ax.get_ylim()
ax.set_ylim([ylim[0]*1.1,max(current)*1.1])
ax.set_xlabel("Time (s) from "+time_str[0]+", "+date_str[0])
ax.set_ylabel(r"$\mu$A")
ax.set_title(r"SINQ Proton Current, Total Charge = "+total_charge_str+r" $\mu$C")
ax.set_aspect(2.0*asp/8.0)
fig.savefig(fname+".pdf",dpi=300)
pl.show()