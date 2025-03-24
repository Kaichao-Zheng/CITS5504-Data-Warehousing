import pandas as pd

def getDim_DateTime():
    global df_fatal
    dateTime_df = df_fatal[['Month','Year','Dayweek','Time']].copy()
    
    # Cleanse date dimension
    dateTime_df = dateTime_df.dropna()
    dateTime_df = dateTime_df.drop_duplicates()
    # Add primary key
    dateTime_df['Date ID'] = range(1, 1+len(dateTime_df))
    
    # JOIN to fatal dataframe
    df_fatal = df_fatal.merge(dateTime_df, on=['Month','Year','Dayweek','Time'], how='left')
    
    # Reorder columns
    dateTime_df = dateTime_df.rename(columns={'Dayweek':'Day of Week'})
    dateTime_df = dateTime_df[['Date ID', 'Month', 'Year', 'Day of Week', 'Time']]
    
    # Export
    dateTime_df.to_csv('Dim_DateTime.csv', index = False)
    
    # Testing
    dateTime_df.info()

def getDim_Holiday():
    global df_fatal
    df_fatal['Period'] = pd.NA
    raw_df = df_fatal[['Christmas Period','Easter Period']].copy()
    
    # Flag data conversion
    holiday_df = pd.DataFrame(columns=['Period','isHoliday'])
    for index, row in raw_df.iterrows():
        # Classify period
        if row['Christmas Period'] == 'Yes' and row['Easter Period'] == 'Yes':
            df_fatal.loc[index, 'Period'] = pd.NA
            holiday_df.loc[index, 'Period'] = pd.NA
            holiday_df.loc[index, 'isHoliday'] = pd.NA
        elif row['Christmas Period'] == 'Yes':
            df_fatal.loc[index, 'Period'] = 'Christmas'
            holiday_df.loc[index, 'Period'] = 'Christmas'
            holiday_df.loc[index, 'isHoliday'] = 'Holiday'
        elif row['Easter Period'] == 'Yes':
            df_fatal.loc[index, 'Period'] = 'Easter'
            holiday_df.loc[index, 'Period'] = 'Easter'
            holiday_df.loc[index, 'isHoliday'] = 'Holiday'
        elif row['Christmas Period'] == 'No' and row['Easter Period'] == 'No':
            df_fatal.loc[index, 'Period'] = 'Neither'
            holiday_df.loc[index, 'Period'] = 'Neither'
            holiday_df.loc[index, 'isHoliday'] = 'Unknown'
    # Cleanse date dimension
    holiday_df = holiday_df.dropna()
    holiday_df = holiday_df.drop_duplicates()
    # Export
    holiday_df.to_csv('Dim_Holiday.csv', index = False)
    
    # Testing
    holiday_df.info()
        
# Import source data
df_fatal = pd.read_excel('src/bitre_fatal_crashes_dec2024.xlsx', sheet_name = "BITRE_Fatal_Crash", skiprows = 4)

# Delete redundant columns
df_fatal.drop(columns=['Day of week'], inplace = True)

# Void invalid cells
df_fatal.loc[:, ['Month']] = pd.to_numeric(df_fatal['Month'], errors = 'coerce')
df_fatal.loc[:, ['Year']] = pd.to_numeric(df_fatal['Year'], errors = 'coerce')
invalid = [-9,'-9','Unknown','Undetermined']
df_fatal.replace(invalid, pd.NA, inplace = True)

# Export dimension tables
getDim_DateTime()
getDim_Holiday()

# Rename columns
df_fatal = df_fatal.rename(columns={'Dayweek':'Day of Week'})

# Export Fact table 
df_fatal.to_csv('Merged.csv', index = False)