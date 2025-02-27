import collections
import re
from crawl_website import download_and_clean_html
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import numpy as np


class QueryExpansion:
    def __init__(self, relevant_results, current_query):
        self.relevant_results = relevant_results
        self.current_query = current_query.split()

    def select_top2_words(self):
        """ Extract the two most important words from the relevant results tagged by the user,
            and reorder the entire query based on TF-IDF scores. """

        documents = []
        file_path = "proj1-stop.txt"


        with open(file_path, "r", encoding="utf-8") as file:
            stop_words_set = set(line.strip().lower() for line in file)

        for res in self.relevant_results:
            snippet = re.sub(r"[^a-zA-Z0-9 ]+", "", res["snippet"]).casefold()
            filtered_snippet = " ".join([word for word in snippet.split() if word not in stop_words_set])
            documents.append(filtered_snippet)

        original_query_text = " ".join(self.current_query)
        documents.append(original_query_text)

        vectorizer = TfidfVectorizer(lowercase=True)
        tfidf_matrix = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()

        tfidf_scores = np.sum(tfidf_matrix.toarray(), axis=0)

        sorted_indices = np.argsort(tfidf_scores)[::-1]
        sorted_words = feature_names[sorted_indices]

        new_words = []
        for word in sorted_words:
            if word not in self.current_query:
                new_words.append(word)
            if len(new_words) == 2:
                break


        all_query_words = list(set(self.current_query + new_words))
        all_query_words_sorted = sorted(all_query_words, key=lambda w: tfidf_scores[feature_names.tolist().index(w)], reverse=True)
        print(sorted_words)
        print(all_query_words_sorted)

        return all_query_words_sorted


