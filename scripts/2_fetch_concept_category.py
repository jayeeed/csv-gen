import requests
import csv
from config import base_url

category_url_template = base_url + "/word/game/category/{}/1164/"


def fetch_category_ids():
    concepts_file = "data/lexile-concept.csv"
    concept_categories = {}

    with open(concepts_file, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            concept_ids = row["concept_id"].split(", ")
            for concept_id in concept_ids:
                if concept_id not in concept_categories:
                    concept_categories[concept_id] = []

                category_response = requests.get(
                    category_url_template.format(concept_id)
                )
                category_data = category_response.json()

                for category in category_data.get("data", []):
                    concept_categories[concept_id].append(category["category_id"])

    with open("data/concept-category.csv", mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["concept_id", "category_id"])
        for concept_id, category_ids in concept_categories.items():
            writer.writerow([concept_id, ", ".join(map(str, category_ids))])

    print("CSV file 'data/concept-category.csv' created successfully.")


if __name__ == "__main__":
    fetch_category_ids()
