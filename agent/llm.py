import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class LLMServiceError(Exception):
    pass


def ask_llm(message):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message
        )

        return response.text

    except errors.ClientError as error:

        if error.code == 429:
            raise LLMServiceError(
                "Gemini API quota has been exceeded. Please try again after the quota resets."
            )

        raise LLMServiceError(
            "The Gemini API request failed."
        )

    except errors.ServerError:
        raise LLMServiceError(
            "The Gemini service is temporarily unavailable. Please try again later."
        )