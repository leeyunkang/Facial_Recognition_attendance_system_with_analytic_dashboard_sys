import pandas as pd
import numpy as np

df = pd.read_csv('/Users/yunka/Desktop/New folder (3)/fyp1/dataset/Absenteeism.csv')
df.drop('Absenteeism Time in Hours', axis=1, inplace=True)
df.drop('Daily Work Load Average', axis=1, inplace=True)
# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Find earliest and latest dates in dataset
min_date = df['Date'].min()
max_date = df['Date'].max()

# Create new dataset
new_data = []

for date in pd.date_range(start=min_date, end=max_date, freq='D'):

    id = []
    for idx in df.index:
        print(idx)
        row = df.loc[idx].copy()
        if row['Date'] == date :
            print(0)
            if row['ID'] not in id:
                new_data.append(row)
                id.append(row['ID'])
            #row['Reason for Absence'] = data['Reason for Absence'][0] if row['ID'] == data['ID'][0] else 'None'
        else:
            row['Reason for Absence'] = 'None'
            row['Date'] = date
            if row['ID'] not in id:
                new_data.append(row)
                id.append(row['ID'])



new_df = pd.DataFrame(new_data)

# Sort by date and ID
new_df.sort_values(by=['Date', 'ID'], inplace=True)
new_df.reset_index(drop=True, inplace=True)

# Fill missing values with NaN
new_df.replace('None', np.nan, inplace=True)

print(new_df)

