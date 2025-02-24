import collections
import re
from crawl_website import download_and_clean_html
from sklearn.feature_extraction.text import TfidfVectorizer
import glob


class QueryExpansion:
  def __init__(self, relevant_results):
    self.relevant_results = relevant_results
  
  # def filter_stop_words(self, words, stop_words):
    # file_path="proj1-stop.txt"
    #     with open(file_path, "r", encoding="utf-8") as file:
    #     stop_words = set(line.strip().lower() for line in file)  # Convert to lowercase and store in a set
    #     # Example usage:
    #     stop_words = load_stop_words("proj1-stop.txt")  # Load stop words from the file
    #     words = ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]  # Example document
    #     filtered_words = filter_stop_words(words, stop_words)
    # return filtered_words

  def select_top2_words(self):
      """ Extract the two most important words from the relevant results tagged by the user. """

      # for re from relevant_results:
      #   url = re["url"]


      # text = " ".join([res["title"] + " " + res["snippet"] for res in self.relevant_results])
      # words = re.findall(r'\b\w+\b', text.lower())

      # # TODO: filter the stop words if necessary
      # word_counts = collections.Counter(filtered_words)
      # top_words = [w for w, _ in word_counts.most_common(2)]
      
      # Step 1: Read text files
    doc_files = glob.glob("path_to_txt_files/*.txt")  # Adjust the path to your folder
    documents = []

    for file in doc_files:
        with open(file, "r", encoding="utf-8") as f:
            documents.append(f.read().strip())  # Read and strip newlines

    # Step 2: Compute TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Step 3: Extract feature names (words) and their TF-IDF scores
    feature_names = vectorizer.get_feature_names_out()
    tfidf_array = tfidf_matrix.toarray()

    # Display TF-IDF results for each document
    for i, doc in enumerate(documents):
        print(f"\nDocument {i+1}:")
        for word, score in zip(feature_names, tfidf_array[i]):
            if score > 0:  # Ignore zero scores
                print(f"{word}: {score:.4f}")
      return top_words
