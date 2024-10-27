import requests
import csv
from config import base_url

level_url_template = base_url + "/word/game/level/{}/{}"

input_csv_file = "data/concept-category.csv"
output_csv_file = "data/concepts-nulls.csv"


def fetch_concepts_with_null():
    concepts_with_null = []

    with open(input_csv_file, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            concept_id = row["concept_id"]
            category_ids = row["category_id"].split(", ")

            for category_id in category_ids:
                api_url = level_url_template.format(concept_id, category_id)

                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json().get("data", [])

                    for concept in data:
                        title_sound = concept.get("title_sound")
                        image = concept.get("image")
                        sound = concept.get("sound")

                        if title_sound is None or image is None or sound is None:
                            concepts_with_null.append(concept_id)
                            break

    with open(output_csv_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["concept_id"])

        for concept_id in set(concepts_with_null):
            writer.writerow([concept_id])

    print(f"CSV file '{output_csv_file}' created successfully.")


if __name__ == "__main__":
    fetch_concepts_with_null()
