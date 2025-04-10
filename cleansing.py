import os
import pandas as pd
import geopandas as gpd

def getDim_Age():
    # Progress messages
    print("Executing getDim_Age() ...")
    
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
    age.to_csv("out/Dim_Age.csv", index = False)
    
    # Status message
    age.info()
    print()

def getDim_Crash(): 
    # Progress messages
    print("Executing getDim_Crash() ...")
    
    # Import dimension
    global fatality, invalid
    crash = pd.read_excel(      # Fatalities of Crash_ID:20164024 in Fatality.xlsx has conflict Speed_Limit
        "src/bitre_fatal_crashes_dec2024.xlsx",
        sheet_name = "BITRE_Fatal_Crash",
        skiprows = 4,
        usecols=['Crash ID', 'Crash Type', 'Speed Limit', 'National Road Type']
    )
    crash = crash.replace(invalid, pd.NA)
    
    # Cleanse dimension
    crash = crash.dropna(subset=['Crash ID'])
    crash = crash.drop_duplicates()
    
    # Pin foreign key to right
    global toDrop
    toDrop += ['Crash Type', 'Speed Limit', 'National Road Type']
    fatality = fatality[[col for col in fatality.columns if col != 'Crash ID'] + ['Crash ID']]
    
    # Export
    crash.to_csv("out/Dim_Crash.csv", index = False)
    
    # Status message
    crash.info()
    print()

def getDim_Involvement():
    # Progress messages
    print("Executing getDim_Involvement() ...")
    
    # Create dimension
    global fatality
    involve = fatality[['Bus Involvement','Heavy Rigid Truck Involvement','Articulated Truck Involvement']].copy()
    
    # Cleanse dimension
    involve = involve.dropna(how='all')
    involve = involve.drop_duplicates()
    involve= involve.fillna('Unknown')
    # Add primary key
    involve['Involve ID'] = range(1, 1+len(involve))
    
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
    involve = involve[['Involve ID'] + [col for col in involve.columns if col != 'Involve ID']]
    
    # Export
    involve.to_csv("out/Dim_Involvement.csv", index = False)
    
    # Status message
    involve.info()
    print()
    
def getDim_DateTime():
    # Progress messages
    print("Executing getDim_DateTime() ...")
    
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
    dateTime.to_csv("out/Dim_DateTime.csv", index = False)
    
    # Status message
    dateTime.info()
    print()

def getDim_Period():
    # Progress messages
    print("Executing getDim_Period() ...")
    
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
    period.to_csv("out/Dim_Period.csv", index = False)
    
    # Status message
    period.info()
    print()

def getDim_Dwelling():
    # Progress messages
    print("Executing getDim_Dwelling() ...")
    
    # Create dimension
    dwell = pd.read_csv(
        "src/LGA (count of dwellings).csv",
        skiprows = 10,
        usecols=[0, 1]
    )
    
    # Cleanse dimension
    dwell = dwell[:-5]      # hardcoding row delete
    dwell = dwell.dropna()
    dwell = dwell.drop_duplicates()
    dwell['LGA (EN)'] = dwell['LGA (EN)'].replace(replace_dict)
    
    # Reshape dimension properties
    dwell = dwell.rename(columns={
        'LGA (EN)': 'LGA Name',
        'Unnamed: 1': 'Dwelling'
    })
    
    # Export
    dwell.to_csv("out/Dim_Dwelling.csv", index = False)
    
    # Status message
    dwell.info()
    print()

def getDim_Location():
    # Progress messages
    print("Executing getDim_Location() ...")
    
    # Crease dimension
    global fatality, replace_dict
    location = fatality[['National LGA Name 2021', 'State']].copy()
    population = pd.read_excel(
        "src/Population estimates by LGA, Significant Urban Area, Remoteness Area, Commonwealth Electoral Division and State Electoral Division, 2001 to 2023.xlsx",
        sheet_name = "Table 1",
        skiprows = 6,
        usecols=['LGA code', 'Local Government Area']       # Ignore population data
    )
    
    # Cleanse LGA Name
    location = location.dropna(subset=['National LGA Name 2021'])
    location = location.drop_duplicates()
    location['National LGA Name 2021'] = location['National LGA Name 2021'].replace(replace_dict)
    
    population = population.dropna(subset=['LGA code', 'Local Government Area'])
    population = population.drop_duplicates()
    population['Local Government Area'] = population['Local Government Area'].replace(replace_dict)
    
    # Reshape fact properties
    global toDrop
    toDrop += ['State']
    
    # Reshape dimension properties
    location = location.rename(columns={
        'National LGA Name 2021': 'LGA Name',
    })
    fatality = fatality.rename(columns={
        'National LGA Name 2021': 'LGA Name',
    })
    
    population = population.rename(columns={
        'LGA code': 'LGA Code',
        'Local Government Area': 'LGA Name',
    })
    
    # JOIN location and population dimensions
    location = location.merge(population, on=['LGA Name'], how='left')
    
    # Reorder columns
    location = location[['LGA Code', 'LGA Name', 'State']]
    
    # Export as Power BI identifiable file format
    location.to_csv("out/Dim_Location.csv", index = False)
    
    # Status message
    location.info()
    print()

def getDim_LGA_Geometry():
    # Progress messages
    print("Executing for getDim_LGA() ...")
    
    # Create dimension
    rawGeo = gpd.read_file("src/LGA_2021_AUST_GDA94.geojson")
    geo = rawGeo[['LGA_CODE21','LGA_NAME21','geometry']].copy()
    
    # Cleanse dimension
    global replace_dict
    geo = geo.replace(['ZZZZZ'], pd.NA)     # Invalid LGA Code for "Outside Australia"
    geo = geo.dropna()
    geo = geo.drop_duplicates()
    
    # Reshape dimension properties
    geo = geo.rename(columns={
        'LGA_CODE21':'LGA Code',
        'LGA_NAME21':'LGA Name',            # Placeholder, just for human readability
        'geometry':'LGA Geometry'           # Dtype geometry can be drill down to coordinates later
    })
    
    # Export as Power BI identifiable file format
    geo.to_file("out/Dim_LGA.json", driver="GeoJSON")
    
    # Status message
    geo.info()
    print()

# main()
# Import raw fact table
print("Importing fatality data as fact table ...\n")
fatality = pd.read_excel(
    "src/bitre_fatalities_dec2024.xlsx",
    sheet_name = "BITRE_Fatality",
    skiprows = 4
)

# Import replace dict
rawDict = pd.read_csv("dict/replaceDict.csv")
replace_dict = dict(zip(rawDict['original'], rawDict['replacement']))

# Add primary key and pin to left
fatality['Fatality ID'] = range(1, 1+len(fatality))
fatality = fatality[['Fatality ID'] + [col for col in fatality.columns if col != 'Fatality ID']]

# Mark redundant columns
fatality = fatality.drop(columns=['Day of week'])
toDrop = ['Time of day']

# Void invalid cells
invalid = [-9,'-9','Unknown','Undetermined']
fatality = fatality.replace(invalid, pd.NA)

# Export dimension tables
if not os.path.exists("out"):
    os.makedirs("out")
getDim_Age()
getDim_Crash()
getDim_Involvement()
getDim_DateTime()
getDim_Period()
getDim_Dwelling()
getDim_Location()
getDim_LGA_Geometry()

# Reshape fact properties
print("Drop redundant properties in fact table ...")
fatality = fatality.drop(columns=toDrop)
fatality = fatality[['Fatality ID','Gender','Age','Road User','Crash ID','Involve ID','Date ID','Period Name','LGA Name','National Remoteness Areas','SA4 Name 2021']]

# Export fact table
fatality.to_csv("out/Fact_Fatality.csv", index = False)

# Status message
print("Cleansing complete!\n")