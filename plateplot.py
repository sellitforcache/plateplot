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
elif nargs == 6:
	fname  = sys.argv[1]
	loc_x  = int(sys.argv[2])
	loc_y1 = int(sys.argv[3])
	loc_y2 = int(sys.argv[4])
	width  = int(sys.argv[5])
	plottype = "averages"
else:
	print "You must specify a filename, loc_x (pixels), loc_y1 (pixels), loc_y2 (pixels), width (total pixels, centered at 'loc_x/y')"
	exit()



### load image
img=pl.imread(fname)
if len(img.shape)==2:
	img_arraynum=1
else:
	img_arraynum=img.shape[2]

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

### main plot
plt = pl.plt
ax = plt.subplot(1,1,1)
imgplot=ax.imshow(imgmat, interpolation='bicubic', extent=[0,ext_x,0,ext_y], origin="lower")
imgplot.set_cmap("gray")
cbar=pl.colorbar(imgplot)
cbar.set_label("Counts")
ax.set_title(fname)
ax.set_xlabel("x (mm)")
ax.set_ylabel("y (mm)")
if plottype!="total":  ### do additional tasks if reqested
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