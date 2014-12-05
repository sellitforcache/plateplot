#! /usr/bin/env python
# Script to plot neutron image gel from BASReader in neutra lab in SINQ hall
# Ryan M. Bergmann, Nov 13, 2014.  ryan.bergmann@psi.ch, ryanmbergmann@gmail.com

import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib.colors import LogNorm, PowerNorm, Normalize
from matplotlib import cm
import sys
import numpy
import re

### set TeX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=16)

def draw_foils(ax,origin=[0,0,0]):
	d2d 	= 11.0
	dia 	= 10.0
	r   	= dia/2.0 
	res 	= 200
	a    	= numpy.linspace(0,2.0*numpy.pi,res)
	centers = [[origin[0]-d2d,origin[1]+d2d],[origin[0],origin[1]+d2d],[origin[0]+d2d,origin[1]+d2d],[origin[0]-d2d,origin[1]],[origin[0],origin[1]],[origin[0]+d2d,origin[1]],[origin[0]-d2d,origin[1]-d2d],[origin[0],origin[1]-d2d],[origin[0]+d2d,origin[1]-d2d]]
	for c in centers:
		x = r*numpy.sin(a) + c[0]
		y = r*numpy.cos(a) + c[1]
		ax.plot(x,y,color='w')

def convert2lin(imgmat,latitude,sensitivity):
	imgmat=numpy.multiply(imgmat,latitude/65535.0)
	imgmat=numpy.power(10,imgmat)
	imgmat=numpy.multiply(imgmat,16.0/(latitude*sensitivity))
	return imgmat

def read_mcstats_dat(fname,res_x,res_y,pix_x,pix_y,ext_x,ext_y):
	mcfile=open(fname)
	line = mcfile.readline()
	a=re.match("# *([a-zA-Z0-9.+_]+): *([a-zA-Z0-9.+_\- ,\(\)]+)",line)
	while a:
		#print a.group(1)
		if a.group(1)=="xylimits":
			substr = a.group(2).split()
			ext_x = (float(substr[1])-float(substr[0]))*10.0 #most likely cm to mm, BE SURE TO CHECK in the file by hand. this script does not read it!
			ext_y = (float(substr[3])-float(substr[2]))*10.0
			print "extent x/y", ext_x, ext_y
		elif a.group(1)=="type":
			#print a.group(2)
			typedata=re.match(" *([a-zA-Z0-9+\-._ ]+)\( *([0-9]+), *([0-9]+)\)",a.group(2))
			pix_x = int(typedata.group(2))
			pix_y = int(typedata.group(3))
			print "datatype",typedata.group(1)," pix_x/y",pix_x,pix_y
		line = mcfile.readline()
		a=re.match("# *([a-zA-Z0-9.+_]+): *([a-zA-Z0-9.+_\- ,\(\)]+)",line)
	# now in the data
	data=[]
	for row in range(pix_y):
		nums = line.split()
		data.append(numpy.array(nums,dtype=numpy.float64))
		line = mcfile.readline()
	res_y = ext_y/pix_y
	res_x = ext_x/pix_x
	return numpy.array(data),res_x,res_y,pix_x,pix_y,ext_x,ext_y 


def read_tiff(fname,res_x,res_y,pix_x,pix_y,ext_x,ext_y):
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
	pix_x = imgmat.shape[1]
	pix_y = imgmat.shape[0]
	ext_x = pix_x * res_x
	ext_y = pix_y * res_y

	### convert to linear
	imgmat = convert2lin(imgmat,latitude,sensitivity)

	### return final image
	return imgmat,res_x,res_y,pix_x,pix_y,ext_x,ext_y



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
res_x = res_y=0.0
pix_x=0
pix_y=0
ext_x=0.0
ext_y=0.0
lower_limit=0.5
if fname=="TriCS":
	total_current = 570.0  # muC
	beamdim=[40,80] #in mm
	center=[105,99]
	res_x = res_y = 50.0e-6 * 1000  # microns to mm
	latitude= 5
	sensitivity= 10000
	imgmat,res_x,res_y,pix_x,pix_y,ext_x,ext_y = read_tiff(fname,res_x,res_y,pix_x,pix_y,ext_x,ext_y)
	imgmat=numpy.divide(imgmat,total_current/1000.0)   # to mC
	imgmat[imgmat<lower_limit]=0.0
elif fname=="HRPT":
	total_current = 200.5  # muC
	beamdim=[40,150]   #in mm
	center=[100,145.25]
	res_x = res_y = 50.0e-6 * 1000 # microns to mm
	latitude= 5
	sensitivity= 10000
	imgmat,res_x,res_y,pix_x,pix_y,ext_x,ext_y = read_tiff(fname,res_x,res_y,pix_x,pix_y,ext_x,ext_y)
	imgmat=numpy.divide(imgmat,total_current/1000.0)   # to mC
elif fname=="EIGER":
	total_current = 261.0  # muC
	beamdim=[60,300]   #in mm
	center=[101,215]
	res_x = res_y = 100.0e-6 * 1000  #microns to mm
	sensitivity= 10000
	latitude= 5
	imgmat,res_x,res_y,pix_x,pix_y,ext_x,ext_y = read_tiff(fname,res_x,res_y,pix_x,pix_y,ext_x,ext_y)
	imgmat=numpy.divide(imgmat,total_current/1000.0)   # to mC
else:
	a=re.match("eiger_mcstas/([a-zA-Z0-9.+\-_ ]+)",fname)
	if a:
		imgmat,res_x,res_y,pix_x,pix_y,ext_x,ext_y = read_mcstats_dat(fname,res_x,res_y,pix_x,pix_y,ext_x,ext_y)
		beamdim=[60,300]   #in mm
		center=[100,200]
		sensitivity= 10000
		latitude=5
	else:
		print "uhoh"

#print imgmat
print ext_x,ext_y,pix_x,pix_y,res_x,res_y
print "min",numpy.min(imgmat),"max",numpy.max(imgmat)


if plottype=="plot" or plottype=="averages" or plottype=="total_average":
	### main plot
	f=pl.figure(figsize=(ext_x*1.3*0.03,ext_y*0.03))
	ax=f.gca()
	my_cmap = cm.get_cmap('spectral')
	my_cmap.set_under('w')
	imgplot=pl.imshow(imgmat, interpolation='bicubic', extent=[0,ext_x,0,ext_y], origin="lower", cmap=my_cmap)#, norm=PowerNorm(1, vmin=50000, vmax=100000))
	imgplot.set_clim(lower_limit,numpy.max(imgmat))
	cbar=pl.colorbar(imgplot)
	cbar.set_label(r"Counts (A.U. / mA$\cdot$s)")
	ax.set_title(fname.replace(r"_",r'\_'))
	ax.set_xlabel(r"x (mm)")
	ax.set_ylabel(r"y (mm)")
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
		ax.plot([loc_x*res_x,loc_x*res_x],[0,pix_y*res_y],color='r',linestyle="--")
		ax.fill_between([col_lower*res_x,col_upper*res_x],[0,0],[pix_y*res_y,pix_y*res_y],color='r',alpha=0.4)
		### set a line at y1
		ax.plot([0,pix_x*res_x],[loc_y1*res_y,loc_y1*res_y],color='b',linestyle="--")
		ax.fill_between([0,pix_x*res_x],[row1_upper*res_y,row1_upper*res_y],[row1_lower*res_y,row1_lower*res_y],color='b',alpha=0.4)
		### set a line at y2
		ax.plot([0,pix_x*res_x],[loc_y2*res_y,loc_y2*res_y],color='g',linestyle="--")
		ax.fill_between([0,pix_x*res_x],[row2_upper*res_y,row2_upper*res_y],[row2_lower*res_y,row2_lower*res_y],color='g',alpha=0.4)
		### make white box for beamline
		try:
			beam_y1=center[1]-beamdim[1]/2
			beam_y2=center[1]+beamdim[1]/2
			beam_x1=center[0]-beamdim[0]/2
			beam_x2=center[0]+beamdim[0]/2
			ax.plot([beam_x1,beam_x2,beam_x2,beam_x1,beam_x1],[beam_y1,beam_y1,beam_y2,beam_y2,beam_y1],color='w',alpha=1)
		except NameError:
			pass
		### plot the foil positions, origin in mm
		draw_foils(ax,origin=center)
		### set image extent
		ax.set_xlim([0,pix_x*res_x])
		ax.set_ylim([0,pix_y*res_y])
		### save and show first plot
		fig=ax.get_figure()
		#fig.tight_layout()
		fig.set_frameon(False)
		fig.savefig(fname+"_fig.pdf",dpi=300)
		### zoom into the port area
		old_axis=ax.axis()
		if fname=="TriCS":
			ax.axis([center[0]-beamdim[0]/1.9,center[0]+beamdim[0]/1.9,center[1]-beamdim[1]/1.9,center[1]+beamdim[1]/1.9])
		elif fname=="HRPT":
			ax.axis([60.0,230.0,4,5])
		fig.savefig(fname+"_fig_zoom.pdf",dpi=300)
		ax.axis(old_axis)
		pl.show()
		### make vertical average plot at loc_x
		plt = pl.plt
		ax = plt.subplot(1,1,1)
		avg_y = []
		for row in range(0,pix_y):
			avg_y.append(numpy.mean(imgmat[row,col_lower:col_upper]))
		p_avg =ax.plot(numpy.multiply(range(0,pix_y),res_y),avg_y,color='r',label="x = %d mm"%(loc_x*res_x))
		v_lims=ax.get_ylim()
		## plot beam ports
		p_beam=ax.plot([beam_y1,beam_y1],[v_lims[0],1.2*v_lims[1]],color='k',linestyle='-')  
		p_beam=ax.plot([beam_y2,beam_y2],[v_lims[0],1.2*v_lims[1]],color='k',linestyle='-')
		p_wire=ax.plot([center[1],center[1]],[v_lims[0],1.2*v_lims[1]],color='fuchsia',linestyle='--')
		## make legend
		pl.legend([p_avg[0],p_beam[0],p_wire[0]],["x = %d mm"%(loc_x*res_x),"Port boundary","Cd wire"],loc=1,prop={'size':12}, fancybox=True, framealpha=0.5)
		#ax.set_title("Vertical average over %d pixels" % width)
		ax.set_xlabel("y (mm)")
		ax.set_ylabel(r"Counts (A.U. / mA$\cdot$s)")
		ax.set_xlim([0,ext_y])
		ax.grid("on")
		#ax.legend()
		fig=ax.get_figure()
		fig.savefig(fname+"_vert.pdf",dpi=300)
		old_axis=ax.axis()
		if fname=="TriCS":
			ax.axis([50.0,150.0,11,30])
		elif fname=="HRPT":
			ax.axis([60.0,230.0,4,5])
		## plot region boundaries AFTER MAIN SAVE.
		p_b1=ax.plot([55,55],  [15,27],color='c',linestyle='-')  
		p_b2=ax.plot([67,67],  [15,27],color='c',linestyle='-')
		p_b3=ax.plot([131,131],[15,27],color='c',linestyle='-')
		p_b3=ax.plot([146,146],[15,27],color='c',linestyle='-')
		## mark regions boundaries
		props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
		ax.text(57,   16, r"\begin{center} Region \\ 1 \end{center}",bbox=props,fontsize=12)
		ax.text(85,   16, r"\begin{center} Region \\ 2 \end{center}",bbox=props,fontsize=12)
		ax.text(133,  16, r"\begin{center} Region \\ 3 \end{center}",bbox=props,fontsize=12)
		## legend
		pl.legend( [p_avg[0],p_beam[0],p_wire[0],p_b1[0]],["x = %d mm"%(loc_x*res_x),"Port boundary","Cd wire","Region boundary"],loc=1,prop={'size':12}, fancybox=True, framealpha=1.0)
		fig.savefig(fname+"_vert_zoom.pdf",dpi=300)
		ax.axis(old_axis)
		pl.show()
		### make horizontal average plot at loc_y1
		plt = pl.plt
		ax = plt.subplot(1,1,1)
		avg_x = []
		for col in range(0,pix_x):
			avg_x.append(numpy.mean(imgmat[row1_lower:row1_upper,col]))
		p_avg1=ax.plot(numpy.multiply(range(0,pix_x),res_x),avg_x,color='b',label="y = %d mm"%(loc_y1*res_y))
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
		p_avg2=ax.plot(numpy.multiply(range(0,pix_x),res_x),avg_x,color='g',label="y = %d mm"%(loc_y2*res_y))
		v_lims=ax.get_ylim()
		p_beam=ax.plot([beam_x1,beam_x1],[v_lims[0],v_lims[1]],color='k',linestyle='-')  ##plot beam ports
		p_beam=ax.plot([beam_x2,beam_x2],[v_lims[0],v_lims[1]],color='k',linestyle='-')
		## legend
		pl.legend( [p_avg1[0],p_avg2[0],p_beam[0]],["y = %d mm"%(loc_y1*res_y),"y = %d mm"%(loc_y2*res_y),"Port boundary"],loc=1,prop={'size':12}, fancybox=True, framealpha=1.0)
		## title, etc
		#ax.set_title("Horizontal average over %d pixels"%width)
		ax.set_xlabel("x (mm)")
		ax.set_ylabel(r"Counts (A.U. / mA$\cdot$s)")
		ax.grid("on")
		ax.set_xlim([0,ext_x])
		fig=ax.get_figure()
		fig.savefig(fname+"_horiz.pdf",dpi=300)
		old_axis=ax.axis()
		if fname=="TriCS":
			ax.axis([70.0,130.0,11,30])
		elif fname=="HRPT":
			ax.axis([60.0,140.0,3.8,5])
		## plot region boundaries AFTER MAIN SAVE.
		p_b1=ax.plot([75,75],  [15,27],color='c',linestyle='-')  
		p_b2=ax.plot([88,88],  [15,27],color='c',linestyle='-')
		p_b3=ax.plot([118,118],[15,27],color='c',linestyle='-')
		p_b3=ax.plot([125,125],[15,27],color='c',linestyle='-')
		## mark regions boundaries
		props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
		ax.text(78,   16, r"\begin{center} Region \\ 1 \end{center}",bbox=props,fontsize=12)
		ax.text(100,  16, r"\begin{center} Region \\ 2 \end{center}",bbox=props,fontsize=12)
		ax.text(119,  16, r"\begin{center} Region \\ 3 \end{center}",bbox=props,fontsize=12)
		## legend
		pl.legend( [p_avg1[0],p_avg2[0],p_beam[0],p_b1[0]],["y = %d mm"%(loc_y1*res_y),"y = %d mm"%(loc_y2*res_y),"Port boundary","Region boundary"],loc=2,prop={'size':12}, fancybox=True, framealpha=1.0)
		## save zoomed
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
		ax.set_title(fname+r" BLOCK AVG (A.U. / mA$\cdot$s) = %f"%blockmean)
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
	ax.set_zlabel(r'Counts (A.U. / mA$\cdot$s)')
	#ax.auto_scale_xyz([width, loc_x], [loc_y1, loc_y2], [0, 65500])
	pl.show()
else:
	print "Plot type '%s' not understood." % plottype