# src/logging_utils.py

import csv
import os

def log_to_csv(filename: str, data: dict):
    header = list(data.keys())
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
