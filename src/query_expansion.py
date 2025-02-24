import collections
import re

class RefineQuery:
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

  def extract_keywords(self):
      """
      Extract the two most important words from the relevant results tagged by the user.
      """
      text = " ".join([res["title"] + " " + res["snippet"] for res in self.relevant_results])
      words = re.findall(r'\b\w+\b', text.lower())

      # TODO: filter the stop words if necessary
      word_counts = collections.Counter(filtered_words)
      top_words = [w for w, _ in word_counts.most_common(2)]

      return top_words