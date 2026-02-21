import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API = os.getenv("OPENAI_API")
OPENAI_API_KEY = OPENAI_API

async_client = AsyncOpenAI(api_key= OPENAI_API_KEY)

async def llm_search_async(prompt: str, model: str = "gpt-4.1") -> str:
    #actual API call
    response = await async_client.responses.create(
        model = model,
        input = prompt,
        tools = [{"type": "web_search_preview"}], #tells model to use web search
    )
    return response.output_text #from the response object, extracts just the text content and returns int.

async def main():
    # defines the question we want to ask. 
    prompt = "Find me some interesting news from today" 
    # Calls the search function with the prompt and waits for the result
    result = await llm_search_async(prompt)
    print("\n💡 Web Search Result")
    print(result)
    
# starts the async event loop and runs main()
if __name__ == "__main__":
    asyncio.run(main())
