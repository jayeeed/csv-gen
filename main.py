import subprocess


def main():
    try:
        print("Fetching Lexile to Concept...")
        subprocess.run(["python", "scripts/1_fetch_lexile_concept.py"], check=True)

        print("Fetching Concept to Category...")
        subprocess.run(["python", "scripts/2_fetch_concept_category.py"], check=True)

        print("Fetching Concept to nulls...")
        subprocess.run(["python", "scripts/3_fetch_concept_nulls.py"], check=True)

        print("Fetching Category to Category...")
        subprocess.run(["python", "scripts/4_fetch_category_nulls.py"], check=True)

        print("Data fetching completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the scripts: {e}")


if __name__ == "__main__":
    main()
