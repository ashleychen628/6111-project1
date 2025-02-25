import requests
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

API_KEY = config["api_key"]
CX_ID = config["cx_id"]

def google_search(query, api_key=API_KEY, cx_id=CX_ID, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cx_id, "q": query, "num": num_results}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        search_results = []

        for item in results.get("items", []):
            search_results.append({
                "url": item.get("link", ""),
                "title": item.get("title", ""),
                "snippet": item.get("snippet", "")
            })

        return search_results
    else:
        print("API Error:", response.status_code, response.text)
        return None
