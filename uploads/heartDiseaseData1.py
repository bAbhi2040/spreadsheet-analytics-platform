import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r"C:\Users\abhid\Downloads\Heart_Disease_Prediction.csv")   # make a csv into a dataframe

df['HD'] = df["Heart Disease"].map({"Absence" : 0, "Presence": 1})      # maps the csv column 'Heart Disease' and makes a new column 
                                                                        # that assigns 0s and 1s to 'absence' and 'presence'

# make 2 series that take data of patients with HD and without HD
hd_yes = df[df['HD'] == 1]
hd_no = df[df['HD'] == 0]




variableQuant = input("enter the variable of interest: ")         # ask user for variable of interest


data = df[variableQuant]                                          # make a new series specifically for the desired data column

uniqueValues = data.unique()                                      # goes through data series and extracts unique, non-repeating values
isBinary = set(uniqueValues) <= {0, 1}                            # checks of uniqueValues only has 0s and 1s, 'set()' goes through arrays
                                                                  # and removes duplicates, '<=' checks if the set is a subset of {x, y}
lower = data.min()
upper = data.max()
dataRange = upper - lower

if isBinary:
    # ensure that if variableQuant is binary, then only two bars will exist for better readability
    bins = [-0.5, .5, 1.5]
    lower = 0
    upper = 1
elif dataRange <= 10:
    # if the range of data is <= 10, then each bar will be centered around a single value for readability
    bins = np.arange(data.min() + .5, data.max() + 1.5, 1)
else:  
    # using Freedman-Diaconis rule, bin width = ((2 * IQR) / n**(1/3))
    n = len(data)                                                     # number of data points
    iqr = np.percentile(data, 75) - np.percentile(data, 25)           # 75th percentile - 25th percentile
    
    if iqr == 0 or dataRange <= 10:
        binWidth = 1                        # failsafe for if iqr is 0 or if dataRange is less than 10
    else:
        binWidth = (2 * iqr) / n**(1/3)     # Freedman-Diaconis rule
    
    
    bins = np.arange(lower, upper + binWidth, binWidth)     # make an array with the lower and upper bin edges of the data set and increase 
                                                            # incrementally by binWidth

# define a fuction for plt.xticks() for different variables
def xticks():
    if isBinary:
        plt.xticks([0, 1])                                      # ensures that the only values of x are binary
    elif dataRange <= 10:
        plt.xticks(np.arange(data.min(), data.max() + 1, 1))    # spaces out x values by increments relating to min and max values of data
    else:
        stepSize = round(binWidth)                      # round binWidth for readability
        stepSize = max(stepSize, 1)                     # failsafe to ensure that stepSize is never 0
        plt.xticks(np.arange(lower, upper + 1, stepSize)) # make a scale using lower and upper bounds increasing by the stepsize

# plots
plt.figure(figsize = (12, 5))
plt.subplot(1, 2, 1)
plt.hist(hd_yes[variableQuant], bins = bins, color = 'red', edgecolor = 'black', rwidth = .95, align = 'mid')
plt.title("Heart Disease")
plt.xlabel(variableQuant)
plt.ylabel('Count')
xticks()
plt.grid(axis = 'y', linestyle = '--', alpha = .5)

plt.subplot(1, 2, 2)
plt.hist(hd_no[variableQuant], bins = bins, edgecolor = 'black', color = 'green', rwidth = .95)
plt.title("No Heart Disease")
plt.xlabel(variableQuant)
plt.ylabel('Count')
xticks()
plt.grid(axis = 'y', linestyle = '--', alpha = .5)


plt.show()