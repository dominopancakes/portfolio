#import psycopg2
from psycopg2.extras import execute_values
from db import get_connection
import pandas as pd # only import for autocomplete and hints

def load(df: pd.DataFrame, table_name: str):
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:

                cols = ", ".join(df.columns)
                values = [tuple(row) for row in df.itertuples(index=False)]

                sql = f"INSERT INTO {table_name} ({cols}) VALUES %s"

                execute_values(cur, sql, values)

                conn.commit()

                print(f"Loaded {len(df)} rows into '{table_name}'")

    except Exception as e:
        print("Load failed")
        print(f"Error: {e}")
        raise   # propagate error to main.py
        



