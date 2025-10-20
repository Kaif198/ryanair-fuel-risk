import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

# Step 1: Load stock data (CSV)
print("Loading stock data...")
stock_df = pd.read_csv('data/ryanair_stock.csv', skiprows=14)
print("Stock data shape:", stock_df.shape)  # Shows rows/columns

# Clean stock: Parse dates, sort, drop duplicates/NaNs, resample to monthly average close
stock_df['date'] = pd.to_datetime(stock_df['date'])  # Note: Column is 'date' lowercase
stock_df = stock_df.sort_values('date').drop_duplicates('date')
stock_df = stock_df.dropna(subset=['close'])
stock_df['Month'] = stock_df['date'].dt.to_period('M')
stock_monthly = stock_df.groupby('Month')['close'].mean().reset_index()
stock_monthly['Month'] = stock_monthly['Month'].dt.to_timestamp()
print("Monthly stock shape:", stock_monthly.shape)

# Step 2: Load fuel data (XLS, weekly)
print("Loading fuel data...")
fuel_df = pd.read_excel('data/jet_fuel_prices.xls', sheet_name='Data 1', skiprows=2)  # Skip header rows
fuel_df.columns = ['Date', 'Price']  # Rename columns
print("Fuel data shape:", fuel_df.shape)

# Clean fuel: Parse dates (format like 'Sep 26, 2025'), sort, drop NaNs, resample monthly
fuel_df['Date'] = pd.to_datetime(fuel_df['Date'], format='%b %d, %Y')
fuel_df = fuel_df.sort_values('Date').drop_duplicates('Date')
fuel_df = fuel_df.dropna(subset=['Price'])
fuel_df['Month'] = fuel_df['Date'].dt.to_period('M')
fuel_monthly = fuel_df.groupby('Month')['Price'].mean().reset_index()
fuel_monthly['Month'] = fuel_monthly['Month'].dt.to_timestamp()
print("Monthly fuel shape:", fuel_monthly.shape)

# Step 3: Merge on Month (outer join, drop NaNs)
merged_df = pd.merge(stock_monthly, fuel_monthly, left_on='Month', right_on='Month', how='outer')
merged_df = merged_df.dropna()  # Remove rows missing stock or fuel
merged_df['Stock_Return'] = merged_df['close'].pct_change()  # % change for ML features
merged_df = merged_df.dropna()  # Clean after returns
print("Merged shape:", merged_df.shape)
print("Merged preview:\n", merged_df.head())

# Step 4: Save to SQLite DB
conn = sqlite3.connect('ryanair_data.db')
merged_df.to_sql('financial_data', conn, if_exists='replace', index=False)
conn.close()
print("Data saved to ryanair_data.db! Ready for modeling.")