import csv 
import matplotlib.pyplot as plt
  
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

#construct array of approximate currently active cases
fig1, ax1 = plt.subplots()

ax1.plot(list(range(len(us_data['new_deaths_smoothed']))),us_data['new_deaths_smoothed'])
arrow_style = {'arrowstyle': 'simple'}
quarantine_start = 58
quarantine_end = 114
quarantine_resume = 165
response_delay = 21
ax1.annotate(text = "first quarantine", xy = (quarantine_start + response_delay, us_data['new_deaths_smoothed'][quarantine_start + response_delay]), arrowprops = arrow_style)
ax1.annotate(text = "reopening begins", xy = (quarantine_end + response_delay, us_data['new_deaths_smoothed'][quarantine_end + response_delay]), arrowprops = arrow_style)
ax1.annotate(text = "reopening reversed", xy = (quarantine_resume + response_delay, us_data['new_deaths_smoothed'][quarantine_resume + response_delay]), arrowprops = arrow_style)
plt.show()