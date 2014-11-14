#! /usr/bin/env python
# Script to plot neutron image gel from BASReader in neutra lab in SINQ hall
# Ryan M. Bergmann, Nov 13, 2014.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.colors import LogNorm, PowerNorm
import sys
import numpy

### get args
nargs = len(sys.argv)
if nargs == 1:
	fname = "ninkasi.png"
	plottype = "plot"
elif nargs == 2:
	fname = sys.argv[1]
	plottype = "plot"
elif nargs==3:
	fname = sys.argv[1]
	plottype = sys.argv[2]
elif nargs == 7:
	fname  = sys.argv[1]
	plottype = sys.argv[2]
	width  = int(sys.argv[3])
	loc_x  = int(sys.argv[4])
	loc_y1 = int(sys.argv[5])
	loc_y2 = int(sys.argv[6])
else:
	print "You must specify a filename, plot type (average/3d)... "
	print "                                    ...AND for 'average': width (total pixels, centered at 'loc_x/y'), loc_x (pixels), loc_y1 (pixels), loc_y2 (pixels)"
	print "                                    ...AND for '3D'     : x1, x2, y1, y2 for the range of the surface plot"
	exit()



### load image
# get array numbers
img=pl.imread(fname)
if len(img.shape)==2:
	img_arraynum=1
else:
	img_arraynum=img.shape[2]
#collapse accordingly
if img_arraynum == 4:
	imgmat=numpy.multiply(img[:,:,0]+img[:,:,1]+img[:,:,2],img[:,:,3])
elif img_arraynum == 1:
	imgmat = img
else:
	print "Image has %d arrays, unhandled." % img_arraynum
	exit(0)

### image parameters
res   = 50.0e-6 * 1000
pix_x = imgmat.shape[1]
pix_y = imgmat.shape[0]
ext_x = pix_x * res
ext_y = pix_y * res

if plottype=="plot" or plottype=="averages":
	### main plot
	plt = pl.plt
	ax = plt.subplot(1,1,1)
	imgplot=ax.imshow(imgmat, interpolation='bicubic', extent=[0,ext_x,0,ext_y], origin="lower", cmap="spectral")#, norm=PowerNorm(1, vmin=50000, vmax=100000))
	cbar=pl.colorbar(imgplot)
	cbar.set_label("Counts")
	ax.set_title(fname)
	ax.set_xlabel("x (mm)")
	ax.set_ylabel("y (mm)")
	if plottype=="averages":  ### do additional tasks if reqested
		### calc limits
		row1_upper = loc_y1+width/2
		row1_lower = loc_y1-width/2
		row2_upper = loc_y2+width/2
		row2_lower = loc_y2-width/2
		col_upper = loc_x+width/2
		col_lower = loc_x-width/2
		### set a line at x
		ax.plot([loc_x*res,loc_x*res],[0,pix_y*res],color='r',linestyle="--")
		ax.fill_between([col_lower*res,col_upper*res],[0,0],[pix_y*res,pix_y*res],color='r',alpha=0.4)
		### set a line at y1
		ax.plot([0,pix_x*res],[loc_y1*res,loc_y1*res],color='b',linestyle="--")
		ax.fill_between([0,pix_x*res],[row1_upper*res,row1_upper*res],[row1_lower*res,row1_lower*res],color='b',alpha=0.4)
		### set a line at y2
		ax.plot([0,pix_x*res],[loc_y2*res,loc_y2*res],color='g',linestyle="--")
		ax.fill_between([0,pix_x*res],[row2_upper*res,row2_upper*res],[row2_lower*res,row2_lower*res],color='g',alpha=0.4)
		### set image extent
		ax.set_xlim([0,pix_x*res])
		ax.set_ylim([0,pix_y*res])
		### show first plot
		pl.show()
		### make vertical average plot at loc_x
		plt = pl.plt
		ax = plt.subplot(1,1,1)
		avg_y = []
		for row in range(0,pix_y):
			avg_y.append(numpy.mean(imgmat[row,col_lower:col_upper]))
		ax.plot(numpy.multiply(range(0,pix_y),res),avg_y,color='r')
		ax.set_title("Vertical average over %d pixels at x=%d" % (width,loc_x))
		ax.set_xlabel("y (mm)")
		ax.set_ylabel("Average counts")
		ax.grid("on")
		pl.show()
		### make horizontal average plot at loc_y1
		plt = pl.plt
		ax = plt.subplot(1,1,1)
		avg_x = []
		for col in range(0,pix_x):
			avg_x.append(numpy.mean(imgmat[row1_lower:row1_upper,col]))
		ax.plot(numpy.multiply(range(0,pix_x),res),avg_x,color='b')
		ax.set_title("Horizontal average over %d pixels at y=%d" % (width,loc_y2))
		ax.set_xlabel("x (mm)")
		ax.set_ylabel("Average counts")
		ax.grid("on")
		pl.show()
		### make horizontal average plot at loc_y2
		plt = pl.plt
		ax = plt.subplot(1,1,1)
		avg_x = []
		for col in range(0,pix_x):
			avg_x.append(numpy.mean(imgmat[row2_lower:row2_upper,col]))
		ax.plot(numpy.multiply(range(0,pix_x),res),avg_x,color='g')
		ax.set_title("Horizontal average over %d pixels at y=%d" % (width,loc_y2))
		ax.set_xlabel("x (mm)")
		ax.set_ylabel("Average counts")
		ax.grid("on")
		pl.show()
	else:
		pl.show()
elif plottype=="3d":
	fig = plt.figure()
	ax = Axes3D(fig)
	x = range(width, loc_x)
	y = range(loc_y1, loc_y2)
	X, Y = numpy.meshgrid(x, y)
	ax.plot_surface(X, Y, imgmat[loc_y1:loc_y2,width:loc_x],cmap=pl.cm.spectral,linewidth=0)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('Counts')
	#ax.auto_scale_xyz([width, loc_x], [loc_y1, loc_y2], [0, 65500])
	pl.show()
else:
	print "Plot type '%s' not understood." % plottype