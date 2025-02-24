import collections
import re

def extract_keywords(relevant_results):
    """
    Extract the two most important words from the relevant results tagged by the user
    """
    text = " ".join([res["title"] + " " + res["snippet"] for res in relevant_results])
    words = re.findall(r'\b\w+\b', text.lower())

    stop_words = {"the", "is", "at", "of", "on", "and", "a", "to", "in"}  # expandable
    filtered_words = [w for w in words if w not in stop_words]

    word_counts = collections.Counter(filtered_words)
    top_words = [w for w, _ in word_counts.most_common(2)]

    return top_words