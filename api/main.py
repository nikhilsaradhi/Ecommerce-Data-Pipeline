

from fastapi import FastAPI
from google.cloud import bigquery
import pandas as pd
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    "config/ecommerce-key.json"

client = bigquery.Client()

PROJECT_ID = "ecommerce-data-pipeline-488018"
DATASET = "analytics"

app = FastAPI(title="Ecommerce Analytics API")


@app.get("/daily-orders")
def daily_orders():
    query = """
    SELECT *
    FROM `ecommerce-data-pipeline-488018.analytics.daily_orders`
    ORDER BY order_day
    """
    df = client.query(query).to_dataframe()
    return df.to_dict(orient="records")



@app.get("/monthly-orders")
def monthly_orders():
    query = """
    SELECT *
    FROM `ecommerce-data-pipeline-488018.analytics.monthly_orders`
    ORDER BY month
    """
    df = client.query(query).to_dataframe()
    return df.to_dict(orient="records")



@app.get("/top-products")
def top_products():
    query = """
    SELECT *
    FROM `ecommerce-data-pipeline-488018.analytics.top_products`
    ORDER BY total_orders DESC
    """
    df = client.query(query).to_dataframe()
    return df.to_dict(orient="records")



@app.get("/seller-city")
def seller_city():
    query = """
    SELECT *
    FROM `ecommerce-data-pipeline-488018.analytics.seller_revenue_city`
    ORDER BY revenue DESC
    """
    df = client.query(query).to_dataframe()
    return df.to_dict(orient="records")



@app.get("/category-contribution")
def category_contribution():
    query = """
    SELECT *
    FROM `ecommerce-data-pipeline-488018.analytics.category_contribution`
    ORDER BY total_orders DESC
    """
    df = client.query(query).to_dataframe()
    return df.to_dict(orient="records")