import pandas as pd
import os
import logging
from datetime import datetime



DATA_PATH = "data"
CLEAN_PATH = "clean_data"


os.makedirs(CLEAN_PATH, exist_ok=True)


logging.basicConfig(
    filename="etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)






def clean_dataframe(df, table_name, primary_key=None, date_columns=None):

    print(f"\n🔹 Cleaning {table_name}...")
    original_count = len(df)

    
    df = df.drop_duplicates().copy()
    after_duplicates = len(df)
    print(f"Duplicates removed: {original_count - after_duplicates}")

    
    if primary_key and primary_key in df.columns:
        before_null = len(df)
        df = df[df[primary_key].notnull()].copy()
        after_null = len(df)
        print(f"Null {primary_key} removed: {before_null - after_null}")

   
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

   
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

   

   
    if "payment_value" in df.columns:
        before = len(df)
        df = df[df["payment_value"] >= 0]
        print(f"Invalid payment rows removed: {before - len(df)}")

    
    if "review_score" in df.columns:
        before = len(df)
        df = df[(df["review_score"] >= 1) & (df["review_score"] <= 5)]
        print(f"Invalid review rows removed: {before - len(df)}")

    
    if "product_weight_g" in df.columns:
        before = len(df)
        df = df[df["product_weight_g"] > 0]
        print(f"Invalid product rows removed: {before - len(df)}")

   

    

    final_count = len(df)

    logging.info(
        f"{table_name} | Before: {original_count}, After Cleaning: {final_count}"
    )

    print(f"Final rows after cleaning: {final_count}")

    return df


    


def clean_table(file_name, table_name, primary_key=None, date_columns=None):

    df = pd.read_csv(f"{DATA_PATH}/{file_name}")
    df = clean_dataframe(
        df,
        table_name=table_name,
        primary_key=primary_key,
        date_columns=date_columns
    )

    df.to_csv(f"{CLEAN_PATH}/clean_{file_name}", index=False)
    print(f" {table_name} cleaned successfully.")




if __name__ == "__main__":

    print(" Starting ETL Pipeline")

    clean_table("customers.csv", "customers", primary_key="customer_id")

    clean_table(
        "orders.csv",
        "orders",
        primary_key="order_id",
        date_columns=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    )

    clean_table("products.csv", "products", primary_key="product_id")

    clean_table("sellers.csv", "sellers", primary_key="seller_id")

    clean_table("order_payments.csv", "order_payments")

    clean_table(
        "order_reviews.csv",
        "order_reviews",
        primary_key="review_id",
        date_columns=[
            "review_creation_date",
            "review_answer_timestamp"
        ]
    )

    clean_table(
        "order_items.csv",
        "order_items",
        date_columns=["shipping_limit_date"]
    )

    clean_table("geolocation.csv", "geolocation")

    clean_table(
        "product_category_name_translation.csv",
        "product_category_name_translation"
    )

    print("\n ETL Cleaning Completed Successfully.")