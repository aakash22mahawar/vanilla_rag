import json

from logging_config import setup_logger

from weaviate_client import WeaviateClient
from llm import LLMClient
from query_parser import QueryParser, MovieQueryFilters

# Initialize the logger

logger = setup_logger()


class MovieRAG:

    def __init__(self):

        self.weaviate_client = WeaviateClient()
        self.llm_client = LLMClient()
        self.query_parser = QueryParser(
            self.llm_client
        )

        try:

            self.weaviate_client.connect()

            logger.info(
                "Movie RAG initialized successfully!"
            )

        except Exception as e:

            logger.error(
                f"Movie RAG initialization failed: {e}"
            )

            raise


    # -----------------------------
    # Retrieve relevant movie data
    # -----------------------------

    def retrieve_context(
        self,
        query: str,
        filters: MovieQueryFilters,
        limit: int = 5
    ) -> list:

        try:

            logger.info(
                f"Retrieving movie context for query: {query}"
            )

            results = self.weaviate_client.search_movies(
                query=query,
                genre=filters.genre,
                start_year=filters.start_year,
                end_year=filters.end_year,
                sort_by=filters.sort_by,
                sort_order=filters.sort_order,
                limit=limit
            )

            logger.info(
                f"Successfully retrieved {len(results)} movie records."
            )

            return results

        except Exception as e:

            logger.error(
                f"Movie context retrieval failed: {e}"
            )

            raise


    # -----------------------------
    # Generate answer using LLM
    # -----------------------------

    def generate_answer(
        self,
        query: str,
        context: list
    ) -> str:

        try:

            context_text = json.dumps(
                context,
                indent=2,
                ensure_ascii=False
            )

            prompt = f"""
                You are a movie information assistant.

                Answer the user's question using ONLY the movie
                information provided in the context below.

                If the context does not contain enough information
                to answer the question, clearly state that the
                available movie data is insufficient.

                Do not invent movie information.

                Context:
                {context_text}

                User question:
                {query}

                Provide a clear and concise answer.
                """

            logger.info(
                "Sending retrieved context to LLM."
            )

            response = self.llm_client.generate(
                prompt=prompt
            )

            logger.info(
                "LLM answer generated successfully."
            )

            return response

        except Exception as e:

            logger.error(
                f"LLM answer generation failed: {e}"
            )

            raise


    # -----------------------------
    # Execute RAG pipeline
    # -----------------------------

    def ask(
        self,
        query: str,
        limit: int = 5
    ) -> str:

        try:

            logger.info(
                f"Starting RAG pipeline for query: {query}"
            )

            # Extract structured filters from user query

            filters = self.query_parser.parse(
                query=query
            )

            logger.info(
                f"Parsed query filters: {filters.model_dump()}"
            )

            # Retrieve relevant context

            context = self.retrieve_context(
                query=query,
                filters=filters,
                limit=limit
            )

            # Generate final answer

            answer = self.generate_answer(
                query=query,
                context=context
            )

            logger.info(
                "RAG pipeline completed successfully."
            )

            return answer

        except Exception as e:

            logger.error(
                f"RAG pipeline failed: {e}"
            )

            raise


    # -----------------------------
    # Close resources
    # -----------------------------

    def close(self):

        try:

            self.weaviate_client.close()

            logger.info(
                "RAG resources closed successfully."
            )

        except Exception as e:

            logger.error(
                f"Failed to close RAG resources: {e}"
            )

            raise


# -----------------------------
# Test the RAG pipeline
# -----------------------------

# if __name__ == "__main__":

#     rag = MovieRAG()

#     try:

#         query = (
#             "Which action movie between 2012 and 2014 had the highest IMDb rating?"
#         )

#         answer = rag.ask(
#             query=query,
#             limit=5
#         )

#         print("\n" + "=" * 80)
#         print("RAG ANSWER")
#         print("=" * 80)

#         print(answer)

#     finally:

#         rag.close()