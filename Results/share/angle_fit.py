#!/usr/bin/env python3
# angle analysis considering errors in angles and counts
#
# @haslbeck
# 5 July

#import ROOT
import pandas as pd


# read in data
data = pd.read_csv('../data/counts_angle.csv', skiprows = 1, header = 0, names = ['folder', 'angle', 'height', 'counts', 'time'])
data = data.sort_values(by = ['angle']).reset_index()

counts = data['counts'].values
times = data['time'].values
angles = data['angle'].values

norm_counts = counts /times


print(
    type(counts), len(counts),
    type(times), len(times),
    type(angles), len(angles),
    type(norm_counts), len(norm_counts),
    
)


  