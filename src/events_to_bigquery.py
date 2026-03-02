import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from google.cloud import bigquery



mysql_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="password",
    host="localhost",
    database="ecommerce_data"
)

mysql_engine = create_engine(mysql_url)



bq_client = bigquery.Client()

PROJECT_ID = "ecommerce-data-pipeline-488018"
DATASET = "ecommerce_dw"



print("Loading events to BigQuery...")

query = "SELECT * FROM ecommerce_events"
df = pd.read_sql(query, mysql_engine)

table_id = f"{PROJECT_ID}.{DATASET}.ecommerce_events"

job = bq_client.load_table_from_dataframe(df, table_id)
job.result()

print(" Events loaded successfully!")