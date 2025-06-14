import pandas as pd
from sqlalchemy import create_engine

# Connect to your SQLite database
engine = create_engine("sqlite:///chat_logs.db")

# Load the chat_logs table into a DataFrame
df = pd.read_sql_table("chat_logs", con=engine)

# Export to CSV
df.to_csv("chat_logs_export.csv", index=False)

print("Chat logs exported to chat_logs_export.csv")
