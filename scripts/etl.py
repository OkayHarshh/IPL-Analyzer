import pandas as pd
from sqlalchemy import create_engine

# Pandas display settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)

# MySQL connection engine
engine = create_engine('mysql+mysqlconnector://root:harsh009%40@127.0.0.1:3306/ipl')

# Load matches.csv
matches = pd.read_csv("IPL-Analyzer/IPL Dataset/matches.csv")
matches['date'] = pd.to_datetime(matches['date'], errors='coerce')
matches.to_sql("matches", con=engine, if_exists="replace", index=False)

# Load deliveries.csv
deliveries = pd.read_csv("IPL-Analyzer/IPL Dataset/deliveries.csv")
deliveries.fillna("None", inplace=True)
deliveries.to_sql("deliveries", con=engine, if_exists="replace", index=False)

print("✅ Data loaded to MySQL successfully.")
