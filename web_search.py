from tavily import AsyncTavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = AsyncTavilyClient(
     api_key=os.environ.get("TAVILY_API_KEY")
)

async def get_web_result(ai_query):

    try:
        response = await client.search(
            query=ai_query,
            search_depth="advanced"
        )
        return response
    except Exception as e:
        return "Web search didn't work, please try again."
    


