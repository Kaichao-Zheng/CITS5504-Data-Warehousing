COPY Dim_Age FROM '/tmp/Dim_Age.csv' WITH (FORMAT csv, HEADER true);					-- Insert Age dimension data
COPY Dim_Crash FROM '/tmp/Dim_Crash.csv' WITH (FORMAT csv, HEADER true);				-- Insert Crash dimension data
COPY Dim_Involvement FROM '/tmp/Dim_Involvement.csv' WITH (FORMAT csv, HEADER true);	-- Insert Involvement dimension data
COPY Dim_DateTime FROM '/tmp/Dim_DateTime.csv' WITH (FORMAT csv, HEADER true);			-- Insert DateTime dimension data
COPY Dim_Period FROM '/tmp/Dim_Period.csv' WITH (FORMAT csv, HEADER true);				-- Insert Period dimension data
COPY Dim_Dwelling FROM '/tmp/Dim_Dwelling.csv' WITH (FORMAT csv, HEADER true);			-- Insert Dwelling dimension data
-- COPY Dim_LGA_Geometry FROM '/tmp/LGA_Geometry.json' WITH (FORMAT json, HEADER true);	-- Pseudo LGA_Geometry dimension data
COPY Dim_Location FROM '/tmp/Dim_Location.csv' WITH (FORMAT csv, HEADER true);			-- Insert Location dimension data
COPY Fact_Fatality FROM '/tmp/Fact_Fatality.csv' WITH (FORMAT csv, HEADER true);		-- Insert fatality fact table data