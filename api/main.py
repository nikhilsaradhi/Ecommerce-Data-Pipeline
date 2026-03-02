from fastapi import FastAPI, Query, HTTPException
from google.cloud import bigquery
import os



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/ecommerce-key.json"

PROJECT_ID = "ecommerce-data-pipeline-488018"
DATASET = "analytics"

app = FastAPI(title="E-Commerce Analytics API")

client = bigquery.Client(project=PROJECT_ID)



def run_query(query: str):
    try:
        df = client.query(query).to_dataframe()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/orders")
def get_orders(view: str = Query("monthly", enum=["monthly", "daily"])):

    if view == "daily":
        table = "daily_orders"
        order_column = "order_day"
    else:
        table = "monthly_orders"
        order_column = "month"

    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{table}`
        ORDER BY {order_column}
    """

    return run_query(query)



@app.get("/top-products")
def top_products(top_n: int = 10):

    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.top_products`
        ORDER BY total_orders DESC
        LIMIT {top_n}
    """

    return run_query(query)



@app.get("/seller-city")
def seller_city(top_n: int = 10):

    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.seller_revenue_city`
        ORDER BY revenue DESC
        LIMIT {top_n}
    """

    return run_query(query)



@app.get("/category-contribution")
def category_contribution(top_n: int = 6):

    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.category_contribution`
        ORDER BY total_orders DESC
        LIMIT {top_n}
    """


    return run_query(query)


    

    