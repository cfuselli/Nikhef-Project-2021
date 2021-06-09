How to compare 2 or more calibrations: 


First make datafiles with: calibrationfit_savedataonly.py
	- this script makes an .csv file with a 1 line header: ADC, mV, filename (of calibrated file)
	  Rest of lines contains: ADC, mV 

Run this script seperate for all files you want to use to compare

Now you can run:  plot_nfiles_nofit.py -h 
to see the imput arguments.
Fill in the right filenames and filepaths and number of files 
Run the script. 

