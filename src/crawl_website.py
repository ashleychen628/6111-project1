import requests
import re
import os
from bs4 import BeautifulSoup


def download_html(url, output_file):
    """
    Downloads a webpage and saves it as an HTML file.
    
    :param url: The URL to fetch.
    :param output_file: The filename to save the HTML content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"Downloaded and saved: {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def clean_html(file_path):
    """
    Reads an HTML file, extracts text, and cleans it for indexing.

    :param file_path: Path to the HTML file.
    :return: List of cleaned words (tokens).
    """
    with open(file_path, "r", encoding="utf-8") as file:
        raw_html = file.read()

    soup = BeautifulSoup(raw_html, "html.parser")

    for tag in soup(["script", "style", "meta", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = re.sub(r"[^a-zA-Z0-9.,±() ]+", "", text)
    text = text.casefold()

    tokens = text.split()

    with open("hi.txt", "w", encoding="utf-8") as file:
      file.write(" ".join(tokens))

    return tokens 

# Usage
url = "https://en.wikipedia.org/wiki/Milky_Way"  
output_file = "downloaded_content.html"
download_html(url, output_file)

html_file = "downloaded_content.html" 
tokens = clean_html(html_file)

print(tokens[:20])