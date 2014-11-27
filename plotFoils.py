#! /usr/bin/env python
# Script to plot gold foil activation results
# Ryan M. Bergmann, Nov 27, 2014.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.colors import LogNorm, PowerNorm, Normalize
import sys
import numpy
import re

### set TeX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

### static parameters 
au198_lambda = 2.69517 # days

### data for gold foil 1, cadmium, epithermal flux
gf1_irr_fluence 	= 64652.5  # muC, from plotbeam
gf1_irr_time    	= 0.0
gf1_mea_time		= 0.0  #?
gf1_activity		= numpy.array([34.0 ,36.0, 33.0,34.0, 36.0,39.0, 42.0, 48.0, 40.0 ])
gf1_mass			= numpy.array([29.32,29.01,24.7,27.23,30.9,31.21,32.27,31.15,30.24])
gf1_xposition		= [1,2,3,1,2,3,1,2,3]
gf1_yposition		= [3,3,3,2,2,2,1,1,1]

### data for gold foil 2,  WARM silicon
gf2_irr_fluence 	= 64278.5  # muC, from plotbeam
gf2_irr_time    	= 0.0
gf2_mea_time		= 0.0  #?
gf2_activity		= numpy.array([530.0,460.0,440.0,490.0,525.0,495.0,545.0,530.0,475.0])
gf2_mass			= numpy.array([31.45,27.92,28.65,29.53,31.24,32.15,32.30,30.82,31.02])
gf2_xposition		= [1,2,3,1,2,3,1,2,3]
gf2_yposition		= [3,3,3,2,2,2,1,1,1]

### data for gold foil 3,  COLD silicon
gf3_irr_fluence 	= 92894.5  # muC, from plotbeam
gf3_irr_time    	= 0.0
gf3_mea_time		= 0.0  #?
gf3_activity		= numpy.array([895.0,885.0,810.0,910.0,895.0,785.0,805.0,795.0,840.0])
gf3_mass			= numpy.array([31.05,30.84,31.67,31.55,30.96,30.00,41.07,41.04,41.29])
gf3_xposition		= [1,2,3,1,2,3,1,2,3]
gf3_yposition		= [3,3,3,2,2,2,1,1,1]

### correct activity back to end of irradiation



### get specific activity


###