import streamlit as st
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root", password="rakshitha@2906", database="nutrition"
)
cursor = conn.cursor()


st.set_page_config(page_title="Nutrition Paradox Dashboard", layout="wide")
st.title("Nutrition Paradox Dashboard")


st.sidebar.header("Filters")
query_type = st.sidebar.radio(
    "Select Query Category",
    ["Obesity Queries", "Malnutrition Queries", "Combined Queries",]
)
year_filter = st.sidebar.selectbox("Select Year (where applicable):", list(range(2012, 2023)))


if query_type == "Obesity Queries":
    st.subheader("Obesity Queries")

    st.markdown("**1. Top 5 regions with highest average obesity in selected year**")
    query1 = f"""
    SELECT Region, AVG(Mean_Estimate) AS avg_obesity
    FROM obesity WHERE Year = {year_filter}
    GROUP BY Region ORDER BY avg_obesity DESC LIMIT 5
    """
    st.dataframe(pd.read_sql(query1, conn))

    st.markdown("**2. Top 5 countries with highest obesity estimates**")
    query2 = """
    SELECT Country, MAX(Mean_Estimate) AS max_obesity
    FROM obesity GROUP BY Country ORDER BY max_obesity DESC LIMIT 5
    """
    st.dataframe(pd.read_sql(query2, conn))

    st.markdown("**3. Obesity trend in India over the years**")
    query3 = """
    SELECT Year, AVG(Mean_Estimate) AS mean_value
    FROM obesity WHERE Country = 'India' GROUP BY Year
    """
    st.line_chart(pd.read_sql(query3, conn).set_index("Year"))

    st.markdown("**4. Average obesity by gender**")
    query4 = """
    SELECT Gender, AVG(Mean_Estimate) AS avg_obesity FROM obesity GROUP BY Gender
    """
    st.dataframe(pd.read_sql(query4, conn))

    st.markdown("**5. Country count by obesity level and age group**")
    query5 = """
    SELECT Age_Group, Obesity_Level, COUNT(*) AS count
    FROM obesity GROUP BY Age_Group, Obesity_Level
    """
    st.dataframe(pd.read_sql(query5, conn))

    st.markdown("**6. Top 5 most and least reliable countries by CI_Width**")
    query6a = """
    SELECT Country, AVG(CI_Width) AS avg_ci
    FROM obesity GROUP BY Country ORDER BY avg_ci DESC LIMIT 5
    """
    st.dataframe(pd.read_sql(query6a, conn))

    query6b = """
    SELECT Country, AVG(CI_Width) AS avg_ci
    FROM obesity GROUP BY Country ORDER BY avg_ci ASC LIMIT 5
    """
    st.dataframe(pd.read_sql(query6b, conn))

    st.markdown("**7. Average obesity by age group**")
    query7 = """
    SELECT Age_Group, AVG(Mean_Estimate) AS avg_obesity
    FROM obesity GROUP BY Age_Group
    """
    st.dataframe(pd.read_sql(query7, conn))

    st.markdown("**8. Top 10 consistent low obesity countries with low CI**")
    query8 = """
    SELECT Country
    FROM obesity GROUP BY Country
    HAVING AVG(Mean_Estimate) < 25 AND AVG(CI_Width) < 3
    LIMIT 10
    """
    st.dataframe(pd.read_sql(query8, conn))

    st.markdown("**9. Countries where female obesity exceeds male by large margin**")
    query9 = """
    SELECT f.Country, f.Year, f.Mean_Estimate AS Female_Obesity,
           m.Mean_Estimate AS Male_Obesity,
           (f.Mean_Estimate - m.Mean_Estimate) AS Difference
    FROM obesity f
    JOIN obesity m
      ON f.Country = m.Country AND f.Year = m.Year
    WHERE f.Gender = 'Female' AND m.Gender = 'Male'
      AND (f.Mean_Estimate - m.Mean_Estimate) > 5
    ORDER BY Difference DESC
    """
    st.dataframe(pd.read_sql(query9, conn))

    st.markdown("**10. Global average obesity percentage per year**")
    query10 = """
    SELECT Year, AVG(Mean_Estimate) AS global_avg_obesity
    FROM obesity GROUP BY Year
    """
    st.line_chart(pd.read_sql(query10, conn).set_index("Year"))


elif query_type == "Malnutrition Queries":
    st.subheader("Malnutrition Queries")

    st.markdown("**11. Average malnutrition by age group**")
    query11 = """
    SELECT Age_Group, AVG(Mean_Estimate)
    FROM malnutrition GROUP BY Age_Group
    """
    st.dataframe(pd.read_sql(query11, conn))

    st.markdown("**12. Top 5 countries with highest malnutrition**")
    query12 = """
    SELECT Country, MAX(Mean_Estimate)
    FROM malnutrition GROUP BY Country ORDER BY MAX(Mean_Estimate) DESC LIMIT 5
    """
    st.dataframe(pd.read_sql(query12, conn))

    st.markdown("**13. Malnutrition trend in Africa**")
    query13 = """
    SELECT Year, AVG(Mean_Estimate)
    FROM malnutrition WHERE Region = 'Africa' GROUP BY Year
    """
    st.line_chart(pd.read_sql(query13, conn).set_index("Year"))

    st.markdown("**14. Average malnutrition by gender**")
    query14 = """
    SELECT Gender, AVG(Mean_Estimate)
    FROM malnutrition GROUP BY Gender
    """
    st.dataframe(pd.read_sql(query14, conn))

    st.markdown("**15. CI width by malnutrition level and age group**")
    query15 = """
    SELECT Age_Group, Malnutrition_Level, AVG(CI_Width)
    FROM malnutrition GROUP BY Age_Group, Malnutrition_Level
    """
    st.dataframe(pd.read_sql(query15, conn))

    st.markdown("**16. Malnutrition trend in India, Nigeria, and Brazil**")
    query16 = """
    SELECT Country, Year, AVG(Mean_Estimate)
    FROM malnutrition
    WHERE Country IN ('India', 'Nigeria', 'Brazil')
    GROUP BY Country, Year
    """
    st.dataframe(pd.read_sql(query16, conn))

    st.markdown("**17. Regions with lowest average malnutrition**")
    query17 = """
    SELECT Region, AVG(Mean_Estimate)
    FROM malnutrition GROUP BY Region ORDER BY AVG(Mean_Estimate) ASC
    """
    st.dataframe(pd.read_sql(query17, conn))

    st.markdown("**18. Countries with rising malnutrition (yearly diff > 5)**")
    query18 = """
    SELECT Country, MAX(Mean_Estimate) - MIN(Mean_Estimate) AS diff
    FROM malnutrition GROUP BY Country HAVING diff > 5
    """
    st.dataframe(pd.read_sql(query18, conn))

    st.markdown("**19. Yearly min/max malnutrition comparison**")
    query19 = """
    SELECT Year, MIN(Mean_Estimate), MAX(Mean_Estimate)
    FROM malnutrition GROUP BY Year
    """
    st.dataframe(pd.read_sql(query19, conn))

    st.markdown("**20. Countries with high CI width in malnutrition data**")
    query20 = """
    SELECT * FROM malnutrition WHERE CI_Width > 5
    """
    st.dataframe(pd.read_sql(query20, conn))


elif query_type == "Combined Queries":
    st.subheader("Combined Queries")

    st.markdown("**21. Obesity vs malnutrition for selected countries**")
    query21 = """
    SELECT o.Country, o.Mean_Estimate AS Obesity, m.Mean_Estimate AS Malnutrition
    FROM obesity o JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
    WHERE o.Country IN ('India', 'USA', 'Nigeria', 'Brazil', 'Germany')
    """
    st.dataframe(pd.read_sql(query21, conn))

    st.markdown("**22. Gender disparity in obesity and malnutrition**")
    query22 = """
    SELECT o.Gender, AVG(o.Mean_Estimate) AS Obesity, AVG(m.Mean_Estimate) AS Malnutrition
    FROM obesity o JOIN malnutrition m ON o.Gender = m.Gender AND o.Year = m.Year
    GROUP BY o.Gender
    """
    st.dataframe(pd.read_sql(query22, conn))

    st.markdown("**23. Region-wise comparison: Africa vs Americas**")
    query23 = """
    SELECT o.Region, AVG(o.Mean_Estimate) AS Obesity, AVG(m.Mean_Estimate) AS Malnutrition
    FROM obesity o JOIN malnutrition m ON o.Region = m.Region AND o.Year = m.Year
    WHERE o.Region IN ('Africa', 'Americas Region')
    GROUP BY o.Region
    """
    st.dataframe(pd.read_sql(query23, conn))

    st.markdown("**24. Countries with high obesity and low malnutrition**")
    query24 = """
    SELECT o.Country
    FROM obesity o JOIN malnutrition m ON o.Country = m.Country AND o.Year = m.Year
    GROUP BY o.Country
    HAVING AVG(o.Mean_Estimate) > 30 AND AVG(m.Mean_Estimate) < 10
    """
    st.dataframe(pd.read_sql(query24, conn))

    st.markdown("**25. Age-wise trend of obesity and malnutrition over years**")
    query25 = """
    SELECT o.Year, o.Age_Group, AVG(o.Mean_Estimate) AS Obesity, AVG(m.Mean_Estimate) AS Malnutrition
    FROM obesity o JOIN malnutrition m ON o.Age_Group = m.Age_Group AND o.Year = m.Year
    GROUP BY o.Year, o.Age_Group
    """
    st.dataframe(pd.read_sql(query25, conn))

