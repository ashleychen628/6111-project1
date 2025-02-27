# 6111-project1

# Query Expansion with Relevance Feedback

## **Project Overview**
This project implements an **information retrieval system** that improves Google search results using **relevance feedback and query expansion**. The system refines user queries iteratively by incorporating **TF-IDF-based keyword selection** and **Vector Space Model (VSM) ordering** to enhance search precision.

The method follows an **interactive relevance feedback loop**, where:
1. The user issues an **initial query**.
2. The system retrieves the **top 10 results** using the **Google Custom Search API**.
3. The user **marks relevant results**.
4. The system **expands the query** by selecting **two important words** from relevant results using **TF-IDF ranking**.
5. The **expanded query is reordered** using **cosine similarity** to prioritize relevant terms.
6. The process repeats until the **desired precision@10** is met or no further improvements can be made.

## **Methodology**
This project implements **two key query expansion techniques**:

### **1. TF-IDF-Based Keyword Selection**
- Extracts **important words** from the **user-marked relevant search results**.
- Uses **TF-IDF scores** to rank words by importance.
- Selects **top 2 words** that are not already in the query.

#### Libraries Used for TF-IDF calculation
- sklearn.feature_extraction.text.TfidfVectorizer – Converts text into TF-IDF vectors for information retrieval.
- sklearn.metrics.pairwise.cosine_similarity – Computes cosine similarity to reorder query terms based on relevance.
  
### **2. Query Reordering using Vector Space Model (VSM)**
- Computes **cosine similarity** between query words and relevant document vectors.
- Reorders the **expanded query** to **prioritize more relevant terms**.
- Ensures the **original query words always remain at the front** to preserve intent.

## **Installation**
### **1. Clone the Repository**
```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo

// after creating your virtual environment
pip install -r requirements.txt

// after activate your env
./run <target_precision> "<your query>"
```

## **Code Structure**
```
|-- src
    |-- driver.py
    |-- query_expansion.py
    |-- crawl_website.py
|-- run
|-- requirements.txt
```

## **Future Improvements**
- Implement Rocchio Algorithm to weight relevant and non-relevant terms.
- Experiment with Word Embeddings (Word2Vec/BERT) for better query expansion.
- Integrate stopword removal & stemming for improved term selection.

