import requests
import csv
from config import base_url

tags_url = base_url + "/tags/"
concept_url_template = base_url + "/word/game/concept/{}/1164/"


def fetch_lexile_concepts():
    response = requests.get(tags_url)
    tags_data = response.json()
    lexile_concepts = {}

    for tag in tags_data:
        lexile_framework = tag["lexile_framework"]
        if lexile_framework not in lexile_concepts:
            lexile_concepts[lexile_framework] = []

        concept_response = requests.get(concept_url_template.format(lexile_framework))
        concept_data = concept_response.json()

        for concept in concept_data.get("data", []):
            lexile_concepts[lexile_framework].append(concept["concept_id"])

    with open("data/lexile-concept.csv", mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["lexile_id", "concept_id"])
        for lexile_framework, concept_ids in lexile_concepts.items():
            writer.writerow([lexile_framework, ", ".join(map(str, concept_ids))])

    print("CSV file 'data/lexile-concept.csv' created successfully.")


if __name__ == "__main__":
    fetch_lexile_concepts()
