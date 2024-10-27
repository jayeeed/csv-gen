import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import base_url

# Define base URL
BASE_URL = base_url + "/word/game/level/{}/{}/"

# Sample input file and output file paths
INPUT_FILE = "data/output.csv"  # Input CSV with concept_id and category_id
OUTPUT_FILE = "data/concept_category_nulls.csv"  # Output CSV with null information

# POST request payload
payload = {"vocabulary_ids": [], "category_question_ids": []}


def check_null_fields(concept_id, category_id):
    url = BASE_URL.format(concept_id, category_id)
    response = requests.post(url, json=payload)

    # Initialize list for null fields
    null_fields = []

    # If request is successful, analyze JSON response
    if response.status_code == 200:
        data = response.json().get("data", {}).get("game_data", {})

        # Check fields for null values
        if data.get("title_sound") is None:
            null_fields.append("title_sound")
        if data.get("problem", {}).get("image") is None:
            null_fields.append("image")
        if data.get("problem", {}).get("sound") is None:
            null_fields.append("sound")

        # Return the concept_id, category_id, and null fields found
        return concept_id, category_id, ", ".join(null_fields) if null_fields else "OK"
    else:
        print(
            f"Error: Failed to fetch data for concept_id {concept_id} and category_id {category_id}"
        )
        return concept_id, category_id, "Error"


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
        writer.writerow(["concept_id", "category_id", "nulls"])

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
                concept_id, category_id, nulls = future.result()
                print(f"{concept_id}, {category_id}: {nulls}")  # Print nulls to console
                writer.writerow([concept_id, category_id, nulls])  # Write result to CSV

    print("CSV file created successfully with nulls information.")


if __name__ == "__main__":
    main()
