from langchain_classic.tools.retriever import create_retriever_tool
from src.exceptions.custom_exceptions import CustomException
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os
from langchain_core.tools import Tool
from langchain.tools import tool
import sys
from src.loging.logger import log
load_dotenv()
from src.exceptions.custom_exceptions import CustomException
serpapi_key = os.getenv("SERPAPI_API_KEY")


#os.environ["SERPAPI_API_KEY"] = serpapi_key


if not serpapi_key:
    raise ValueError(
        "SERPAPI_API_KEY environment variable is not set. "
        "Please set it in your .env file or pass it as an environment variable."
    )
search_wrapper = SerpAPIWrapper(serpapi_api_key=serpapi_key)
from functools import lru_cache

@lru_cache(maxsize=1)
def google_search(query: str) -> str:
    """Search Google for current information."""
    try:
        # Explicitly pass query to avoid empty strings
        if not query:
            return "Error: Empty search query."
        return search_wrapper.run(query)
    except Exception as e:
        # Log the error to your console so you know WHY it failed
        log.error(f"SerpAPI Error: {e}") 
        raise CustomException(f"Error: The search tool is currently unavailable. Please rephrase. {e}",sys)



search = Tool(
    name="google_search",
    description="Search Google for current information retrive facts information or currency information.",
    func=search_wrapper.run # Note: passing the function itself
)
