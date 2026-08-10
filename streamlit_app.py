import streamlit as st

from rag import MovieRAG


st.set_page_config(
    page_title="Vanilla RAG - Movie Search",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Vanilla RAG - Movie Search")
st.markdown(
    "Ask natural-language questions about movies using RAG with Grok and Weaviate."
)


# --------------------------------------------------------------------
# Input
# --------------------------------------------------------------------

question = st.text_input(
    "Ask your question",
    placeholder="Example: Which action movie between 2012 and 2014 had the highest IMDb rating?"
)

limit = st.number_input(
    "Number of results",
    min_value=1,
    max_value=20,
    value=5
)


# --------------------------------------------------------------------
# Button
# --------------------------------------------------------------------

if st.button("Generate Result"):

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    rag = None

    try:

        with st.spinner("Searching movies and generating answer..."):

            rag = MovieRAG()

            answer = rag.ask(
                query=question,
                limit=limit
            )

        st.success("Answer generated successfully!")

        # ------------------------------------------------------------
        # Final Answer
        # ------------------------------------------------------------

        st.subheader("Answer")

        st.markdown(answer)

    except Exception as e:

        st.error(str(e))

    finally:

        if rag is not None:

            rag.close()