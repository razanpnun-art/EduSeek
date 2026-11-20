import streamlit as st

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

        # Temporary frontend data
        # Replace with real retrieval results later
        sample_results = [
            {
                "rank": 1,
                "title": "Data Analysis in Python",
                "docno": "6559",
                "score": 0.92
            },
            {
                "rank": 2,
                "title": "Python Data Analytics",
                "docno": "3304",
                "score": 0.85
            },
            {
                "rank": 3,
                "title": "Foundations of Data Analysis",
                "docno": "782",
                "score": 0.78
            }
        ]

        st.info(
            "Demo results only. "
            "Real retrieval integration is pending."
        )

        for course in sample_results:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">
                    {course['rank']}. {course['title']}
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
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.caption(
    "EduSeek | Information Retrieval Course Project"
)
