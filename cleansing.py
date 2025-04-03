import pandas as pd

def getDim_Crash():
    # Progress messages
    print("Executing for getDim_Crash() ...")
    print("Should remain 51285/56873 rows")
    
    # import dimension
    global fatality
    crash = fatality[['Crash ID', 'Crash Type', 'Speed Limit']].copy()
    
    # Cleanse dimension
    crash = crash.dropna(subset=['Crash ID'])
    crash = crash.drop_duplicates()
    
    # Pin foreign key to right
    fatality = fatality[[col for col in fatality.columns if col != 'Crash ID'] + ['Crash ID']]
    # Delete dimension properties
    fatality.drop(columns=['Crash Type','Speed Limit'], inplace=True)
    
    # Export
    crash.to_csv("output/Dim_Crash.csv", index = False)
    
    # Testing
    crash.info()
    
def getDim_Involvement():
    # Progress messages
    print("Executing for getDim_Involvement() ...")
    print("Should remain ?/? rows")

def getDim_DateTime():
    # Progress messages
    print("Executing getDim_DateTime() ...")
    print("Should remain 48435/56873 rows")
    
    # Create dimension
    global fatality
    dateTime = fatality[['Month','Year','Dayweek','Time']].copy()
    
    # Cleanse dimension
    dateTime = dateTime.drop_duplicates()
    
    # Add primary key
    dateTime['Date ID'] = range(1, 1+len(dateTime))
    
    # JOIN to fact table
    fatality = fatality.merge(dateTime, on=['Month','Year','Dayweek','Time'], how='left')
    fatality.drop(columns=['Month','Year','Dayweek','Time'], inplace=True)
    
    # Rename column
    dateTime = dateTime.rename(columns={'Dayweek':'Day of Week'})
    
    # Reshape columns
    dateTime = dateTime[['Date ID', 'Month', 'Year', 'Day of Week', 'Time']]
    
    # Export
    dateTime.to_csv("output/Dim_DateTime.csv", index = False)
    
    # Testing
    dateTime.info()

def getDim_Holiday():
    # Progress messages
    print("Executing getDim_Holiday() ...")
    print("Should remain 3/814 rows")
    
    # Add foreign key
    global fatality
    fatality['Period'] = pd.NA
    
    # Create dimension
    holiday = pd.DataFrame(columns=['Period','isHoliday'])
    
    # Flag data conversion and JOIN
    rawData = fatality[['Christmas Period','Easter Period']].copy()
    for index, row in rawData.iterrows():
        # Classify period
        if row['Christmas Period'] == 'Yes' and row['Easter Period'] == 'Yes':
            fatality.loc[index, 'Period'] = pd.NA
            holiday.loc[index, 'Period'] = pd.NA
            holiday.loc[index, 'isHoliday'] = pd.NA
        elif row['Christmas Period'] == 'Yes':
            fatality.loc[index, 'Period'] = 'Christmas'
            holiday.loc[index, 'Period'] = 'Christmas'
            holiday.loc[index, 'isHoliday'] = 'Holiday'
        elif row['Easter Period'] == 'Yes':
            fatality.loc[index, 'Period'] = 'Easter'
            holiday.loc[index, 'Period'] = 'Easter'
            holiday.loc[index, 'isHoliday'] = 'Holiday'
        elif row['Christmas Period'] == 'No' and row['Easter Period'] == 'No':
            fatality.loc[index, 'Period'] = 'Neither'
            holiday.loc[index, 'Period'] = 'Neither'
            holiday.loc[index, 'isHoliday'] = 'Unknown'
    fatality.drop(columns=['Christmas Period', 'Easter Period'], inplace=True)
    
    # Cleanse dimension
    holiday = holiday.dropna(subset=['Period'])
    holiday = holiday.drop_duplicates()
    
    # Export
    holiday.to_csv("output/Dim_Holiday.csv", index = False)
    
    # Testing
    holiday.info()
    
def getDim_Location():
    # Progress messages
    print("Executing getDim_Location() ...")

def getDim_LGA():
    # Progress messages
    print("Executing for getDim_LGA() ...")
    
def getDim_Dwelling():
    # Progress messages
    print("Executing for getDim_Dwelling() ...")
    
def getDim_Remoteness():
    # Progress messages
    print("Executing for getDim_Remoteness() ...")

# main()
# Progress messages
print("Importing raw data spreadsheets ...")

# Import raw spreadsheets
fatality = pd.read_excel(
    "src/bitre_fatalities_dec2024.xlsx",
    sheet_name = "BITRE_Fatality",
    skiprows = 4
)

# Add primary key and pin to left
fatality['Fatality ID'] = range(1, 1+len(fatality))
fatality = fatality[['Fatality ID'] + [col for col in fatality.columns if col != 'Fatality ID']]

# Delete redundant columns
fatality.drop(columns=['Day of week', 'Time of day', 'Age Group'], inplace=True)

# Convert columns to numeric
fatality.loc[:, ['Month']] = pd.to_numeric(fatality['Month'], errors = 'coerce')
fatality.loc[:, ['Year']] = pd.to_numeric(fatality['Year'], errors = 'coerce')

# Void invalid cells
invalid = [-9,'-9','Unknown','Undetermined']
fatality.replace(invalid, pd.NA, inplace = True)

# Export dimension tables
getDim_Crash()
getDim_DateTime()
getDim_Holiday()

# Rename columns
fatality = fatality.rename(columns={'Dayweek':'Day of Week'})

# Export Fact table
fatality.to_csv("output/Fact_Fatality.csv", index = False)

# Testing
print("Cleansing complete\n")