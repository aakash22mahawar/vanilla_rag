import configparser
import json
import os

import weaviate
from weaviate.classes.query import Filter, Sort

from logging_config import setup_logger

# Initialize the logger

logger = setup_logger()


class WeaviateClient:

    def __init__(self):

        self.client = None
        self.collection_name = "Movie_Metadata"

    # -----------------------------
    # Establish Weaviate connection
    # -----------------------------

    def connect(self):

        config = configparser.ConfigParser()

        config_path = os.path.join(
            os.path.dirname(__file__),
            "config.ini"
        )

        config.read(
            os.path.abspath(config_path)
        )

        try:

            # Read Weaviate configuration

            weaviate_url = config["WEAVIATE"]["WEAVIATE_URL"]
            weaviate_api_key = config["WEAVIATE"]["WEAVIATE_API"]

            # Establish Weaviate connection

            self.client = weaviate.connect_to_weaviate_cloud(
                cluster_url=weaviate_url,
                auth_credentials=weaviate.auth.AuthApiKey(
                    weaviate_api_key
                )
            )

            logger.info(
                "Weaviate connection established successfully!"
            )

            return self.client

        except Exception as e:

            logger.error(
                f"Weaviate connection failed: {e}"
            )

            raise

    # -----------------------------
    # Search movies
    # -----------------------------

    def search_movies(
        self,
        query: str,
        genre: str | None = None,
        start_year: int | None = None,
        end_year: int | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        limit: int = 5
    ) -> list:

        try:

            collection = self.client.collections.use(
                self.collection_name
            )

            weaviate_filters = None

            # -----------------------------
            # Start year filter
            # -----------------------------

            if start_year is not None:

                weaviate_filters = Filter.by_property(
                    "title_year"
                ).greater_or_equal(
                    start_year
                )

            # -----------------------------
            # End year filter
            # -----------------------------

            if end_year is not None:

                year_filter = Filter.by_property(
                    "title_year"
                ).less_or_equal(
                    end_year
                )

                if weaviate_filters is None:

                    weaviate_filters = year_filter

                else:

                    weaviate_filters = (
                        weaviate_filters & year_filter
                    )

            # -----------------------------
            # Genre filter
            # -----------------------------

            if genre is not None:

                genre_filter = Filter.by_property(
                    "genres"
                ).like(
                    f"*{genre}*"
                )

                if weaviate_filters is None:

                    weaviate_filters = genre_filter

                else:

                    weaviate_filters = (
                        weaviate_filters & genre_filter
                    )

            # -----------------------------
            # Execute Weaviate query
            # -----------------------------

            if sort_by is not None:

                # -----------------------------
                # Validate supported sort field
                # -----------------------------

                allowed_sort_fields = {
                    "imdb_score"
                }

                if sort_by not in allowed_sort_fields:

                    raise ValueError(
                        f"Unsupported sort field: {sort_by}"
                    )

                # -----------------------------
                # Determine sort direction
                # -----------------------------

                ascending = (
                    sort_order == "ascending"
                )

                sort = Sort.by_property(
                    name=sort_by,
                    ascending=ascending
                )

                response = collection.query.fetch_objects(
                    filters=weaviate_filters,
                    sort=sort,
                    limit=limit
                )

                logger.info(
                    f"Executed filtered movie query sorted by "
                    f"{sort_by} ({sort_order})."
                )

            else:

                # -----------------------------
                # Semantic search
                # -----------------------------

                response = collection.query.near_text(
                    query=query,
                    limit=limit,
                    filters=weaviate_filters
                )

                logger.info(
                    "Executed semantic movie search."
                )

            # -----------------------------
            # Extract results
            # -----------------------------

            results = []

            for obj in response.objects:

                results.append(
                    obj.properties
                )

            logger.info(
                f"Successfully retrieved {len(results)} movie records."
            )

            return results

        except Exception as e:

            logger.error(
                f"Movie search failed: {e}"
            )

            raise

    # -----------------------------
    # Close Weaviate connection
    # -----------------------------

    def close(self):

        if self.client:

            self.client.close()

            logger.info(
                "Weaviate connection closed."
            )


# -----------------------------
# Test Weaviate connection
# -----------------------------

# if __name__ == "__main__":

#     weaviate_client = WeaviateClient()

#     client = weaviate_client.connect()

#     try:
#
#         if client.is_ready():
#
#             exists = client.collections.get(
#                 "Movie_Metadata"
#             ).exists()
#
#             print(
#                 f"Movie_Metadata collection exists: {exists}"
#             )
#
#         # Search movies using filters
#
#         results = weaviate_client.search_movies(
#             query="Action movies from 2012 to 2014",
#             genre="Action",
#             start_year=2012,
#             end_year=2014,
#             limit=5
#         )
#
#         for result in results:
#
#             print(
#                 json.dumps(
#                     result,
#                     indent=2
#                 )
#             )
#
#     finally:
#
#         weaviate_client.close()