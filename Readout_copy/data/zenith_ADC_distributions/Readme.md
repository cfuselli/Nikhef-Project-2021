for sg:
python3 simple_analysis_separate_files.py -path ../output/output_2021-06-23_14-03/ ../output/output_2021-06-23_15-38/ ../output/output_2021-06-23_16-30/ -labels 0rad 0.57rad 1.57rad -title zenith
for bg:
simple_analysis_separate_files.py -path ../output/output_2021-06-23_14-03/ ../output/output_2021-06-23_15-38/ ../output/output_2021-06-23_16-30/ -labels 0rad 0.57rad 1.57rad -title zenith -ignore setup data
