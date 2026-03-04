import streamlit
import asyncio
import json
from utils import llm_call, llm_search_async

def get_orchestrator_prompt(user_query):
    return f"""
    Analyze the following use question, then break it down into up to 3 related sub-questions.
    Output the result as a JSON array.
    Each sub-question inside the JSON array should be a JSON object following this format. 
    [
        {{
            "question": "sub question 1",
            "description": "point of this subquestion and explanation of the intention"
        }},
        {{
            "question": "sub question 2"
            "description": "point of this subquestion and explanation of the intention"
        }}
        ]
        
        User Query: {user_query}
        """
        
def get_worker_prompt(user_query, question, description):
    return f"""
    다음 사용자 질문에서 파생된 하위 질문을 보고 응답해. 
    사용자 질문: {user_query}
    하위 질문: {question}
    하위 질문의 의도: {description}
    하위 질문을 철저히 분석해 그에 대해 포괄적이고 상세하게 응답해.
    웹 검색 도구를 이용해 자료 조사를 하고, 이를 반영해 응답해.
    """

async def run_llm_parallel(prompt_details):
    tasks = [
        llm_search_async(item['user_prompt'], item['model'])
        for item in prompt_details
    ]
    responses = await asyncio.gather(*tasks)
    return responses

async def run_llm_parallel(prompt_details):
    tasks = [
        llm_search_async(item['user_prompt'], item['model'])
        for item in prompt_details
    ]

    responses = await asyncio.gather(*tasks)
    return responses    

        
    