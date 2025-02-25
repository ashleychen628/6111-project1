import collections
import re
from crawl_website import download_and_clean_html
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import numpy as np



class QueryExpansion:
    def __init__(self, relevant_results, current_query):
        self.relevant_results = relevant_results
        self.current_query = current_query


    def select_top2_words(self):
        """ Extract the two most important words from the relevant results tagged by the user. """

        documents = []
        file_path="proj1-stop.txt"
        with open(file_path, "r", encoding="utf-8") as file:
          stop_words_set = set(line.strip().lower() for line in file)
        
        for res in self.relevant_results:
            snippet = re.sub(r"[^a-zA-Z0-9 ]+", "", res["snippet"]).casefold()
            filtered_snippet = " ".join([word for word in snippet.split() if word not in stop_words_set])
            documents.append(filtered_snippet)

        # Compute TF-IDF for the selected relevant documents
        vectorizer = TfidfVectorizer()  
        tfidf_matrix = vectorizer.fit_transform(documents)  
        feature_names = vectorizer.get_feature_names_out()  
        
        # Compute sum TF-IDF score for each word across all selected docs
        tfidf_scores = np.sum(tfidf_matrix.toarray(), axis=0)  
        
        # Sort words by TF-IDF score in descending order
        sorted_indices = np.argsort(tfidf_scores)[::-1]  # Get indices of top words
        sorted_words = feature_names[sorted_indices]  # Get words in descending TF-IDF order

        # Select words that are NOT already in the query
        new_words = []
        for word in sorted_words:
            if word not in self.current_query.casefold():
                new_words.append(word)
            if len(new_words) == 2:  
                break

        return new_words
