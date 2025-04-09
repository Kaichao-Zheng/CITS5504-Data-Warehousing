# CITS5504 Project 1

## Data Warehousing Flow Diagram

<img src="https://s2.loli.net/2025/03/03/d3Dw12vpkCO5BUf.png" alt="image.png" style="zoom:50%;" />

## Recommended Workflow

- [x] **Requirements analysis**

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

- [ ] **Business processes analysis**

  N/A

- [x] **Dataset analysis**

  Week 3-4 Lecture

  1. **Determine grains**

  1. **Determine 8+ dimensions:**

     *Use italic to represent *measures*

     *Exclude <u>foreigner keys</u>

     - **Fatality** (Fatality ID, Gender, Road User)✔️
       - **Age** (Age, Age Group)✔️
       - **Crash** (Crash ID, Crash Type, Speed Limit)✔️
       - **Involvement** (Bus Involvement, Heavy Rigid Truck Involvement, Articulated Truck Involvement)✔️
       - **DateTime** (Year, Month, Day of week, Time)✔️
       - **Period**(Period Name, Period Type)✔️
       - **Location** (<u>LGA Code</u>, <u>LGA Name</u>, State)✔️
         - **LGA** (<u>LGA Code</u>, **Coordinates**)✔️
         - **Dwelling** (<u>LGA Name</u>, Dwelling)✔️
  
- [x] **ETL (In progress)** 

  Week 3 Lab

  ##### Data cleansing - divide, merge, reorder source data

  `import pandas as pd`

  ##### Data preprocessing - design measures (Pending)

  

- [x] **Design dimension table and fact table**

  Week 2-4 Lectures

- [ ] **Depict data warehouse schema**

  Week 2 Lecture

- [ ] **Hierarchy and Starnet**

  Week 2-3 Lectures

- [ ] **Cube**

  Week 3 Lecture

- [ ] **Business queries**

  See lecture scenarios

  e.g. Week 4

  What is the average ticket fare for economy class passengers?  

  What is the average flight duration for flights to Europe in 2024?

  What is the maximum ticket fare for business class passengers whose membership is gold in Q4 2023?

- [ ] **Results visualization**

  Week 4-5 Labs

  * **GeoJSON**

- [ ] **Association rules mining**

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
