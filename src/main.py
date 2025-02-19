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
        print(f"Searching for: {query}")
        google_search(query, API_KEY, CX_ID)

        relevant_results = get_user_feedback()
        precision = len(relevant_results) / 10  # Precision@10

        print(f"Precision: {precision}")
        if precision >= target_precision or precision == 0:
            print("Stopping search refinement.")
            break

        new_words = extract_keywords()
        print(f"Expanding query with: {new_words}")
        
        query = query + " " + " ".join(new_words)  # Append new words
        print(f"New Query: {query}")

if __name__ == "__main__":
    main()
