import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import base_url

# Define base URL
BASE_URL = base_url + "/word/game/level/{}/{}/"

# Sample input file and output file paths
INPUT_FILE = "data/2_concept_category.csv"  # Input CSV with concept_id and category_id
OUTPUT_FILE = (
    "data/concept_category_nulls_extended.csv"  # Output CSV with null information
)

# POST request payload
payload = {"vocabulary_ids": [], "category_question_ids": []}


def find_null_keys(data, prefix=""):
    """
    Recursively finds all keys with null values in a nested dictionary and returns them as a list.
    """
    null_keys = []
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if value is None:
            null_keys.append(full_key)
        elif isinstance(value, dict):
            null_keys.extend(find_null_keys(value, full_key))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    null_keys.extend(find_null_keys(item, f"{full_key}[{i}]"))
    return null_keys


def check_null_fields(concept_id, category_id):
    url = BASE_URL.format(concept_id, category_id)
    response = requests.post(url, json=payload)

    # If request is successful, analyze JSON response
    if response.status_code == 200:
        data = response.json()
        null_keys = find_null_keys(data)

        # Format output based on whether null keys were found
        nulls = ", ".join(null_keys) if null_keys else "OK"
        return concept_id, category_id, nulls, url
    else:
        print(
            f"Error: Failed to fetch data for concept_id {concept_id} and category_id {category_id}"
        )
        return concept_id, category_id, "Error", url


def main():
    # Read input CSV file
    with open(INPUT_FILE, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        concept_category_pairs = [
            (row["concept_id"], row["category_id"]) for row in reader
        ]

    # Prepare CSV for output
    with open(OUTPUT_FILE, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["concept_id", "category_id", "nulls", "api_url"])

        # Use ThreadPoolExecutor to handle multiple requests concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit tasks to the executor
            future_to_concept_category = {
                executor.submit(check_null_fields, concept_id, category_id): (
                    concept_id,
                    category_id,
                )
                for concept_id, category_id in concept_category_pairs
            }

            # Collect results as they complete
            for future in as_completed(future_to_concept_category):
                concept_id, category_id, nulls, url = future.result()
                print(f"{concept_id}, {category_id}: {nulls}")  # Print nulls to console
                writer.writerow(
                    [concept_id, category_id, nulls, url]
                )  # Write result to CSV

    print("CSV file created successfully with nulls information.")


if __name__ == "__main__":
    main()
