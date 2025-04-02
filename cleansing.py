import pandas as pd

def getDim_DateTime():
    global crashes
    dateTime = crashes[['Month','Year','Dayweek','Time']].copy()
    
    # Cleanse date dimension
    dateTime = dateTime.dropna()
    dateTime = dateTime.drop_duplicates()
    # Add primary key
    dateTime['Date ID'] = range(1, 1+len(dateTime))
    
    # JOIN to fatal dataframe
    crashes = crashes.merge(dateTime, on=['Month','Year','Dayweek','Time'], how='left')
    
    # Reorder columns
    dateTime = dateTime.rename(columns={'Dayweek':'Day of Week'})
    dateTime = dateTime[['Date ID', 'Month', 'Year', 'Day of Week', 'Time']]
    
    # Export
    dateTime.to_csv("output/Dim_DateTime.csv", index = False)
    
    # Testing
    dateTime.info()

def getDim_Holiday():
    global crashes
    crashes['Period'] = pd.NA
    rawData = crashes[['Christmas Period','Easter Period']].copy()
    
    # Flag data conversion
    holiday = pd.DataFrame(columns=['Period','isHoliday'])
    for index, row in rawData.iterrows():
        # Classify period
        if row['Christmas Period'] == 'Yes' and row['Easter Period'] == 'Yes':
            crashes.loc[index, 'Period'] = pd.NA
            holiday.loc[index, 'Period'] = pd.NA
            holiday.loc[index, 'isHoliday'] = pd.NA
        elif row['Christmas Period'] == 'Yes':
            crashes.loc[index, 'Period'] = 'Christmas'
            holiday.loc[index, 'Period'] = 'Christmas'
            holiday.loc[index, 'isHoliday'] = 'Holiday'
        elif row['Easter Period'] == 'Yes':
            crashes.loc[index, 'Period'] = 'Easter'
            holiday.loc[index, 'Period'] = 'Easter'
            holiday.loc[index, 'isHoliday'] = 'Holiday'
        elif row['Christmas Period'] == 'No' and row['Easter Period'] == 'No':
            crashes.loc[index, 'Period'] = 'Neither'
            holiday.loc[index, 'Period'] = 'Neither'
            holiday.loc[index, 'isHoliday'] = 'Unknown'
    # Cleanse date dimension
    holiday = holiday.dropna()
    holiday = holiday.drop_duplicates()
    # Export
    holiday.to_csv("output/Dim_Holiday.csv", index = False)
    
    # Testing
    holiday.info()
        
# Import raw data
crashes = pd.read_excel("src/bitre_fatal_crashes_dec2024.xlsx", sheet_name = "BITRE_Fatal_Crash", skiprows = 4)
fatalities = pd.read_excel("src/bitre_fatalities_dec2024.xlsx", sheet_name = "BITRE_Fatality", skiprows = 4)

# Delete redundant columns
crashes.drop(columns=['Day of week'], inplace = True)

# Void invalid cells
crashes.loc[:, ['Month']] = pd.to_numeric(crashes['Month'], errors = 'coerce')
crashes.loc[:, ['Year']] = pd.to_numeric(crashes['Year'], errors = 'coerce')
invalid = [-9,'-9','Unknown','Undetermined']
crashes.replace(invalid, pd.NA, inplace = True)

# Export dimension tables
getDim_DateTime()
getDim_Holiday()

# Rename columns
crashes = crashes.rename(columns={'Dayweek':'Day of Week'})

# Export Fact table
crashes.to_csv("output/Fact_Crashes.csv", index = False)