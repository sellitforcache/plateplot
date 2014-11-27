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
plt.rc('font', size=12)

### static parameters 
au198_HL 		= 2.69517 # days
au198_lambda 	= numpy.log(2)/2.69517 # 1/days

### data for gold foil 1, cadmium, epithermal flux
gf1_charge	 		= 64652.5  # muC, from plotbeam
gf1_irr_time    	= 0.0
gf1_mea_time		= 0.0  #?
gf1_activity		= numpy.array([34.0 ,36.0, 33.0,34.0, 36.0,39.0, 42.0, 48.0, 40.0 ])
gf1_mass			= numpy.array([29.32,29.01,24.7,27.23,30.9,31.21,32.27,31.15,30.24])
gf1_xposition		= [0,1,2,0,1,2,0,1,2]
gf1_yposition		= [0,0,0,1,1,1,2,2,2]

### data for gold foil 2,  WARM silicon
gf2_charge	 		= 64278.5  # muC, from plotbeam
gf2_irr_time    	= 0.0
gf2_mea_time		= 0.0  #?
gf2_activity		= numpy.array([530.0,460.0,440.0,490.0,525.0,495.0,545.0,530.0,475.0])
gf2_mass			= numpy.array([31.45,27.92,28.65,29.53,31.24,32.15,32.30,30.82,31.02])
gf2_xposition		= [0,1,2,0,1,2,0,1,2]
gf2_yposition		= [0,0,0,1,1,1,2,2,2]

### data for gold foil 3,  COLD silicon
gf3_charge	 		= 92894.5  # muC, from plotbeam
gf3_irr_time    	= 0.0
gf3_mea_time		= 0.0  #?
gf3_activity		= numpy.array([895.0,885.0,810.0,910.0,895.0,785.0,805.0,795.0,840.0])
gf3_mass			= numpy.array([31.05,30.84,31.67,31.55,30.96,30.00,41.07,41.04,41.29])
gf3_xposition		= [0,1,2,0,1,2,0,1,2]
gf3_yposition		= [0,0,0,1,1,1,2,2,2]

### correct activity back to end of irradiation
gf1_activity = numpy.multiply( gf1_activity , numpy.exp( au198_lambda * (gf1_mea_time - gf1_irr_time) ) )
gf2_activity = numpy.multiply( gf2_activity , numpy.exp( au198_lambda * (gf2_mea_time - gf2_irr_time) ) )
gf3_activity = numpy.multiply( gf3_activity , numpy.exp( au198_lambda * (gf3_mea_time - gf3_irr_time) ) )

### get specific activity
gf1_spec_activity = numpy.divide( gf1_activity , gf1_mass)
gf2_spec_activity = numpy.divide( gf2_activity , gf2_mass)
gf3_spec_activity = numpy.divide( gf3_activity , gf3_mass)

### get specific activity per charge
gf1_spec_activity_percharge = numpy.divide( gf1_spec_activity , gf1_charge)
gf2_spec_activity_percharge = numpy.divide( gf2_spec_activity , gf2_charge)
gf3_spec_activity_percharge = numpy.divide( gf3_spec_activity , gf3_charge)

### convert from Bq to muBq
gf1_spec_activity_percharge = numpy.multiply( gf1_spec_activity_percharge , 1e6)
gf2_spec_activity_percharge = numpy.multiply( gf2_spec_activity_percharge , 1e6)
gf3_spec_activity_percharge = numpy.multiply( gf3_spec_activity_percharge , 1e6)

### find maximum
ymax = numpy.max([gf1_spec_activity_percharge.max(),gf3_spec_activity_percharge.max(),gf3_spec_activity_percharge.max()])

### plot results in grid
fig, axarr = plt.subplots(3, 3)
width=0.1
for ind in range(len(gf1_xposition)):
	axarr[gf1_yposition[ind], gf1_xposition[ind]].bar(      0.0, gf1_spec_activity_percharge[ind], width, color='r')
	axarr[gf2_yposition[ind], gf2_xposition[ind]].bar(    width, gf2_spec_activity_percharge[ind], width, color='g')
	axarr[gf3_yposition[ind], gf3_xposition[ind]].bar(2.0*width, gf3_spec_activity_percharge[ind], width, color='b')
	axarr[gf1_yposition[ind], gf1_xposition[ind]].set_title('(%d,%d) Warm vs Cold = %f'% (gf1_yposition[ind], gf1_xposition[ind], gf3_spec_activity_percharge[ind]/gf2_spec_activity_percharge[ind] - 1.0))
	axarr[gf1_yposition[ind], gf1_xposition[ind]].legend(['Epithermal','Total, Warm','Total, Cold'],loc=2,prop={'size':10})
	axarr[gf1_yposition[ind], gf1_xposition[ind]].grid()
	axarr[gf1_yposition[ind], gf1_xposition[ind]].set_ylim([0.0,1.1*ymax])
pl.suptitle(r"Gold Foil Irradiation at TriCS, Nov 13, 2014.  Units in $\mu$Bq $\mu$C$^{-1}$ mg$^{-1}$")
pl.show()

### make 'images'
gf1_img = numpy.zeros((3,3))
gf2_img = numpy.zeros((3,3))
gf3_img = numpy.zeros((3,3))
for ind in range(len(gf1_spec_activity)):
	gf1_img[gf1_yposition[ind], gf1_xposition[ind]] = gf1_spec_activity_percharge[ind]
	gf2_img[gf2_yposition[ind], gf2_xposition[ind]] = gf2_spec_activity_percharge[ind]
	gf3_img[gf3_yposition[ind], gf3_xposition[ind]] = gf3_spec_activity_percharge[ind]

### plot individual distributions on 3x3 square, same scale
fig, axarr = plt.subplots(1, 3)
im=axarr[0].imshow(gf1_img,interpolation='None',vmin=0,vmax=ymax)
axarr[0].set_title('Epithermal')
axarr[1].imshow(gf2_img,interpolation='None',vmin=0,vmax=ymax)
axarr[1].set_title('Total, Warm')
axarr[2].imshow(gf3_img,interpolation='None',vmin=0,vmax=ymax)
axarr[2].set_title('Total, Cold')
cbar=pl.colorbar(im,ax=axarr[2])
cbar.set_label(r"$\mu$Bq $\mu$C$^{-1}$ mg$^{-1}$")
pl.show()

### plot individual distributions on 3x3 square, own scales
fig, axarr = plt.subplots(1, 3)
im=axarr[0].imshow(gf1_img,interpolation='None')
axarr[0].set_title('Epithermal')
cbar=pl.colorbar(im,ax=axarr[0])
cbar.set_label(r"$\mu$Bq $\mu$C$^{-1}$ mg$^{-1}$")
im=axarr[1].imshow(gf2_img,interpolation='None')
axarr[1].set_title('Total, Warm')
cbar=pl.colorbar(im,ax=axarr[1])
cbar.set_label(r"$\mu$Bq $\mu$C$^{-1}$ mg$^{-1}$")
im=axarr[2].imshow(gf3_img,interpolation='None')
axarr[2].set_title('Total, Cold')
cbar=pl.colorbar(im,ax=axarr[2])
cbar.set_label(r"$\mu$Bq $\mu$C$^{-1}$ mg$^{-1}$")
pl.show()