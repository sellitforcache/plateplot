#! /usr/bin/env python

import pylab as pl
import sys
import numpy

### get args
nargs = len(sys.argv)
if nargs == 1:
	fname = "ninkasi.png"
	plottype = "total"
elif nargs == 2:
	fname = sys.argv[1]
	plottype = "total"
elif nargs == 5:
	fname = sys.argv[1]
	loc_x = int(sys.argv[2])
	loc_y = int(sys.argv[3])
	width = int(sys.argv[4])
	plottype = "average"
else:
	print "You must specify a filename, loc_x (pixels), loc_y (pixels), width (total pixels, centered at 'loc_x/y')"
	exit()



### load image
img=pl.imread(fname)
imgmat=numpy.multiply(img[:,:,0]+img[:,:,1]+img[:,:,2],img[:,:,3])

### image parameters
res = 50.0e-6
pix_x = imgmat.shape[1]
pix_y = imgmat.shape[0]
ext_x = pix_x * res
ext_y = pix_y * res

### main plot
plt = pl.plt
ax = plt.subplot(1,1,1)
imgplot=ax.imshow(imgmat, interpolation='bicubic')
imgplot.set_cmap("gray")
cbar=pl.colorbar(imgplot)
cbar.set_label("Counts")
ax.set_title(fname)
ax.set_xlabel("x (cm)")
ax.set_ylabel("y (cm)")
if plottype!="total":  ### do additional tasks if reqested
	### calc limits
	row_upper = loc_y+width/2
	row_lower = loc_y-width/2
	col_upper = loc_x+width/2
	col_lower = loc_x-width/2
	### set a line at x
	ax.plot([loc_x,loc_x],[0,pix_y],color='r')
	ax.fill_between([col_lower,col_upper],[0,0],[pix_y,pix_y],color='r',alpha=0.5)
	### set a line at y
	ax.plot([0,pix_x],[loc_y,loc_y],color='b')
	ax.fill_between([0,pix_x],[row_upper,row_upper],[row_lower,row_lower],color='b',alpha=0.5)
	### set image extent
	ax.set_xlim([0,pix_x])
	ax.set_ylim([0,pix_y])
	### show first plot
	pl.show()
	### make horizontal average plot at loc_y
	plt = pl.plt
	ax = plt.subplot(1,1,1)
	avg_x = []
	for col in range(0,pix_x):
		avg_x.append(numpy.mean(imgmat[row_lower:row_upper,col]))
	ax.plot(range(0,pix_x),avg_x,color='b')
	ax.set_title("horizontal average")
	ax.set_xlabel("x")
	ax.set_ylabel("average counts over %d pixels"%width)
	ax.grid("on")
	pl.show()
	### make vertical average plot at loc_x
	plt = pl.plt
	ax = plt.subplot(1,1,1)
	avg_y = []
	for row in range(0,pix_y):
		avg_y.append(numpy.mean(imgmat[row,col_lower:col_upper]))
	ax.plot(range(0,pix_y),avg_y,color='r')
	ax.set_title("vertical average")
	ax.set_xlabel("y")
	ax.set_ylabel("average counts over %d pixels"%width)
	ax.grid("on")
	pl.show()
else:
	pl.show()