import csv 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
  
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
row_indices = {'total_cases': 4, 'new_cases': 5, 'total_deaths': 7, 'new_deaths': 8, "new_deaths_smoothed": 9}
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

fig1, ax1 = plt.subplots()
quarantine_start = 79
quarantine_end = 142
response_delay = 21
ax1.plot(list(range(len(us_data['new_deaths_smoothed']))),us_data['new_deaths_smoothed'], label = "Actual Deaths")
ax1.plot(quarantine_start,us_data['new_deaths_smoothed'][quarantine_start], 'r*')
ax1.plot(quarantine_end,us_data['new_deaths_smoothed'][quarantine_end], 'r*')

ax1.annotate(text = " Quarantine Starts", xy = (quarantine_start, us_data['new_deaths_smoothed'][quarantine_start]))
ax1.annotate(text = " Reopening Begins", xy = (quarantine_end, us_data['new_deaths_smoothed'][quarantine_end]))

days = np.array(list(range(quarantine_start + response_delay, quarantine_end + response_delay)))
deaths = np.array(us_data['new_deaths_smoothed'])[quarantine_start + response_delay:quarantine_end + response_delay]
def func(x, a, b, c):
    return a * np.exp(-b * x) + c
predicted = curve_fit(func,  days - quarantine_start - response_delay,  deaths)
print(predicted[0])
days = np.append(days, range(quarantine_end + response_delay + 1, quarantine_end + response_delay + 180), 0)
ax1.plot(days, predicted[0][0] * np.exp(-predicted[0][1] * (days - quarantine_start - response_delay)) + predicted[0][2], 'm', label="Predicted Deaths w/ Extended Quarantine")
ax1.legend()
ax1.set_ylabel("Deaths")
ax1.set_xlabel("Days Since 1/22/2020")
plt.title("USA Covid Deaths Per Day")
plt.show()