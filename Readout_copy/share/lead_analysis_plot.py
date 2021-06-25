import numpy as np
import csv
import matplotlib.pyplot as plt

heights = []
counts = []
time = []

#read file
fpath = "../data/"
fname = "counts_lead.csv"
file_loc = (fpath+fname)
with open(file_loc) as csv_file: 
	csv_reader = csv.reader(csv_file, delimiter= ',')
	for i,row in enumerate(csv_reader):
		if i>2:   # skip header
		    heights.append(float(row[1]))
		    counts.append(float(row[2]))
		    time.append(float(row[3]))
		    pass

countrate = []
passed = []	
print(heights)
for i in range(len(counts)):
	countrate.append(counts[i]/time[i])
for i in range(len(countrate)-1):
	passed.append(countrate[i]-countrate[i+1])
#print(heights)
#print(passed)

#create histogram/bar graph of muon pass rate vs height of lead
bins=np.array(heights)[0:-1]
print(np.shape(bins))
plt.bar(bins, passed)
plt.ylabel("Rate of muons passed [counts / s]")
plt.xlabel("Lead traversed [cm]")
plt.show()
