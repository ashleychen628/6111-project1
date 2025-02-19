import requests
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

API_KEY = config["api_key"]
CX_ID = config["cx_id"]

def google_search(query, api_key, cx_id, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cx_id, "q": query, "num": num_results, "start": 1}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json()
        with open("../data/search_results.json", "w") as file:
            json.dump(results, file, indent=4)
        return results
    else:
        print("API Error:", response.status_code, response.text)
        return None
