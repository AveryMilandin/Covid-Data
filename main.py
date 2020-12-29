import csv 
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

# csv file name 
filename = "owid-covid-data.csv"
  
# initializing the rows list 
rows = [] 

#first row of US data
us_start = 53232
#last row of US data (Christmas)
us_end = 53571
  
# reading csv file 
with open(filename, 'r') as csvfile: 
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
      
    # extracting field names through first row 
    fields = next(csvreader) 
  
    # extracting each data row one by one 
    for row in csvreader: 
        rows.append(row) 
  
    # get total number of rows 
    print("Total no. of rows: %d"%(csvreader.line_num)) 
  
  
#indices of metrics in rows
row_indices = {'total_cases': 4, 'new_cases': 5, 'total_deaths': 7, 'new_deaths': 8}
#create dict of arrays for each metric listed above
us_data = dict()
for metric in row_indices.keys():
    us_data[metric] = []
#populate arrays for each metric
for row in rows[us_start: us_end]:
    # parsing each column of a row 
    for metric in row_indices.keys():
        row_index = row_indices[metric]
        val = row[row_index]
        numeric_val = None
        if val == '':
            numeric_val = 0
        else:
            numeric_val = int(float(val))
        us_data[metric].append(numeric_val)

#approximate currently active cases calculated as sum of all new cases for past 3 weeks
currentlyActive = []
#ratio of currently infected that die each day
deathRatio = []
newCases = np.array(us_data['new_cases'])

#start 121 days in so that there are enough cases for statistically significant data
for i in range(121, us_end-us_start):
    currentlyActive.append(np.sum(newCases[i-21:i]))
    deathRatio.append(us_data['new_deaths'][i]/currentlyActive[i-121] * 100)

days = list(range(len(deathRatio)))
deathRatioSmooth = savgol_filter(deathRatio, 51, 2)

plt.plot(days,deathRatio)
plt.plot(days,deathRatioSmooth)
plt.ylim([0,0.3])
plt.show()