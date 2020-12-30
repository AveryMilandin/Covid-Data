# Covid-Data

In this project we analyze data from the repository at https://github.com/owid/covid-19-data.
## Running the Code
To run main.py, which produces both figures, first clone the repository:
```
  $ git clone https://github.com/AveryMilandin/Covid-Data.git
  $ cd Covid-Data
```
You will need to install matplotlib, scipy, and numpy if you don't have them:
```
  $ pip install matplotlib scipy numpy
```
You can then run the code:
```
  $ py -3 main.py
```
Please note that running with Python 2 will not work.
## Analyzing the Data
  We attempt to investigate two questions. First, has the increase in testing in the US caused the perceived death rate to decrease? And second, How would the deaths per day in the US have been affected if quarantine had been extended for 180 days instead of starting reopening. <br />
  For the first question, we need to see the death ratio per day as a function of time. To generate such a plot, we need the number of deaths each day and the number of currently active cases each day so that we can get a ratio of these two numbers on each day. We are given the number of deaths each day in the data set but not the number of currently active cases, so we approximated this value as the sum of the new cases per day for that past 21 days leading up to a given day. With this we were able to generate a plot of the death ratio per day, and we also applied a spline fit as an attempt to smooth the data: <br />
  ![alt text](https://github.com/AveryMilandin/Covid-Data/blob/main/DeathRatio.png)
  <br /> This plot tells us two things. One is that the death ratio seems to decrease over time, which implies that the increase in testing may have had an impact on the death ratio. Also, notice that the data spikes up and down, and even in the spline fit, which is supposed to smooth out the data, there are still spikes. This implies that these spikes are statistically significant and have a cause. One potential cause of these spikes could be the fact that not every state reports covid data every day. If California were only reporting data every other day, for example, we would expect spikes every other day since California has lots of covid deaths.
  <br /> For the second question, we are given all of the data that we need. We can plot the deaths per day as a function of time, and we can highlight the points on the plot where quarantine started and where reopening started. We can then use the data in between these two points to come up with an exponential fit to the data, which can then be used to predict deaths per day if quarantine had continued: <br />
  ![alt text](https://github.com/AveryMilandin/Covid-Data/blob/main/DeathsPerDay.png)
  <br /> Notice that there is a delay from when quarantine started to when deaths started to decrease, and there is also a delay from when quarantine ended to when deaths started to increase. This delay was approximately 21 days, so for the regression we actually used data starting from 21 days after the start of quarantine and ending 21 days after the reopening started. From the regression line we can see that the deaths per day may have decreased to less than 80 per day by December 25th, but instead we are at about 2500 per day.
