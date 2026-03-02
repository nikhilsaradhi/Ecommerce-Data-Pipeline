import os
import pandas as pd
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError



connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="Nikhil@#.587",
    host="localhost",
    database="ecommerce_data"
)

engine = create_engine(connection_url)



DATA_PATH = "clean_data"   

TABLE_FILE_MAPPING = {
    "customers": "clean_customers.csv",
    "sellers": "clean_sellers.csv",
    "products": "clean_products.csv",
    "orders": "clean_orders.csv",
    "order_items": "clean_order_items.csv",
    "order_payments": "clean_order_payments.csv",
    "order_reviews": "clean_order_reviews.csv",
    "geolocation": "clean_geolocation.csv",
    "product_category_name_translation": "clean_product_category_name_translation.csv"
}



logging.basicConfig(
    filename="mysql_loader.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)








def load_table(table_name, file_name):
    try:
        file_path = os.path.join(DATA_PATH, file_name)

        print(f" Loading {table_name}...")
        logging.info(f"Starting load for {table_name}")

        df = pd.read_csv(file_path)

        df.to_sql(
            table_name,
            con=engine,
            if_exists="append",  
            index=False,
            chunksize=10000
        )

        print(f" {table_name} loaded successfully.")
        logging.info(f"{table_name} loaded successfully.")

    except FileNotFoundError:
        print(f" File not found: {file_name}")
        logging.error(f"File not found: {file_name}")

    except SQLAlchemyError as e:
        print(f" Database error for {table_name}: {e}")
        logging.error(f"Database error for {table_name}: {str(e)}")

    except Exception as e:
        print(f" Unexpected error for {table_name}: {e}")
        logging.error(f"Unexpected error for {table_name}: {str(e)}")




if __name__ == "__main__":
    print(" Starting Clean Data Load into MySQL\n")

    

    for table, file in TABLE_FILE_MAPPING.items():
        load_table(table, file)

    print("\n All clean datasets loaded successfully.")