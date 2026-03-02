import pandas as pd
import os

CLEAN_PATH = "clean_data"

files = os.listdir(CLEAN_PATH)

print("Validating cleaned files...\n")

for file in files:
    if file.endswith(".csv"):
        path = os.path.join(CLEAN_PATH, file)
        df = pd.read_csv(path)

        print(f"File: {file}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print(f"Duplicate Rows: {df.duplicated().sum()}")
        print(f"Total Null Values: {df.isnull().sum().sum()}")
        print("-" * 50)

print("\nValidation complete.")