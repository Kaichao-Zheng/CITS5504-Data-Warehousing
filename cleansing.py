import os
import pandas as pd
import geopandas as gpd

replace_dict = {
    'Anangu Pitjantjatjara Yankunytjatjara': 'Bayside (QLD)',
}

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
    
    # Status message
    age.info()
    print()

def getDim_Crash(): 
    # Progress messages
    print("Executing for getDim_Crash() ...")
    print("Should remain 51284/51283 rows")
    
    # Import dimension
    global fatality
    crash = pd.read_excel(      # Fatalities of Crash_ID:20164024 in Fatality.xlsx has conflict Speed_Limit
        "src/bitre_fatal_crashes_dec2024.xlsx",
        sheet_name = "BITRE_Fatal_Crash",
        skiprows = 4,
        usecols=['Crash ID', 'Crash Type', 'Speed Limit']
    )
    
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
    
    # Status message
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
    
    # Status message
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
    
    # Status message
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
    
    # Status message
    period.info()
    print()
    
def getDim_Location():
    # Progress messages
    print("Executing getDim_Location() ...")
    
    # Crease dimension
    global fatality, replace_dict
    location = fatality[['National LGA Name 2021', 'State']].copy()
    
    # Cleanse LGA Name
    location = location.dropna(subset=['National LGA Name 2021'])
    location = location.drop_duplicates()
    location['National LGA Name 2021'] = location['National LGA Name 2021'].replace(replace_dict)

def getDim_LGA():
    # Progress messages
    print("Executing for getDim_LGA() ...")
    print("Should remain 565/564 rows")
    
    # Create dimension
    rawGeo = gpd.read_file("src/LGA_2021_AUST_GDA94.geojson")
    geo = rawGeo[['LGA_CODE21','LGA_NAME21','geometry']].copy()
    
    # Cleanse dimension
    geo = geo.replace(['ZZZZZ'], pd.NA)     # Invalid LGA Code for "Outside Australia"
    geo = geo.dropna()
    geo = geo.drop_duplicates()
    
    # Reshape dimension properties
    geo = geo.rename(columns={
        'LGA_CODE21':'LGA Code',
        'LGA_NAME21':'LGA Name',
        'geometry':'LGA Geometry'           # Dtype geometry can be drill down to coordinates later
    })
    
    # Export as Power BI identifiable file format
    geo.to_file("output/Dim_LGA.json", driver="GeoJSON")
    
    # Status message
    geo.info()


# main()
# Progress messages
print("Importing raw data spreadsheets ...\n")

# Import raw fact table
fatality = pd.read_excel(
    "src/bitre_fatalities_dec2024.xlsx",
    sheet_name = "BITRE_Fatality",
    skiprows = 4
)

# Import replace dict
rawDict = pd.read_csv("replaceDict.csv")
replace_dict = dict(zip(rawDict['original'], rawDict['replacement']))

# # Add primary key and pin to left
# fatality['Fatality ID'] = range(1, 1+len(fatality))
# fatality = fatality[['Fatality ID'] + [col for col in fatality.columns if col != 'Fatality ID']]

# # Mark redundant columns
# fatality = fatality.drop(columns=['Day of week'])
# toDrop = ['Time of day']

# # Void invalid cells
# invalid = [-9,'-9','Unknown','Undetermined']
# fatality = fatality.replace(invalid, pd.NA)
# crash = crash.replace(invalid, pd.NA)

# Export dimension tables
if not os.path.exists("output"):
    os.makedirs("output")
# getDim_Age()
# getDim_Crash()
# getDim_Involvement()
# getDim_DateTime()
# getDim_Period()
getDim_Location()
# getDim_LGA()

# # Export fact table
# print("Drop:" + str(toDrop))
# fatality = fatality.drop(columns=toDrop)
# fatality.to_csv("output/Fact_Fatality.csv", index = False)

# Status message
print("Cleansing complete\n")