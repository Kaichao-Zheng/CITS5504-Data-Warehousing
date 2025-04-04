import os
import pandas as pd

def getDim_Age():
    # Progress messages
    print("Executing getDim_Age() ...")
    print("Should remain 102/5461 rows")
    
    # Import dimension
    global fatality
    age = fatality[['Age','Age Group']].copy()
    
    # Cleanse fact properties
    global toDrop
    toDrop += ['Age Group']
    
    # Cleanse dimension
    age = age.dropna()
    age = age.drop_duplicates()
    
    # Export
    age.to_csv("output/Dim_Age.csv", index = False)
    
    # Testing
    age.info()
    print()

def getDim_Crash():
    # Progress messages
    print("Executing for getDim_Crash() ...")
    print("Should remain 51284/51283 rows")
    
    # Import dimension
    global fatality
    global crash    # Fatalities of Crash_ID:20164024 in Fatality.xlsx has conflict Speed_Limit
    
    # Cleanse dimension
    crash = crash.dropna(subset=['Crash ID'])
    crash = crash.drop_duplicates()
    crash = crash.fillna('Unknown')
    
    # Pin foreign key to right
    global toDrop
    toDrop += ['Crash Type', 'Speed Limit']
    fatality = fatality[[col for col in fatality.columns if col != 'Crash ID'] + ['Crash ID']]
    
    # Export
    crash.to_csv("output/Dim_Crash.csv", index = False)
    
    # Testing
    crash.info()
    print()
    
def getDim_Involvement():
    # Progress messages
    print("Executing for getDim_Involvement() ...")
    print("Should remain 13/32584 rows")
    
    # Create dimension
    global fatality
    involve = fatality[['Bus Involvement','Heavy Rigid Truck Involvement','Articulated Truck Involvement']].copy()
    
    # Cleanse dimension
    involve = involve.dropna(how='all')
    involve = involve.drop_duplicates()
    involve= involve.fillna('Unknown')
    # Add primary key
    involve['involve ID'] = range(1, 1+len(involve))
    
    # Reshape fact properties
    global toDrop
    toDrop += ['Bus Involvement','Heavy Rigid Truck Involvement','Articulated Truck Involvement']
    fatality = fatality.merge(involve, on=['Bus Involvement','Heavy Rigid Truck Involvement','Articulated Truck Involvement'], how='left')
        
    # Reshape dimension properties
    involve = involve.rename(columns={
        'Bus Involvement': 'Bus',
        'Heavy Rigid Truck Involvement': 'Heavy Rigid Truck',
        'Articulated Truck Involvement': 'Articulated Truck'
    })
    involve = involve[['involve ID'] + [col for col in involve.columns if col != 'involve ID']]
    
    # Export
    involve.to_csv("output/Dim_Involvement.csv", index = False)
    
    # Testing
    involve.info()
    print()
    
def getDim_DateTime():
    # Progress messages
    print("Executing getDim_DateTime() ...")
    print("Should remain 48473/56873 rows")
    
    # Create dimension
    global fatality
    dateTime = fatality[['Month','Year','Dayweek','Time']].copy()
    
    # Cleanse dimension
    dateTime = dateTime.dropna(how='all')
    dateTime = dateTime.drop_duplicates()
    # Add primary key
    dateTime['Date ID'] = range(1, 1+len(dateTime))
    
    # Reshape fact properties
    global toDrop
    toDrop += ['Month','Year','Dayweek','Time']
    fatality = fatality.merge(dateTime, on=['Month','Year','Dayweek','Time'], how='left')
    
    # Reshape dimension properties
    dateTime = dateTime.rename(columns={'Dayweek':'Day of Week'})
    dateTime = dateTime[['Date ID'] + [col for col in dateTime.columns if col != 'Date ID']]
    
    # Export
    dateTime.to_csv("output/Dim_DateTime.csv", index = False)
    
    # Testing
    dateTime.info()
    print()

def getDim_Period():
    # Progress messages
    print("Executing getDim_Period() ...")
    print("Should remain 2/892 rows")
    
    # Create dimension
    global fatality
    rawData = fatality[['Christmas Period','Easter Period']].copy()
    fatality['Period Name'] = pd.NA
    period = pd.DataFrame(columns=['Period Name','Period Type'])
    
    # Reshape fact properties
    global toDrop
    toDrop += ['Christmas Period','Easter Period']
    
    # Flag data conversion and JOIN
    for index, row in rawData.iterrows():
        # Classify period
        if row['Christmas Period'] == 'Yes' and row['Easter Period'] == 'Yes':  # logic error
            fatality.loc[index, 'Period Name'] = pd.NA
            period.loc[index, 'Period Name'] = pd.NA
            period.loc[index, 'Period Type'] = pd.NA
        elif row['Christmas Period'] == 'Yes':
            fatality.loc[index, 'Period Name'] = 'Christmas'
            period.loc[index, 'Period Name'] = 'Christmas'
            period.loc[index, 'Period Type'] = 'Holiday'
        elif row['Easter Period'] == 'Yes':
            fatality.loc[index, 'Period Name'] = 'Easter'
            period.loc[index, 'Period Name'] = 'Easter'
            period.loc[index, 'Period Type'] = 'Holiday'
        elif row['Christmas Period'] == 'No' and row['Easter Period'] == 'No':
            fatality.loc[index, 'Period Name'] = pd.NA
            period.loc[index, 'Period Name'] = pd.NA
            period.loc[index, 'Period Type'] = pd.NA
    
    # Cleanse dimension
    period = period.dropna(subset=['Period Name'])
    period = period.drop_duplicates()
    
    # Export
    period.to_csv("output/Dim_Period.csv", index = False)
    
    # Testing
    period.info()
    print()
    
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
print("Importing raw data spreadsheets ...\n")

# Import raw spreadsheets
fatality = pd.read_excel(
    "src/bitre_fatalities_dec2024.xlsx",
    sheet_name = "BITRE_Fatality",
    skiprows = 4
)
crash = pd.read_excel(
    "src/bitre_fatal_crashes_dec2024.xlsx",
    sheet_name = "BITRE_Fatal_Crash",
    skiprows = 4,
    usecols=['Crash ID', 'Crash Type', 'Speed Limit']
)

# Add primary key and pin to left
fatality['Fatality ID'] = range(1, 1+len(fatality))
fatality = fatality[['Fatality ID'] + [col for col in fatality.columns if col != 'Fatality ID']]

# Mark redundant columns
fatality = fatality.drop(columns=['Day of week'])
toDrop = ['Time of day']

# Void invalid cells
invalid = [-9,'-9','Unknown','Undetermined']
fatality = fatality.replace(invalid, pd.NA)
crash = crash.replace(invalid, pd.NA)

# Export dimension tables
if not os.path.exists("output"):
    os.makedirs("output")
getDim_Age()
getDim_Crash()
getDim_Involvement()
getDim_DateTime()
getDim_Period()

# Export fact table
print("Drop:" + str(toDrop))
fatality = fatality.drop(columns=toDrop)
fatality.to_csv("output/Fact_Fatality.csv", index = False)

# Status message
print("Cleansing complete\n")