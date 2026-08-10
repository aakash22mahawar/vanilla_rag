import json

from pydantic import BaseModel, Field

from logging_config import setup_logger
from llm import LLMClient

# Initialize the logger

logger = setup_logger()


# -----------------------------
# Movie query filter model
# -----------------------------

class MovieQueryFilters(BaseModel):

    genre: str | None = Field(
        default=None,
        description="Movie genre mentioned in the user's query."
    )

    start_year: int | None = Field(
        default=None,
        description="Starting year of the requested movie range."
    )

    end_year: int | None = Field(
        default=None,
        description="Ending year of the requested movie range."
    )

    sort_by: str | None = Field(
        default=None,
        description="Movie property used to sort the results."
    )

    sort_order: str | None = Field(
        default=None,
        description="Sort direction: ascending or descending."
    )


# -----------------------------
# Query Parser
# -----------------------------

class QueryParser:

    def __init__(
        self,
        llm_client: LLMClient
    ):

        self.llm_client = llm_client

        logger.info(
            "Query parser initialized successfully!"
        )


    # -----------------------------
    # Parse user query
    # -----------------------------

    def parse(
        self,
        query: str
    ) -> MovieQueryFilters:

        try:

            prompt = f"""
                    You are a movie search query parser.

                    Extract the following information from the user's
                    movie search query:

                    - genre
                    - start_year
                    - end_year
                    - sort_by
                    - sort_order

                    Rules:

                    1. Extract the movie genre if mentioned.
                    2. Extract the starting year if a year range is mentioned.
                    3. Extract the ending year if a year range is mentioned.
                    4. If the user asks for highest or best IMDb rating,
                       set sort_by to "imdb_score".
                    5. If the user asks for lowest IMDb rating,
                       set sort_by to "imdb_score".
                    6. Use "descending" for highest or best.
                    7. Use "ascending" for lowest.
                    8. If sorting is not requested, return null
                       for sort_by and sort_order.
                    9. Do not invent or assume values.
                    10. Return the result according to the provided schema.

                    User query:
                    {query}
                    """

            logger.info(
                f"Parsing user query: {query}"
            )

            filters = self.llm_client.generate_structured(
                prompt=prompt,
                response_model=MovieQueryFilters
            )

            logger.info(
                "User query parsed successfully."
            )

            return filters

        except Exception as e:

            logger.error(
                f"User query parsing failed: {e}"
            )

            raise


# -----------------------------
# Test query parser
# -----------------------------

# if __name__ == "__main__":

#     llm_client = LLMClient()

#     query_parser = QueryParser(
#         llm_client=llm_client
#     )

#     try:

#         query = (
#             "Which action movie between 2012 and 2014 "
#             "had the highest IMDb rating?"
#         )

#         filters = query_parser.parse(
#             query=query
#         )

#         print("\n" + "=" * 80)
#         print("PARSED QUERY FILTERS")
#         print("=" * 80)

#         print(
#             json.dumps(
#                 filters.model_dump(),
#                 indent=2
#             )
#         )

#     finally:

#         logger.info(
#             "Query parser test completed."
#         )