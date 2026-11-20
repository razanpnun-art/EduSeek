import streamlit as st

st.set_page_config(
    page_title="EduSeek",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduSeek")
st.subheader("Course Search Engine")

st.write("Find online courses using TF-IDF or BM25.")

st.divider()

query = st.text_input(
    "Search for courses",
    placeholder="Enter a course topic..."
)

method = st.radio(
    "Select Retrieval Method",
    ["TF-IDF", "BM25"],
    horizontal=True
)

if st.button("🔍 Search", type="primary"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        st.subheader("Search Results")
        st.write("Query:", query)
        st.write("Retrieval Method:", method)

        # Temporary sample results for frontend testing
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

        st.info("Demo results only. Retrieval integration is pending.")

        for course in sample_results:
            with st.container(border=True):
                st.markdown(
                    f"### {course['rank']}. {course['title']}"
                )
                st.write("Document ID:", course["docno"])
                st.write("Relevance Score:", course["score"])
