import configparser
import os

from openai import OpenAI
from pydantic import BaseModel
from logging_config import setup_logger


# Initialize the logger
logger = setup_logger()


class LLMClient:

    def __init__(self):

        # Load configuration
        config = configparser.ConfigParser()

        config_path = os.path.join( os.path.dirname(__file__),"config.ini")

        config.read(os.path.abspath(config_path))

        try:

            # Read xAI configuration
            self.grok_api_key = config["XAI"]["GROK_API_KEY"]
            self.grok_base_url = config["XAI"]["GROK_BASE_URL"]
            self.grok_model = config["XAI"]["GROK_MODEL"]

            # Establish LLM client
            self.client = OpenAI(api_key=self.grok_api_key,base_url=self.grok_base_url)

            logger.info("LLM client initialized successfully!")

        except Exception as e:

            logger.error(f"LLM client initialization failed: {e}")

            raise


    # -----------------------------
    # Generate LLM response
    # -----------------------------

    def generate(self, prompt: str) -> str:

        try:

            response = self.client.chat.completions.create(
                model=self.grok_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6
            )

            answer = response.choices[0].message.content

            logger.info("LLM response generated successfully.")

            return answer

        except Exception as e:

            logger.error(
                f"LLM response generation failed: {e}"
            )

            raise


    # -----------------------------
    # Generate structured response
    # -----------------------------

    def generate_structured(
            self,
            prompt: str,
            response_model: type[BaseModel]
    ) -> BaseModel:

        try:

            response = self.client.beta.chat.completions.parse(
                model=self.grok_model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.0,
                response_format=response_model
            )

            parsed_response = response.choices[0].message.parsed

            logger.info(
                "Structured LLM response generated successfully."
            )

            return parsed_response

        except Exception as e:

            logger.error(
                f"Structured LLM response generation failed: {e}"
            )

            raise    


# -----------------------------
# Test LLM connection
# -----------------------------

# if __name__ == "__main__":

#     llm_client = LLMClient()

#     try:

#         prompt = """
#         Tell me in one sentence why retrieval augmented generation
#         is useful for question answering.
#         """

#         response = llm_client.generate(
#             prompt=prompt
#         )

#         print("\n" + "=" * 80)
#         print("LLM RESPONSE")
#         print("=" * 80)

#         print(response)

#     finally:

#         logger.info("LLM test completed.")