import json
from google_search import google_search
from user_feedback import get_user_feedback
from query_expansion import extract_keywords

with open("config.json", "r") as config_file:
    config = json.load(config_file)

API_KEY = config["api_key"]
CX_ID = config["cx_id"]

def main():
    query = input("Enter initial query: ")
    target_precision = float(input("Enter target precision (0 to 1): "))

    while True:
        print(f"\nSearching for: {query}")
        search_results = google_search(query, API_KEY, CX_ID)

        if not search_results or len(search_results) < 10:
            print("Not enough results. Stopping.")
            break

        relevant_results = get_user_feedback(search_results)
        precision = len(relevant_results) / 10  # Precision@10

        print(f"\nPrecision: {precision:.2f}")

        if precision >= target_precision:
            print("Target precision reached. Stopping.")
            break
        elif precision == 0:
            print("No relevant results. Stopping.")
            break

        new_words = extract_keywords(relevant_results)
        print(f"\nExpanding query with: {new_words}")

        query = query + " " + " ".join(new_words)
        print(f"New Query: {query}")

if __name__ == "__main__":
    main()

