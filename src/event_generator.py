import pandas as pd
import uuid
import random
from faker import Faker
from datetime import datetime

fake = Faker()

EVENT_TYPES = [
    "page_view",
    "product_view",
    "search",
    "add_to_cart",
    "remove_from_cart",
    "checkout_started",
    "payment_attempt",
    "payment_success",
    "payment_failed",
    "order_cancelled",
    "order_delivered",
    "review_submitted"
]



customers = pd.read_csv("clean_data/clean_customers.csv")
products = pd.read_csv("clean_data/clean_products.csv")
orders = pd.read_csv("clean_data/clean_orders.csv")

customer_ids = customers["customer_id"].tolist()
product_ids = products["product_id"].tolist()
order_ids = orders["order_id"].tolist()



def generate_event():

    return {
        "event_id": str(uuid.uuid4()),
        "event_type": random.choice(EVENT_TYPES),
        "customer_id": random.choice(customer_ids),
        "product_id": random.choice(product_ids),
        "order_id": random.choice(order_ids),
        "event_timestamp": datetime.now(),
        "device": random.choice(["mobile", "web", "tablet"]),
        "city": fake.city(),
        "country": fake.country()
    }


def generate_events(n=1000):

    events = [generate_event() for _ in range(n)]

    df = pd.DataFrame(events)

    df.to_csv("events/events.csv", index=False)

    print(f" {n} events generated successfully")


if __name__ == "__main__":
    generate_events(5000)