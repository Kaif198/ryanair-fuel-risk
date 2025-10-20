import sqlite3
import pandas as pd

# Connect to DB
conn = sqlite3.connect('ryanair_data.db')
print("DB connected! Running scenarios...")

# Query 1: Overview
df_overview = pd.read_sql('SELECT COUNT(*) AS Total_Months FROM financial_data', conn)
df_dates = pd.read_sql('SELECT MIN(Month) AS Start_Date, MAX(Month) AS End_Date FROM financial_data', conn)
df_avgs = pd.read_sql('SELECT AVG(close) AS Avg_Stock_Price, AVG(Price) AS Avg_Fuel_Price FROM financial_data', conn)
print("1. Overview:")
print(df_overview)
print(df_dates)
print(df_avgs)
print()

# Query 2: Recent 10 months
df_recent = pd.read_sql('SELECT Month, close AS Stock_Price, Price AS Fuel_Price, Stock_Return FROM financial_data ORDER BY Month DESC LIMIT 10', conn)
print("2. Recent 10 months:")
print(df_recent)
print()

# Query 3: High Fuel Risk (Top 15 spikes)
df_risk = pd.read_sql('''
    SELECT 
        Month, 
        close AS Stock_Price, 
        Price AS Fuel_Price,
        Stock_Return,
        AVG(Price) OVER () AS Avg_Fuel,
        CASE 
            WHEN Price > (SELECT AVG(Price) FROM financial_data) * 1.2 
            THEN 'High Fuel Risk (Strategic Alert: Monitor Costs)'
            ELSE 'Normal'
        END AS Scenario_Flag
    FROM financial_data
    ORDER BY Price DESC
    LIMIT 15
''', conn)
print("3. High Fuel Risk (Top 15):")
print(df_risk)
print()

# Query 4: Summary Insights
df_summary = pd.read_sql('''
    SELECT 
        Scenario_Flag,
        COUNT(*) AS Num_Months,
        AVG(Stock_Return) AS Avg_Return_During,
        COUNT(CASE WHEN Stock_Return < -0.05 THEN 1 END) AS Num_Big_Drops
    FROM (
        SELECT 
            close,
            Price,
            Stock_Return,
            CASE 
                WHEN Price > (SELECT AVG(Price) FROM financial_data) * 1.2 
                THEN 'High Fuel Risk'
                ELSE 'Normal'
            END AS Scenario_Flag
        FROM financial_data
    )
    GROUP BY Scenario_Flag
''', conn)
print("4. Insights Summary:")
print(df_summary)
print()

# Export high-risk CSV for Power BI
df_risk.to_csv('data/scenario_fuel.csv', index=False)
print("Exported 'data/scenario_fuel.csv' for dashboard!")

conn.close()
print("Done! Insights ready.")