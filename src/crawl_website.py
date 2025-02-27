import requests
import re
import os
from bs4 import BeautifulSoup

# def download_html(url, output_file):
#     """ Downloads a webpage and saves it as an HTML file. """
#     try:
#         response = requests.get(url)
#         response.raise_for_status()

#         with open(output_file, "w", encoding="utf-8") as file:
#             file.write(response.text)

#         print(f"Downloaded and saved: {output_file}")

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
DOC_PATH = "../data/relevant_docs"

if not os.path.exists(DOC_PATH):
    os.makedirs(DOC_PATH)

def download_and_clean_html(url, index):
    """ Reads an HTML file, extracts text, and cleans it for indexing. """
    try:
        # response = requests.get(url)
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 403:
            return None
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "meta", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        # text = re.sub(r"[^a-zA-Z0-9.,() ]+", "", text)
        text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
        
        text = text.casefold()

        tokens = text.split()

        if not os.path.exists(DOC_PATH):
            os.makedirs(DOC_PATH)

        next_index = index + 1 

        file_path = os.path.join(DOC_PATH, f"document{next_index}.txt")

        with open(file_path, "w", encoding="utf-8") as file:
          file.write(" ".join(tokens))
        
        return tokens 
          
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
   
# # Usage
# url = "https://www.milkywaybar.com/"  
# output_file = "downloaded_content.html"
# # download_html(url, output_file)

# html_file = "downloaded_content.html" 
# tokens = download_and_clean_html(url, 1)

# print(tokens[:20])