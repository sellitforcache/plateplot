#! /usr/bin/env python
# Script determine the azimuthal neutron flux, based on the image gel from BASReader in neutra lab in SINQ hall
# Ryan M. Bergmann, Nov 13, 2014.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.colors import LogNorm, PowerNorm
import sys
import numpy
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline

### set image parameters
#Exit
ExitDist    = 5978.50
# TriCS
TricsFname  = "TriCS"
TricsDist   = 7358.64 
TricsCharge = 570.0   # muC
TricsAngle  = 0.0     # leftmost item is 0, increasing to the right
# HRPT
HrptFname   = "HRPT"
HrptDist    = 9427.64
HrptCharge  = 200.5
HrptAngle   = 0.218653198     # radians, approximated from the hrpt engineering drawing from Vadim
# HRPT
EigerFname  = "EIGER"
EigerDist   = 6500.64 # check!!
EigerCharge = 261.0    # checked.
EigerAngle  = 3.14159 # check!!     # radians, approximated from the hrpt engineering drawing from Vadim

### load images and convert data to float64
TricsMat = numpy.array(pl.imread(TricsFname),dtype=numpy.float64)
HrptMat  = numpy.array(pl.imread(HrptFname), dtype=numpy.float64)
EigerMat = numpy.array(pl.imread(EigerFname),dtype=numpy.float64)

### image parameters
TricsRes   = 50e-6 * 1000
TricsPix_x = TricsMat.shape[1]
TricsPix_y = TricsMat.shape[0]
TricsExt_x = TricsPix_x * TricsRes
TricsExt_y = TricsPix_y * TricsRes
HrptRes    = 50e-6 * 1000
HrptPix_x  =  HrptMat.shape[1]
HrptPix_y  =  HrptMat.shape[0]
HrptExt_x  =  HrptPix_x * HrptRes
HrptExt_y  =  HrptPix_y * HrptRes
EigerRes   = 100e-6 * 1000
EigerPix_x = EigerMat.shape[1]
EigerPix_y = EigerMat.shape[0]
EigerExt_x = EigerPix_x * EigerRes
EigerExt_y = EigerPix_y * EigerRes
latitude = 5
sensitivity = 10000


### convert from log scale
TricsMat = numpy.multiply(TricsMat,latitude/65535.0)
TricsMat = numpy.power(10,TricsMat)
TricsMat = numpy.multiply(TricsMat,16.0/(latitude*sensitivity))
HrptMat  = numpy.multiply(HrptMat,latitude/65535.0)
HrptMat  = numpy.power(10,HrptMat)
HrptMat  = numpy.multiply(HrptMat,16.0/(latitude*sensitivity))
EigerMat = numpy.multiply(EigerMat,latitude/65535.0)
EigerMat = numpy.power(10,EigerMat)
EigerMat = numpy.multiply(EigerMat,16.0/(latitude*sensitivity))

### scale to exit intensity by r^2
TricsMat = numpy.multiply(TricsMat,numpy.power(TricsDist/ExitDist,2))
HrptMat  = numpy.multiply( HrptMat,numpy.power( HrptDist/ExitDist,2))
EigerMat = numpy.multiply(EigerMat,numpy.power(EigerDist/ExitDist,2))

### scale to per unit charge on target
TricsMat = numpy.multiply(TricsMat,1.0/TricsCharge)
HrptMat  = numpy.multiply( HrptMat,1.0/ HrptCharge)
EigerMat = numpy.multiply(EigerMat,1.0/EigerCharge)

### make the average vectors and show for verification
# specify linear regions
TricsRegion_x1 = 1800
TricsRegion_x2 = 2300
HrptRegion_x1  = 1800
HrptRegion_x2  = 2300
EigerRegion_x1 = 1000
EigerRegion_x2 = 1100
# Trics
width = 200
loc_y1 = 1500
row1_upper = loc_y1+width/2
row1_lower = loc_y1-width/2
plt = pl.plt
ax = plt.subplot(1,1,1)
TricsAvg_x = []
TricsX = numpy.multiply(numpy.multiply(numpy.array(range(0,TricsPix_x)),TricsRes),numpy.arctan(TricsRes/TricsDist))  # convert to rads at his arm length, linear approx for small angles
TricsX = numpy.add(TricsX,TricsAngle)  #  translate to angle
for col in range(0,TricsPix_x):
	TricsAvg_x.append(numpy.mean(TricsMat[row1_lower:row1_upper,col]))
TricsRegionX   = TricsX[    TricsRegion_x1:TricsRegion_x2]
TricsRegionAvg = TricsAvg_x[TricsRegion_x1:TricsRegion_x2]
ax.plot(TricsX,TricsAvg_x,TricsRegionX,TricsRegionAvg)
ax.set_title("Trics Horizontal average over %d pixels at y=%d" % (width,loc_y1))
ax.set_xlabel("x (mm)")
ax.set_ylabel("Average counts (A.U.)")
ax.grid("on")
pl.show()
# Hrpt
width = 200
loc_y1 = 2500
row1_upper = loc_y1+width/2
row1_lower = loc_y1-width/2
plt = pl.plt
ax = plt.subplot(1,1,1)
HrptAvg_x = []
HrptX = numpy.multiply(numpy.multiply(numpy.array(range(0,HrptPix_x)),HrptRes),numpy.arctan(HrptRes/HrptDist))  # convert to rads at his arm length, linear approx for small angles
HrptX = numpy.add(HrptX,HrptAngle)  #  translate to angle
for col in range(0,HrptPix_x):
	HrptAvg_x.append(numpy.mean(HrptMat[row1_lower:row1_upper,col]))
HrptRegionX    = HrptX[     HrptRegion_x1: HrptRegion_x2]
HrptRegionAvg  = HrptAvg_x[ HrptRegion_x1: HrptRegion_x2]
ax.plot(HrptX,HrptAvg_x,HrptRegionX,HrptRegionAvg)
ax.set_title("Hrpt Horizontal average over %d pixels at y=%d" % (width,loc_y1))
ax.set_xlabel("x (mm)")
ax.set_ylabel("Average counts (A.U.)")
ax.grid("on")
pl.show()
# Eiger
width = 200
loc_y1 = 1500
row1_upper = loc_y1+width/2
row1_lower = loc_y1-width/2
plt = pl.plt
ax = plt.subplot(1,1,1)
EigerAvg_x = []
EigerX = numpy.multiply(numpy.multiply(numpy.array(range(0,EigerPix_x)),EigerRes),numpy.arctan(EigerRes/EigerDist))  # convert to rads at his arm length, linear approx for small angles
EigerX = numpy.add(EigerX,EigerAngle)  #  translate to angle
for col in range(0,EigerPix_x):
	EigerAvg_x.append(numpy.mean(EigerMat[row1_lower:row1_upper,col]))
EigerRegionX   = EigerX[    EigerRegion_x1:EigerRegion_x2]
EigerRegionAvg = EigerAvg_x[EigerRegion_x1:EigerRegion_x2]
ax.plot(EigerX,EigerAvg_x,EigerRegionX,EigerRegionAvg)
ax.set_title("Eiger Horizontal average over %d pixels at y=%d" % (width,loc_y1))
ax.set_xlabel("x (mm)")
ax.set_ylabel("Average counts (A.U.)")
ax.grid("on")
pl.show()

### extent selection and curve fit 
xdata=numpy.hstack([TricsRegionX,  HrptRegionX  ,EigerRegionX])
ydata=numpy.hstack([TricsRegionAvg,HrptRegionAvg,EigerRegionAvg])
def func1(x,a,b):
	return a*x + b
def func2(x,a,b,c):
	return a*x*x + b*x + c
def func3(x,a,b,c,d):
	return a*x*x*x + b*x*x + c*x + d
popt1, pcov1 = curve_fit(func1, xdata, ydata)
popt2, pcov2 = curve_fit(func2, xdata, ydata)
popt3, pcov3 = curve_fit(func3, xdata, ydata)
#s = UnivariateSpline(xdata, ydata, k=2)
FuncX   = numpy.linspace(0.0,EigerX[-1],1000)
FuncY1 = func1(FuncX,popt1[0],popt1[1])
FuncY2 = func2(FuncX,popt2[0],popt2[1],popt2[2])
FuncY3 = func3(FuncX,popt3[0],popt3[1],popt3[2],popt3[3])
#FuncYs  = s(FuncX)

### plot and show
p1 = pl.plot(TricsRegionX,TricsRegionAvg,  label='TriCS Data')
p2 = pl.plot( HrptRegionX, HrptRegionAvg,  label= 'HRPT Data')
p3 = pl.plot(EigerRegionX,EigerRegionAvg,  label='EIGER Data')
p4 = pl.plot(FuncX,FuncY1,                 label='Curve Fit to 1st-Order Polynomial')
p5 = pl.plot(FuncX,FuncY2,                 label='Curve Fit to 2nd-Order Polynomial')
p6 = pl.plot(FuncX,FuncY3,                 label='Curve Fit to 3rd-Order Polynomial')
pl.grid()
pl.legend()
fig=pl.gcf()
ax=fig.gca()
ax.set_xlabel('Degrees from TriCS (radians)')
ax.set_ylabel('Flux (A.U)')
pl.show()