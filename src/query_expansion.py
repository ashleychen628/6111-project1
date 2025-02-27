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
        """Extract the two most important words from relevant results and reorder the entire query."""

        documents = []
        stop_words_set = set()

        file_path = "proj1-stop.txt"
        with open(file_path, "r", encoding="utf-8") as file:
            stop_words_set = set(line.strip().lower() for line in file)

        for res in self.relevant_results:
            if res["full_text"]:
                text = re.sub(r"[^a-zA-Z0-9 ]+", "", " ".join(res["full_text"])).casefold()
            else:
                text = re.sub(r"[^a-zA-Z0-9 ]+", "", res["snippet"]).casefold()

            filtered_text = " ".join([word for word in text.split() if word not in stop_words_set])
            documents.append(filtered_text)

        original_query_text = " ".join(self.current_query)
        documents.append(original_query_text)

        vectorizer = TfidfVectorizer(lowercase=True)
        tfidf_matrix = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()

        tfidf_scores = np.sum(tfidf_matrix.toarray(), axis=0)
        word_score_map = {feature_names[i]: tfidf_scores[i] for i in range(len(feature_names))}

        new_words = []
        for word in sorted(word_score_map, key=word_score_map.get, reverse=True):
            if word not in self.current_query:
                new_words.append(word)
            if len(new_words) == 2:
                break


        all_query_words = self.current_query + new_words
        all_query_words_sorted = sorted(all_query_words, key=lambda w: word_score_map.get(w, 0), reverse=True)

        return " ".join(all_query_words_sorted)


