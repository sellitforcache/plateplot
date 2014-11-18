#! /usr/bin/env python
# Script determine the azimuthal neutron flux, based on the image gel from BASReader in neutra lab in SINQ hall
# Ryan M. Bergmann, Nov 13, 2014.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.colors import LogNorm, PowerNorm
import sys
import numpy

### set image parameters
#Exit
ExitDist    = 5978.50
# TriCS
TricsFname  = "TriCS"
TricsDist   = 7358.64 
TricsCharge = 570.0   # muC
TricsAngle  = 0.218653198     # radians, approximated from the hrpt engineering drawing from Vadim
# HRPT
HrptFname   = "HRPT"
HrptDist    = 9427.64
HrptCharge  = 200.5
HrptAngle   = 0.0      # approximated from the hrpt engineering drawing from Vadim

### load images and convert data to float64
TricsMat = numpy.array(pl.imread(TricsFname),dtype=numpy.float64)
HrptMat  = numpy.array(pl.imread(HrptFname),dtype=numpy.float64)

### image parameters
res   = 50.0e-6 * 1000
TricsPix_x = TricsMat.shape[1]
TricsPix_y = TricsMat.shape[0]
TricsExt_x = TricsPix_x * res
TricsExt_y = TricsPix_y * res
HrptPix_x  =  HrptMat.shape[1]
HrptPix_y  =  HrptMat.shape[0]
HrptExt_x  =  HrptPix_x * res
HrptExt_y  =  HrptPix_y * res

### convert from log scale
TricsMat = numpy.power(10,numpy.divide(TricsMat,10000))
TricsMat = numpy.divide(TricsMat,10000)
HrptMat  = numpy.power(10,numpy.divide(HrptMat,10000))
HrptMat  = numpy.divide(HrptMat,10000)

### scale to exit intensity by r^2
TricsMat = numpy.multiply(TricsMat,numpy.power(TricsDist/ExitDist,2))
HrptMat  = numpy.multiply( HrptMat,numpy.power( HrptDist/ExitDist,2))

### scale to per unit charge on target
TricsMat = numpy.multiply(TricsMat,1.0/TricsCharge)
HrptMat  = numpy.multiply( HrptMat,1.0/ HrptCharge)

### make the average vectors and show for verification
# Trics
width = 200
row1_upper = 1500+width/2
row1_lower = 1500-width/2
plt = pl.plt
ax = plt.subplot(1,1,1)
avg_x = []
for col in range(0,TricsPix_x):
	TricsAvg_x.append(numpy.mean(TricsMat[row1_lower:row1_upper,col]))
ax.plot(numpy.multiply(range(0,TricsPix_x),res),TricsAvg_x,color='b')
ax.set_title("Trics Horizontal average over %d pixels at y=%d" % (width,loc_y1))
ax.set_xlabel("x (mm)")
ax.set_ylabel("Average counts (A.U.)")
ax.grid("on")
pl.show()
# Hrpt
width = 200
row1_upper = 2500+width/2
row1_lower = 2500-width/2
plt = pl.plt
ax = plt.subplot(1,1,1)
HrptAvg_x = []
for col in range(0,HrptPix_x):
	HrptAvg_x.append(numpy.mean(HrptMat[row1_lower:row1_upper,col]))
ax.plot(numpy.multiply(range(0,HrptPix_x),res),HrptAvg_x,color='b')
ax.set_title("Hrpt Horizontal average over %d pixels at y=%d" % (width,loc_y1))
ax.set_xlabel("x (mm)")
ax.set_ylabel("Average counts (A.U.)")
ax.grid("on")
pl.show()


### convert x to azimuthal rads


### plot and show