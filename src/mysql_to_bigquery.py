import pandas as pd
from sqlalchemy import create_engine
from google.cloud import bigquery



from sqlalchemy.engine import URL
from sqlalchemy import create_engine

mysql_url = URL.create(
    drivername="mysql+pymysql",
    username="your username",
    password="your password",  
    host="localhost",
    database="ecommerce_data"
)

mysql_engine = create_engine(mysql_url)



from google.cloud import bigquery

bq_client = bigquery.Client(
    project="ecommerce-data-pipeline-488018",
    location="asia-south1"   
)

DATASET = "ecommerce_dw"

TABLES = [
    "dim_customers",
    "dim_products",
    "dim_sellers",
    "dim_date",
    "fact_orders",
    "fact_payments",
    "fact_reviews",
    "fact_events"
]



def load_table_to_bigquery(table):

    print(f"\n Loading {table} to BigQuery...")

    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, mysql_engine)

    table_id = f"{bq_client.project}.{DATASET}.{table}"

    job = bq_client.load_table_from_dataframe(
        df,
        table_id
    )

    job.result()

    print(f" {table} loaded successfully.")




if __name__ == "__main__":

    print(" MySQL → BigQuery Loading Started")

    for table in TABLES:
        load_table_to_bigquery(table)

    print("\n All tables loaded into BigQuery!")
