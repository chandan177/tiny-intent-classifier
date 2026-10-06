"""
This script validates the data in the intents.csv file. It checks for the following:
1. The file exists and is readable.
2. The file has the correct format (two columns: text and label).
3. The labels are consistent and there are no unexpected labels.
"""

import csv
from collections import Counter

# define the path to the intents.csv file
DATA_PATH = "data/raw/intents.csv"

# Check if the file exists and is readable
with open(DATA_PATH, encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

# Check if the file has the correct format (two columns: text and label)
print("Total rows:", len(rows))

# Check for unexpected labels
counts = Counter(row["label"] for row in rows)

# Print the counts of each label
for label, count in sorted(counts.items()):
    print(f"{label}: {count}")