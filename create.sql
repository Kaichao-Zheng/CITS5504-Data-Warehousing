-- Create dimension table for Age
CREATE TABLE Dim_Age (
    "Age"					VARCHAR(10) PRIMARY KEY,
    "Age Group"				VARCHAR(20)
);

-- Create dimension table for Crash
CREATE TABLE Dim_Crash (
    "Crash ID"				INTEGER PRIMARY KEY,
    "Crash Type"			VARCHAR(20),
	"Speed Limit"			VARCHAR(10),
	"National Road Type"	VARCHAR(50)
);

-- Create dimension table for Involvement
CREATE TABLE Dim_Involvement (
    "Involve ID"			VARCHAR(5) PRIMARY KEY,
    "Bus"					VARCHAR(10),
	"Heavy Rigid Truck"		VARCHAR(10),
	"Articulated Truck"		VARCHAR(10)
);

-- Create dimension table for DateTime
CREATE TABLE Dim_DateTime (
    "DateTime ID"			INTEGER PRIMARY KEY,
    "Month"					INTEGER,
	"Year"					INTEGER,
	"Day of Week"			VARCHAR(10),
	"Time"					VARCHAR(10)
);

-- Create dimension table for Period
CREATE TABLE Dim_Period (
    "Period Name"			VARCHAR(10) PRIMARY KEY,
    "Period Type"			VARCHAR(10)
);

-- Create dimension table for Dwelling
CREATE TABLE Dim_Dwelling (
    "LGA Name"				VARCHAR(50) PRIMARY KEY,
	"Dwelling"				VARCHAR(10)
);

-- -- Create dimension table for LGA_Geometry
-- CREATE TABLE Dim_LGA_Geometry (
--	"LGA Code"				VARCHAR(10) PRIMARY KEY,
--	"LGA Geometry"			GEOMETRY(MultiPolygon, 4326)	-- Placeholder datatype, doesn't work
-- );

-- Create dimension table for Location
CREATE TABLE Dim_Location (
    "LGA Code"				VARCHAR(10),
    "LGA Name"				VARCHAR(50) PRIMARY KEY,
	"State"					VARCHAR(10),
--	FOREIGN KEY ("LGA Code") REFERENCES Dim_LGA_Geometry("LGA Code"),
    FOREIGN KEY ("LGA Name") REFERENCES Dim_Dwelling("LGA Name")
);

-- Create fact table for fatality
CREATE TABLE Fact_Fatality (
    "Fatality ID"			INTEGER PRIMARY KEY,
    "Gender"				VARCHAR(10),
	"Age"					VARCHAR(10),
    "Road User"				VARCHAR(30),
    "Crash ID"				INTEGER,
    "Involve ID"			VARCHAR(5),
    "DateTime ID"			INTEGER,
    "Period Name"			VARCHAR(10),
    "LGA Name"				VARCHAR(50),
    "National Remoteness Areas" VARCHAR(30),
    "SA4 Name 2021"			VARCHAR(50),
    FOREIGN KEY ("Age") REFERENCES Dim_Age("Age"),
    FOREIGN KEY ("Crash ID") REFERENCES Dim_Crash("Crash ID"),
    FOREIGN KEY ("Involve ID") REFERENCES Dim_Involvement("Involve ID"),
    FOREIGN KEY ("DateTime ID") REFERENCES Dim_DateTime("DateTime ID"),
    FOREIGN KEY ("Period Name") REFERENCES Dim_Period("Period Name"),
    FOREIGN KEY ("LGA Name") REFERENCES Dim_Location("LGA Name")
);