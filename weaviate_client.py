import configparser
import json
import os

import weaviate
from logging_config import setup_logger


logger = setup_logger()


class WeaviateClient:

    def __init__(self):
        self.client = None
        self.collection_name = "Movie_Metadata"

    def connect(self):

        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__),"config.ini")

        config.read(os.path.abspath(config_path))

        try:
            weaviate_url = config["WEAVIATE"]["WEAVIATE_URL"]
            weaviate_api_key = config["WEAVIATE"]["WEAVIATE_API"]

            self.client = weaviate.connect_to_weaviate_cloud(
                cluster_url=weaviate_url,
                auth_credentials=weaviate.auth.AuthApiKey(weaviate_api_key))

            logger.info("Weaviate connection established successfully!")

            return self.client

        except Exception as e:
            logger.error(f"Weaviate connection failed: {e}")
            raise

    def search_movies(self,query: str,limit: int = 5) -> list:

        collection = self.client.collections.use(self.collection_name)

        response = collection.query.near_text(
            query=query,
            limit=limit
        )

        results = []

        for obj in response.objects:
            results.append(obj.properties)

        return results

    def close(self):

        if self.client:
            self.client.close()

            logger.info("Weaviate connection closed.")


if __name__ == "__main__":

    weaviate_client = WeaviateClient()

    try:

        client = weaviate_client.connect()

        if client.is_ready():

            exists = client.collections.get("Movie_Metadata" ).exists()

            print(f"Movie_Metadata collection exists: {exists}")

            results = weaviate_client.search_movies(
                query="Action movies from 2012 to 2014",
                limit=2
            )

            for result in results:
                print(json.dumps(result,indent=2))

    finally:

        weaviate_client.close()