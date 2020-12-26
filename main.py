# importing csv module 
import csv 
  
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

for metric in us_data.keys():
    data = us_data[metric]
    print(metric + ":", end = " ")
    print(data)