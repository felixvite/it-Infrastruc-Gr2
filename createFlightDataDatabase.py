import pandas as pd
import sqlite3

# Load the CSV data into a pandas DataFrame
df = pd.read_csv('FlightData.csv')

# Create a connection to a SQLite database
conn = sqlite3.connect('FlightData.db')

# Write the data to a SQLite table
df.to_sql('flight_data', conn, if_exists='replace', index=False)

# Commit any changes and close the connection
conn.commit()
conn.close()
