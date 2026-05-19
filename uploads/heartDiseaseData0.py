import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\abhid\Downloads\Heart_Disease_Prediction.csv") # make a csv into a dataframe

df['HD'] = df["Heart Disease"].map({"Absence" : 0, "Presence": 1}) # goes through the csv column 'Heart Disease' and makes a new column that 
                                                                   # assigns 0s and 1s to 'absense' and 'presense'

# make 2 new tables (dfs) that take data of patients with HD and without HD
hd_yes = df[df['HD'] == 1]
hd_no = df[df['HD'] == 0]


bins = range(25, 81, 5)

plt.figure(figsize = (12, 5))
plt.subplot(1, 2, 1)
plt.hist(hd_yes["Age"], bins = bins, color = 'red', edgecolor = 'black')
plt.title("Heart Disease")
plt.xlabel('Age')
plt.ylabel('Count')
plt.xticks(bins)
plt.grid(axis = 'y', linestyle = '--', alpha = .5)

plt.subplot(1, 2, 2)
plt.hist(hd_no["Age"], bins = bins, edgecolor = 'black', color = 'green')
plt.title("No Heart Disease")
plt.xlabel('Age')
plt.ylabel('Count')
plt.xticks(bins)
plt.grid(axis = 'y', linestyle = '--', alpha = .5)


plt.show()