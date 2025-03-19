import pandas as pd

def getDim_Date():
    global df_fatal
    date_df = df_fatal[['Month','Year','Dayweek','Time']].copy()
    
    # Cleanse date dimension
    date_df = date_df.dropna()
    date_df = date_df.drop_duplicates()
    # Add primary key
    date_df['DateID'] = range(1, 1+len(date_df))
    
    # JOIN to fatal dataframe
    df_fatal = df_fatal.merge(date_df, on=['Month','Year','Dayweek','Time'], how='left')
    
    # Reorder column_index
    date_df = date_df.rename(columns={'Dayweek':'DayOfWeek'})
    date_df =  date_df[['DateID', 'Month', 'Year', 'DayOfWeek', 'Time']]
    
    # Export as csv file
    date_df.to_csv('Dim_Date.csv', index = False)
    df_fatal.to_csv('Merged.csv', index = False)
    
    # Testing
    date_df.info()

# Read table files
df_fatal = pd.read_excel('src/bitre_fatal_crashes_dec2024.xlsx', sheet_name = "BITRE_Fatal_Crash", skiprows = 4)

# Void invalid cells
df_fatal.loc[:, ['Month']] = pd.to_numeric(df_fatal['Month'], errors = 'coerce')
df_fatal.loc[:, ['Year']] = pd.to_numeric(df_fatal['Year'], errors = 'coerce')
invalid = [-9,'-9','Unknown','Undetermined']
df_fatal.replace(invalid, pd.NA, inplace=True)

getDim_Date()

