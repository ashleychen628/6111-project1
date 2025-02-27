import collections
import re
import glob
import numpy as np
from crawl_website import download_and_clean_html
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity




class QueryExpansion:
    def __init__(self, relevant_results, current_query, full_text):
        self.relevant_results = relevant_results
        self.current_query = current_query.casefold().split()
        self.full_text = full_text
        self.documents = self.process_documents()
        self.vectorizer, self.tfidf_matrix, self.feature_names = self.compute_tfidf(self.documents)

    def process_documents(self):
        """ Preprocess snippets: clean text, remove stopwords, and return as list. """
        documents = []
        file_path="proj1-stop.txt"
        with open(file_path, "r", encoding="utf-8") as file:
          stop_words_set = set(line.strip().lower() for line in file)
        
        filtered_full_text = " ".join([word for word in self.full_text if word not in stop_words_set])
        documents.append(filtered_full_text )
        
        return documents

    def compute_tfidf(self, documents):
        """ Computes TF-IDF vectors for documents and returns the vectorizer, matrix, and feature names. """
        vectorizer = TfidfVectorizer()  
        tfidf_matrix = vectorizer.fit_transform(documents)  
        feature_names = vectorizer.get_feature_names_out()  
        return vectorizer, tfidf_matrix, feature_names

    def select_top2_words(self):
        """ Extract the two most important words from the relevant results tagged by the user. """
        
        # Compute sum TF-IDF score for each word across all selected docs
        tfidf_scores = np.sum(self.tfidf_matrix.toarray(), axis=0)  
        
        # Sort words by TF-IDF score in descending order
        sorted_indices = np.argsort(tfidf_scores)[::-1]  # Get indices of top words
        sorted_words = self.feature_names[sorted_indices]  # Get words in descending TF-IDF order

        # Select words that are NOT already in the query
        new_words = []
        for word in sorted_words:
            if word not in self.current_query:
                new_words.append(word)
            if len(new_words) == 2:  
                break

        return new_words

    def reorder_query_vsm(self, expanded_query):
        """ Reorders the expanded query based on cosine similarity with relevant documents. """
        query_vectors = self.vectorizer.transform(expanded_query)
        similarity_scores = cosine_similarity(query_vectors, self.tfidf_matrix).mean(axis=1)

        # Sort words by descending cosine similarity
        reordered_query = [word for word, _ in sorted(zip(expanded_query, similarity_scores), key=lambda x: x[1], reverse=True)]
        return reordered_query

    def expand_and_reorder_query(self):
        """ Selects top 2 words using TF-IDF, then reorders full query using cosine similarity. """
        
        new_words = self.select_top2_words()
        expanded_query = self.current_query + new_words  # Combine old query with new words
        
        reordered_query = self.reorder_query_vsm(expanded_query)
        return reordered_query
