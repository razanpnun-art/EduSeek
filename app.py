import streamlit as st
import re
from pathlib import Path
import pandas as pd
import pyterrier as pt
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
st.set_page_config(
    page_title="EduSeek | Course Search",
    page_icon="🎓",
    layout="centered"
)
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
INDEX_FILE = BASE_DIR / "data.properties"
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


# Website interface

st.title("🎓 EduSeek")

st.subheader("Knowledge is one search away.")

st.caption(
    "Discover courses that match your interests and learning goals."
)

st.write("")

with st.container(border=True):

    with st.form("search_form"):

        query = st.text_input(
            "What would you like to learn?",
            placeholder="e.g. Data Analysis with Python"
        )

        method = st.radio(
            "Select retrieval method",
            ["TF-IDF", "BM25"],
            horizontal=True
        )

        search = st.form_submit_button(
            "Search courses",
            type="primary",
            use_container_width=True
        )

if search:

    if not query.strip():
        st.warning("Please enter a search query.")

    else:

        results = []

        try:
            with st.spinner("Finding relevant courses..."):
                results = search_courses(query, method)

        except Exception as e:
            st.error(f"Search failed: {e}")

        else:

            if not results:
                st.warning(
                    "No results found. Try different English keywords."
                )

            else:

                st.divider()
                st.subheader("Search results")

                st.caption(
                    f'{len(results)} results for "{query}" · {method}'
                )

                for course in results:

                    with st.container(border=True):

                        left, right = st.columns([3, 1])

                        with left:
                            st.caption(
                                f"RANK {course['rank']:02d}"
                            )

                            st.subheader(course["title"])

                            st.caption(
                                f"Document ID: {course['docno']}"
                            )

                        with right:
                            st.metric(
                                "Relevance Score",
                                f"{course['score']:.6f}"
                            )

                        if course["description"]:
                            with st.expander("Course details"):
                                st.text(course["description"] + "...")

st.divider()
st.caption("EduSeek · Search. Discover. Learn.")
