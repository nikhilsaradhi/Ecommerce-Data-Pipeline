from google.cloud import bigquery
import os



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path of json key "



client = bigquery.Client()

print(" Connected to BigQuery")



datasets = list(client.list_datasets())

if datasets:
    print("\nAvailable datasets:")
    for dataset in datasets:
        print(dataset.dataset_id)
else:
    print("No datasets found.")
