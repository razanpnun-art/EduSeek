import streamlit as st
import re
import html
from pathlib import Path
import pandas as pd
import pyterrier as pt
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

@st.cache_resource
def load_preprocessing():
    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()
    return stop_words, stemmer

stop_words, stemmer = load_preprocessing()

def normalize_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def remove_stopwords(text):
    words = text.split()
    filtered_words = [
        word for word in words if word not in stop_words
    ]
    return " ".join(filtered_words)

def stem_text(text):
    words = text.split()
    stemmed_words = [
        stemmer.stem(word) for word in words
    ]
    return " ".join(stemmed_words)

def preprocess_text(text):
    text = normalize_text(text)
    text = remove_stopwords(text)
    text = stem_text(text)
    return text
BASE_DIR = Path(__file__).parent
INDEX_FILE = BASE_DIR / "coursera_index" / "data.properties"
COLLECTION_FILE = BASE_DIR / "collection (11).csv"
TOP_K = 10


@st.cache_resource(show_spinner="Loading search index...")
def load_system():
    if not pt.java.started():
        pt.java.init()
    index = pt.IndexFactory.of(pt.IndexRef.of(str(INDEX_FILE)))
    retrievers = {
        "TF-IDF": pt.BatchRetrieve(
            index, controls={"wmodel": "TF_IDF"}, num_results=TOP_K
        ),
        "BM25": pt.BatchRetrieve(
            index, controls={"wmodel": "BM25"}, num_results=TOP_K
        ),
    }
    collection = pd.read_csv(COLLECTION_FILE, encoding="utf-8-sig")
    collection["docno"] = collection["docno"].astype(str)
    collection = collection.set_index("docno")
    return retrievers, collection


def search_courses(query, method):
    clean_query = preprocess_text(query)
    if not clean_query:
        return []

    retrievers, collection = load_system()
    queries = pd.DataFrame([{"qid": "1", "query": clean_query}])
    res = retrievers[method].transform(queries)

    results = []
    for _, row in res.iterrows():
        docno = str(row["docno"])
        title, text = "Unknown course", ""
        if docno in collection.index:
            title = str(collection.loc[docno, "title"])
            text = str(collection.loc[docno, "text"])
        results.append({
            "rank": int(row["rank"]) + 1,
            "title": title,
            "docno": docno,
            "score": float(row["score"]),
            "description": text[:250],
        })
    return results
st.set_page_config(
    page_title="EduSeek | Course Search",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #F4F8FC;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(120deg, #102C46, #176A79);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 28px;
}

.hero h1 {
    color: white;
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    color: #D3E5F2;
    font-size: 17px;
}

.result-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #DFE8EF;
    margin-bottom: 14px;
}

.result-title {
    color: #102C46;
    font-size: 20px;
    font-weight: 650;
}

.result-details {
    color: #64748B;
    font-size: 14px;
    margin-top: 8px;
}

.score {
    color: #137C85;
    font-weight: bold;
}

.stButton > button {
    background-color: #137C85;
    color: white;
    border-radius: 9px;
    border: none;
    padding: 10px 28px;
}

.stButton > button:hover {
    background-color: #0D6068;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🎓 EduSeek</h1>
    <p>Discover your next course</p>
    <p>Find relevant online courses using TF-IDF and BM25.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("🔎 Search Courses")

query = st.text_input(
    "What would you like to learn?",
    placeholder="e.g. Data Analysis with Python"
)

method = st.radio(
    "Select Retrieval Method",
    ["TF-IDF", "BM25"],
    horizontal=True
)

search = st.button("🔍 Search Courses")

if search:
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        st.divider()
        st.subheader("Search Results")

        st.write(f"**Query:** {query}")
        st.write(f"**Retrieval Method:** {method}")

        results = []
        try:
            results = search_courses(query, method)
        except Exception as e:
            st.error(f"Search failed: {e}")
        else:
            if not results:
                st.warning("No results found. Try different English keywords.")

        for course in results:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">
                    {course['rank']}. {html.escape(course['title'])}
                </div>
                <div class="result-details">
                    Document ID: {course['docno']}
                </div>
                <div class="result-details">
                    Relevance Score:
                    <span class="score">
                        {course['score']:.2f}
                    </span>
                </div>
                <div class="result-details">
                    {html.escape(course['description'])}...
                </div>
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.caption(
    "EduSeek | Information Retrieval Course Project"
)
