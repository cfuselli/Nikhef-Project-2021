This folder contains files for the cable analysis with detector noor and scintillator Carlo of size 15x5x1cm (does not exist anymore)

in Calibration/share/ run
python3 cable_analysis.py -path ../data/cable_test/nice_plots/15x5x1cm/ -f cable_0cm_Dnoor_Scarlo_300.csv cable_20cm_Dnoor_Scarlo_300.csv cable_40cm_Dnoor_Scarlo_300.csv -dist 20cm -dist2 _0cm  -labeld "no cable" -label 20cm -labeld2 40cm -fit 

