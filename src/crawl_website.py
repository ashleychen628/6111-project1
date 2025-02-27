import requests
import re
import os
from bs4 import BeautifulSoup

DOC_PATH = "../data/relevant_docs"

def download_and_clean_html(url_list):
    """ Reads an HTML file, extracts text, and cleans it for indexing. """
    full_text = []

    for url in url_list:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "meta", "noscript"]):
                tag.decompose()
        
            text = soup.get_text(separator=" ")

            text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
     
            text = text.casefold().split()

            full_text += text
    
    return full_text
        