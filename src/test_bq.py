from google.cloud import bigquery
import os



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\kandu\\Desktop\\ecommerce-event-pipeline\\config\\ecommerce-data-pipeline-488018-74b96fd452be.json"



client = bigquery.Client()

print(" Connected to BigQuery")



datasets = list(client.list_datasets())

if datasets:
    print("\nAvailable datasets:")
    for dataset in datasets:
        print(dataset.dataset_id)
else:
    print("No datasets found.")