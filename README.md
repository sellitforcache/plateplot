SINQ Imaging Plate Scripts
========
**Ryan M. Bergmann, Paul Scherrer Institut, Dec. 2014.**

Python scripts that are useful for analyzing SINQ imaging plate results.

### USAGE:

Arguments:

0 arguments:  Default test plot

1 argument :  [file_name]  Loads TIF "file_name" and plots it

2 arguments:  [file_name] [plot_type] Loads TIF "file_name" and plots according to "plot_type".  Plot types = plot (only image), average (calculated average across band, default positions/widths), total_average (calculates average of entire image)	

6 arguments:  [file_name] [plot_type] [width] [loc_x] [loc_y1] [loc_y2] Same as 2 arguments, but with the specified locations and widths of the averages
else       :  Throw error and print instructions.


Example:
``` bash
$ ./plotPlate.py [args]
```

