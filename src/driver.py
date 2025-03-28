import requests
import json

from google_search import google_search
from user_feedback import get_user_feedback
from query_expansion import QueryExpansion
from crawl_website import download_and_clean_html

# with open("config.json", "r") as config_file:
#     config = json.load(config_file)

# API_KEY = config["api_key"]
# CX_ID = config["cx_id"]

class InfoRetrieval:
    def __init__(self, target_precision, query, api_key, cx_id):
      """Recieve the target precision and user's query. """
      self.target_precision = target_precision
      self.query = query
      self.total_results = 10
      self.api_key = api_key
      self.cx_id = cx_id

    def start(self):
      """Start the searching process. """
      if self.query == None or self.target_precision == None:
          self.query = input("Search Here: ")
          self.target_precision = float(input("Enter target precision (0 to 1): "))
      else:
        while True:
            print("\n======================")
            print(f"Parameters:\nClient key  = {self.api_key}\nEngine key  = {self.cx_id}")
            print(f"Query       = {self.query}\nPrecision   = {self.target_precision:.1f}")
            print("======================\n")
            
            search_results = self.google_search()

            if not search_results or len(search_results) < 10:
                print("Not enough results. Stopping.")
                break

            relevant_results = self.get_user_feedback(search_results)
            precision = len(relevant_results) / self.total_results  # Precision@10

            print("\n======================")
            print("FEEDBACK SUMMARY")
            print(f"Query {self.query}")
            print(f"Precision {precision:.1f}")
            print("======================\n")

            if precision >= self.target_precision:
                print("Target precision reached. Stopping.")
                break
            elif precision == 0:
                print("No relevant results. Stopping.")
                break
            else:
                query_expansion = QueryExpansion(relevant_results, self.query)
                top2_words = query_expansion.expand_and_reorder_query()
                # self.query = self.query + " " + top2_words[0] + " " + top2_words[1]
                self.query = " ".join(top2_words)

    def google_search(self):
        """Query the Google API to get the top 10 result. """
        num_results=10

        url = "https://www.googleapis.com/customsearch/v1"
        params = {"key": self.api_key, "cx": self.cx_id, "q": self.query, "num": num_results}

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            results = response.json()
            search_results = []

            print("Google Search Results:\n======================")
            
            idx = 0
            for item in results.get("items", []):
                # Check if the obtained url is an html and ignore the non-html
                # TODO: add this explanation to README and explain we won't show the non-thml files
                # url = item.get("link", "")
                # res = requests.head(url)
                # TODO: handle non-htmls
                # content_type = response.headers.get("Content-Type", "")
                # print(content_type)
                # if "text/html" in content_type:
                    # print("an HTML page")
                url = item.get("link", "")
                # TODO: handle non-htmls
                # download_and_clean_html(url, idx)
                search_results.append({
                    "url": item.get("link", ""),
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", "")
                })
                
                idx = idx + 1
                # print(f"Result {idx}\n[\n URL: {search_results['url']}\n Title: {search_results['title']}\n Summary: {search_results['snippet']}\n]")
         
                    
            print("======================")
            return search_results
        else:
            print("API Error:", response.status_code, response.text)
            return None

    def get_user_feedback(self, search_results):
        """ Let users choose which search results are relevant and return relevant results marked by users. """
        relevant_results = []

        print("\nPlease mark relevant results (Y/N):")
        for idx, result in enumerate(search_results):
            print(f"\nResult {idx+1} \n[\nURL: {result['url']}\nTitle: {result['title']}\nSummary: {result['snippet']}]")
            print(f"\nRelevant (Y/N)?", end="")
            user_input = input().strip().lower()

            if user_input == "y":
                relevant_results.append(result)

        return relevant_results
