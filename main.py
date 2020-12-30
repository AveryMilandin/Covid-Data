import csv 
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit

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

#approximate currently active cases calculated as sum of all new cases for past 3 weeks
currentlyActive = []
#ratio of currently infected that die each day
deathRatio = []
newCases = np.array(us_data['new_cases'])

#start at 121 days in so that there are enough cases for statistically significant data
for i in range(121, us_end-us_start):

    #approximate new cases for given day
    currentlyActive.append(np.sum(newCases[i-21:i])) 
    deathRatio.append(us_data['new_deaths'][i]/currentlyActive[i-121] * 100)

days = list(range(len(deathRatio)))

#Spline fit to deathRatio
deathRatioSmooth = savgol_filter(deathRatio, 51, 2) 

#Create figure for death ratio plot
fig0, ax0 = plt.subplots() 
ax0.plot(days,deathRatio)
ax0.plot(days,deathRatioSmooth)
plt.title("USA Death Ratio Over Time")
ax0.set_xlabel("Days Since 5/20/2020")
ax0.set_ylabel("Percentage of Deaths From Currently Active Cases")
plt.ylim([0,0.3])

#Create figure for deaths per day plot
fig1, ax1 = plt.subplots() 

#"First" day of quarantine. Just an estimate since quarantine started on different days in different states
quarantine_start = 79 

#reopening started
quarantine_end = 142 

#This is how long it takes the graph to react to actions taken by the US
response_delay = 21 

#plotting the raw data
ax1.plot(list(range(len(us_data['new_deaths_smoothed']))),us_data['new_deaths_smoothed'], label = "Actual Deaths") 

#highlight quarantine start point
ax1.plot(quarantine_start,us_data['new_deaths_smoothed'][quarantine_start], 'r*') 
ax1.annotate(text = " Quarantine Starts", xy = (quarantine_start, us_data['new_deaths_smoothed'][quarantine_start]))

#highlight quarantine end point
ax1.plot(quarantine_end,us_data['new_deaths_smoothed'][quarantine_end], 'r*') 
ax1.annotate(text = " Reopening Begins", xy = (quarantine_end, us_data['new_deaths_smoothed'][quarantine_end]))

#Exponential Regression: y = Ae^(bx) + c

#list of days to be used for regression
days = np.array(list(range(quarantine_start + response_delay, quarantine_end + response_delay))) 

#corresponding death data for those days
deaths = np.array(us_data['new_deaths_smoothed'])[quarantine_start + response_delay:quarantine_end + response_delay] 

#function with parameters a, b, and c that will be estimated based on data
def func(x, a, b, c):
    return a * np.exp(-b * x) + c

#SciKit does the regression for us
predicted = curve_fit(func,  days - quarantine_start - response_delay,  deaths)

#We will use the regression results to predict the expected deaths if quarantine had continued for 180 days longer
days = np.append(days, range(quarantine_end + response_delay + 1, quarantine_end + response_delay + 180), 0)
ax1.plot(days, predicted[0][0] * np.exp(-predicted[0][1] * (days - quarantine_start - response_delay)) + predicted[0][2], 'm', label="Predicted Deaths w/ Extended Quarantine")
ax1.legend()
ax1.set_ylabel("Deaths")
ax1.set_xlabel("Days Since 1/22/2020")
plt.title("USA Covid Deaths Per Day")
plt.show()