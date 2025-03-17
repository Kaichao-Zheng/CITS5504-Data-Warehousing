# CITS5504 Project 1

## Timeline

| Date            | Week      | Lectures                      | Labs                      | Project                    |
| :-------------- | :-------- | :---------------------------- | ------------------------- | -------------------------- |
| 24 Feb - 02 Mar | Week 1    | **Intro Data Warehousing**    | Lab 0	**Online  Quiz** | **Group Project 25%**      |
| 03 Mar - 09 Mar | Week 2    | Data Warehouse Design         | Lab 1-1                   | ✔Dataset analysis          |
| 10 Mar - 16 Mar | Week 3    | Data Cube Technologies        | Lab 1-2                   | ⌛ETL                       |
| 17 Mar - 23 Mar | Week 4    | Dimension Modelling           | Lab 1-3                   |                            |
| 24 Mar - 30 Mar | Week 5    | Association Rule Mining       | Lab 1-4	**Lab  Demo**  |                            |
| 31 Mar - 06 Apr | Week 6    | Data Marts and Metadata       | Lab 1-5	**Lab Demo**   |                            |
| 07 Apr - 13 Apr | Week 7    | **Intro Graph Databases**     | **Project Consultation**  | Due on 11 Apr              |
| 14 Apr - 20 Apr | Week 8    | Graph Data Modelling          | Lab 2-1                   |                            |
| 21 Apr - 27 Apr | **Break** |                               |                           |                            |
| 28 Apr - 04 May | Week 9    | *Guest Lecture*               | Lab 2-2                   | **Individual Project 20%** |
| 05 May - 11 May | Week 10   | Graph Queries - Cypher        | Lab 2-3                   |                            |
| 12 May - 18 May | Week 11   | Advanced Cypher               | Lab 2-4                   |                            |
| 19 May - 25 May | Week 12   | Path Finding and Graph Search | Lab 2-5                   | Due on 23 May              |
| 26 May - 01 Jun | **Break** |                               |                           |                            |



## Data Warehousing Flow Diagram

<img src="https://s2.loli.net/2025/03/03/d3Dw12vpkCO5BUf.png" alt="image.png" style="zoom:50%;" />

## Recommended Workflow

- [x] #### Requirements analysis

  N/A→CITS4401 Week2

  ##### Functional Requirements

  - Build a data warehouse to **store data**
    - ETL process
    - Data cleansing (no more than 5%)
  - Present key insight with a **dashboard/visualization**
  - Support **decision-making** with **data mining** techniques
    - List and describe a few suggestions
  - Provide **schema**, **starnet**, and **query footprints**

  ##### Non-Functional Requirements

  - Contains **3-4 datasets** and **8+ dimensions**
  - **Report has no page limitation**

- [ ] #### Business processes analysis

  N/A

- [x] #### Dataset analysis

  Week 3 Lecture

  1. Determine grains

  2. Determine 8+ dimensions:

     *Use italic to represent *measures*

     *Exclude <u>foreigner keys</u>

     - **Crash** (Crash_ID, Crash_Type, Speed Limit)
       - **Fatality** (<u>Fatality_ID</u>, Gender, Age)
       - **Involvement** (Bus_Involvement, Heavy_Rigid_Truck_Involvement, Articulated_Truck_Involvement)
       - **Date** (Year, Month, Dayweek, Time, Christmas_Period, Easter_Period)
       - **Location** (**GeoJSON**, State, SA4_Name)
         - **Local_Government_Area** (LGA_Code, National_LGA_Name, Estimated_Population)
           - **Dwelling** (Dwelling_Records)
       - **Remoteness** (Remoteness_Areas, Estimated_Population)

- [x] #### ETL⚠️(In progress) 

  Week 3 Lab

  ##### Data cleansing - divide, merge, reorder source data

  `import pandas as pd`

  ##### Data preprocessing - design measures

  

- [ ] #### Design dimension table and fact table

  Week 2-4 Lectures

- [ ] #### Depict data warehouse schema

  Week 2 Lecture

- [ ] #### Hierarchy and Starnet

  Week 2-3 Lectures

- [ ] #### Cube

  Week 3 Lecture

- [ ] #### Business queries

  N/A

- [ ] #### Results visualization

  Week 4-5 Labs

  * **GeoJSON**

- [ ] #### Association rules mining

  Week 5 Lecture + Week 6 Lab

## Details & Analysis

### Outcome

This project aims to showcase itself in personal [portfolio](https://www.w3schools.com/howto/howto_website_create_portfolio.asp)!

### Source Data Types

Integrating and Warehousing with:	.xlsx	.PDF	.Geojson	.CSV

### Association Rule Mining Requirements

Python only, see Week 5

## Design & Implementation

1. Determine grains
2. Determine 8 dimensions
3. 



# References

[UWA: IEEE Referencing Style Examples](https://guides.library.uwa.edu.au/IEEE/Examples)

⚠️Must **cite** suggestions from gen AI.

# Marking Scheme

Check [project gitbook](https://csse-uwa.gitbook.io/data-warehouse-project-1-s1-2025)
