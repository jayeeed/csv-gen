import requests
import pandas as pd
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define the CSV file paths
input_csv = "data/all_concept.csv"  # Input CSV containing concept_id
output_csv = "data/output.csv"  # Output CSV for storing results

# Read the concept_ids from the CSV file
concept_ids = pd.read_csv(input_csv)["concept_id"].tolist()


# Function to make a POST request for a given concept_id and category_id
def fetch_data(concept_id, category_id):
    # Format the URL with the actual concept_id and category_id
    url = f"https://api-play-staging.brightzy.com/word/game/level/{concept_id}/{category_id}/"
    json_body = {"vocabulary_ids": [], "category_question_ids": []}

    print(f"Making request to {url}")  # Print the API call in the terminal

    try:
        response = requests.post(url, json=json_body)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Check if the status is 1 for a successful response
        if data.get("status") == 1:
            print(
                f"Success: Received valid response for concept_id {concept_id} and category_id {category_id}"
            )
            return concept_id, category_id  # Return both concept_id and category_id
        else:
            print(
                f"Not found for concept_id {concept_id} and category_id {category_id}: {data.get('message')}"
            )
            return None  # Return None for unsuccessful responses

    except requests.exceptions.RequestException as e:
        print(
            f"Request failed for concept_id {concept_id} and category_id {category_id}: {e}"
        )
        return None  # Return None for failed requests


# Create a dictionary to store successful category_ids under their respective concept_ids
successful_results = {}

# Using ThreadPoolExecutor for concurrent API calls
with ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers as needed
    future_to_params = {
        executor.submit(fetch_data, concept_id, category_id): (concept_id, category_id)
        for concept_id in concept_ids
        for category_id in range(50, 1051)  # Loop from 50 to 1050
    }

    for future in as_completed(future_to_params):
        result = future.result()
        if result is not None:
            concept_id, category_id = result
            # Add the category_id to the list of category_ids for the concept_id
            if concept_id not in successful_results:
                successful_results[concept_id] = []
            successful_results[concept_id].append(category_id)

# Save the successful results to a CSV file
with open(output_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["concept_id", "category_id"])  # Write header
    for concept_id, category_ids in successful_results.items():
        for category_id in category_ids:
            writer.writerow(
                [concept_id, category_id]
            )  # Write each concept_id and corresponding category_id

print(f"Successful category_ids saved to {output_csv}")
