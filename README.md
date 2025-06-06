
# Nutrition Paradox: A Global View on Obesity and Malnutrition



---

## Project Overview

The objective of this project is to:

- Understand regional and demographic patterns in obesity and malnutrition
- Measure the reliability of data using confidence interval width (CI_Width)
- Identify trends over time
- Present insights using a visual dashboard

---

## Data Sources

Data is retrieved via the WHO public API:

| Dataset Category     | API Code            |
|----------------------|---------------------|
| Adult Obesity        | `NCD_BMI_30C`       |
| Child Obesity        | `NCD_BMI_PLUS2C`    |
| Adult Malnutrition   | `NCD_BMI_18C`       |
| Child Malnutrition   | `NCD_BMI_MINUS2C`   |

Data is filtered to include years from 2012 to 2022.

---

## Data Preprocessing

- Fetched data from 4 WHO APIs
- Combined adult and child datasets
- Added derived columns:
  - `CI_Width = UpperBound - LowerBound`
  - `Obesity_Level`, `Malnutrition_Level`, `Age_Group`
- Converted ISO3 country codes to full names using `pycountry`
- Standardized gender values and filled missing regions
- Stored cleaned data in MySQL (`obesity`, `malnutrition` tables)

---

## Exploratory Data Analysis (EDA)

The EDA process includes:

- Distribution plots for `Mean_Estimate` and `CI_Width`
- Bar charts, box plots, and line plots for comparisons
- Multivariate analysis by region, age group, gender, and year
- Outlier detection using box plots
- Data quality analysis based on CI width

---

## SQL-Based Insights

The project includes 25 SQL queries divided into:

- Obesity Analysis (10 queries)
- Malnutrition Analysis (10 queries)
- Combined Comparisons (5 queries)

These queries answer key questions about health trends, vulnerable groups, and data reliability across regions.

---

## Streamlit Dashboard

An interactive dashboard built with Streamlit includes:

- Sidebar filters: Year, Query Category
- Displays SQL outputs with dataframes and charts
- Visual insights for obesity and malnutrition side-by-side
- Powered by a MySQL database backend


streamlit run streamlit_app.py
