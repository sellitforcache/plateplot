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

if fname=="TriCS":
	beamdim=[40,150] #in mm
	center=[100,96]
elif fname=="HRPT":
	beamdim=[40,150]   #in mm
	center=[100,146]

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

### convert data to float64
imgmat = numpy.array(imgmat,dtype=numpy.float64)

### image parameters
res   = 50.0e-6 * 1000
pix_x = imgmat.shape[1]
pix_y = imgmat.shape[0]
ext_x = pix_x * res
ext_y = pix_y * res

### convert from log scale
imgmat=numpy.power(10,numpy.divide(imgmat,10000))
imgmat=numpy.divide(imgmat,10000)

if plottype=="plot" or plottype=="averages" or plottype=="total_average":
	### main plot
	f=pl.figure(figsize=(ext_x*1.3*0.03,ext_y*0.03))
	ax=f.gca()
	imgplot=pl.imshow(imgmat, interpolation='bicubic', extent=[0,ext_x,0,ext_y], origin="lower", cmap="spectral")#, norm=PowerNorm(1, vmin=50000, vmax=100000))
	cbar=pl.colorbar(imgplot)
	cbar.set_label("Counts (A.U.)")
	ax.set_title(fname)
	ax.set_xlabel("x (mm)")
	ax.set_ylabel("y (mm)")
	#ax.set_aspect(pix_y/pix_x)
	#fig.set_size_inches(18.5,5.0)
	if plottype=="averages":  ### do additional tasks if reqested
		### calc limits
		row1_upper = loc_y1+width/2
		row1_lower = loc_y1-width/2
		row2_upper = loc_y2+width/2
		row2_lower = loc_y2-width/2
		col_upper  = loc_x +width/2
		col_lower  = loc_x -width/2
		### set a line at x
		ax.plot([loc_x*res,loc_x*res],[0,pix_y*res],color='r',linestyle="--")
		ax.fill_between([col_lower*res,col_upper*res],[0,0],[pix_y*res,pix_y*res],color='r',alpha=0.4)
		### set a line at y1
		ax.plot([0,pix_x*res],[loc_y1*res,loc_y1*res],color='b',linestyle="--")
		ax.fill_between([0,pix_x*res],[row1_upper*res,row1_upper*res],[row1_lower*res,row1_lower*res],color='b',alpha=0.4)
		### set a line at y2
		ax.plot([0,pix_x*res],[loc_y2*res,loc_y2*res],color='g',linestyle="--")
		ax.fill_between([0,pix_x*res],[row2_upper*res,row2_upper*res],[row2_lower*res,row2_lower*res],color='g',alpha=0.4)
		### make white box for beamline
		try:
			beam_y1=center[1]-beamdim[1]/2
			beam_y2=center[1]+beamdim[1]/2
			beam_x1=center[0]-beamdim[0]/2
			beam_x2=center[0]+beamdim[0]/2
			ax.plot([beam_x1,beam_x2,beam_x2,beam_x1,beam_x1],[beam_y1,beam_y1,beam_y2,beam_y2,beam_y1],color='w',alpha=1)
		except NameError:
			pass
		### set image extent
		ax.set_xlim([0,pix_x*res])
		ax.set_ylim([0,pix_y*res])
		### save and show first plot
		fig=ax.get_figure()
		#fig.tight_layout()
		fig.set_frameon(False)
		fig.savefig(fname+"_fig.pdf",dpi=300)
		pl.show()
		### make vertical average plot at loc_x
		plt = pl.plt
		ax = plt.subplot(1,1,1)
		avg_y = []
		for row in range(0,pix_y):
			avg_y.append(numpy.mean(imgmat[row,col_lower:col_upper]))
		ax.plot(numpy.multiply(range(0,pix_y),res),avg_y,color='r',label="at x = %d mm"%(loc_x*res))
		ax.set_title("Vertical average over %d pixels" % width)
		ax.set_xlabel("y (mm)")
		ax.set_ylabel("Average counts (A.U.)")
		ax.grid("on")
		ax.legend()
		fig=ax.get_figure()
		fig.savefig(fname+"_vert.pdf",dpi=300)
		old_axis=ax.axis()
		if fname=="TriCS":
			ax.axis([50.0,150.0,100,130])
		elif fname=="HRPT":
			ax.axis([60.0,230.0,23,30])
		fig.savefig(fname+"_vert_zoom.pdf",dpi=300)
		ax.axis(old_axis)
		pl.show()
		### make horizontal average plot at loc_y1
		plt = pl.plt
		ax = plt.subplot(1,1,1)
		avg_x = []
		for col in range(0,pix_x):
			avg_x.append(numpy.mean(imgmat[row1_lower:row1_upper,col]))
		ax.plot(numpy.multiply(range(0,pix_x),res),avg_x,color='b',label="at y = %d mm"%(loc_y1*res))
		#ax.set_title("Horizontal average over %d pixels at y=%d" % (width,loc_y1))
		#ax.set_xlabel("x (mm)")
		#ax.set_ylabel("Average counts (A.U.)")
		#ax.grid("on")
		#fig=ax.get_figure()
		#fig.savefig(fname+"_horiz1.pdf",dpi=300)
		#old_axis=ax.axis()
		#if fname=="TriCS":
		#	ax.axis([70.0,130.0,100,130])
		#elif fname=="HRPT":
		#	ax.axis([70.0,130.0,23,30])
		#fig.savefig(fname+"_horiz1_zoom.pdf",dpi=300)
		#ax.axis(old_axis)
		#pl.show()
		### make horizontal average plot at loc_y2
		#plt = pl.plt
		#ax = plt.subplot(1,1,1)
		avg_x = []
		for col in range(0,pix_x):
			avg_x.append(numpy.mean(imgmat[row2_lower:row2_upper,col]))
		ax.plot(numpy.multiply(range(0,pix_x),res),avg_x,color='g',label="at y = %d mm"%(loc_y2*res))
		ax.set_title("Horizontal average over %d pixels"%width)
		ax.set_xlabel("x (mm)")
		ax.set_ylabel("Average counts (A.U.)")
		ax.legend()
		ax.grid("on")
		fig=ax.get_figure()
		fig.savefig(fname+"_horiz.pdf",dpi=300)
		old_axis=ax.axis()
		if fname=="TriCS":
			ax.axis([70.0,130.0,100,130])
		elif fname=="HRPT":
			ax.axis([70.0,130.0,23,30])
		fig.savefig(fname+"_horiz_zoom.pdf",dpi=300)
		ax.axis(old_axis)
		pl.show()
	elif plottype=="total_average":
		loc_x2=loc_x
		loc_x1=width
		### show block
		ax.fill_between([loc_x1*res,loc_x2*res],[loc_y1*res,loc_y1*res],[loc_y2*res,loc_y2*res],color='k',alpha=0.6)
		### set image extent
		ax.set_xlim([0,pix_x*res])
		ax.set_ylim([0,pix_y*res])
		### calculate entire mean
		blockmean = numpy.mean(imgmat[loc_y1:loc_y2,loc_x1:loc_x2])
		ax.set_title(fname+" BLOCK AVG (A.U.) = %f"%blockmean)
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