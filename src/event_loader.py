import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import logging



connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="password",
    host="localhost",
    database="ecommerce_data"
)

engine = create_engine(connection_url)

logging.basicConfig(
    filename="event_loader.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



def load_events():

    print(" Loading Events into MySQL...")

    df = pd.read_csv("events/events.csv")

    df.to_sql(
        "ecommerce_events",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000
    )

    print(" Events inserted successfully")
    logging.info("Events loaded successfully")


if __name__ == "__main__":
    load_events()