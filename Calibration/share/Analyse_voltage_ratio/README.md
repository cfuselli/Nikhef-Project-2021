Always run analysis_voltage.py first. The input file must look like: 

	Amplitude, .. 	#input amplitude
	..		#measured list of output
	..
	..
	Amplitude, ..	#next imput amplitude
	..		#measured list of output
	..
	etc.

-----------------------------------------------------------------------------------------------------------------------------------------------
usage: analysis_voltage.py [-h] [-in_name IN_NAME] [-in_path IN_PATH] [-out_name OUT_NAME] [-out_path OUT_PATH] [-header HEADER]

Plot ratio Output [mV] over Input [mV]. Input is voltage dispayed on pulse generator, output is voltage measured from BNC output.

optional arguments:
  -h, --help          show this help message and exit
  -in_name IN_NAME    csv filename with input voltages and measured voltages
  -in_path IN_PATH    default ../data/
  -out_name OUT_NAME  .csv file with: ratio(out/in), std ratio, input voltage per line
  -out_path OUT_PATH  default ../data/calibration/
  -header HEADER      default 0
-----------------------------------------------------------------------------------------------------------------------------------------------




Then use output file(s) from analysis_voltage.py as input for nplot_input_output.py if you want to compare different detectors! 

-----------------------------------------------------------------------------------------------------------------------------------------------

usage: nplot_input_output.py [-h] -list LIST [LIST ...] [-in_path IN_PATH] [-out_name OUT_NAME] [-out_path OUT_PATH] [-header HEADER]

Plot multiple ratios vs. input voltage. -FIRST RUN: analysis_voltage.py to get the right .csv files

optional arguments:
  -h, --help            show this help message and exit
  -list LIST [LIST ...], --list LIST [LIST ...]
                        csv filenames with voltage in- and output (Use like: -list_fnames name1 name2 name3
  -in_path IN_PATH      default ../data/
  -out_name OUT_NAME    figure name
  -out_path OUT_PATH    default ../data/calibration/
  -header HEADER        default 0

-----------------------------------------------------------------------------------------------------------------------------------------------