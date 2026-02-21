import asyncio
import json
from utils import llm_call, llm_search_async

# 1. Define Orchestrator prompt generator Function
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
            "question": "sub question 2",
            "description": "point of this subquestion and explanation of the intention"
            
        }}
        
    ]
    User Query: {user_query}
    """
    
def get_worker_prompt(user_query, question, description):
    return f"""
    Look at the sub-questions derived from the following user question and respond to them.
    Userquery: {user_query}
    subquestion: {question}
    Intention of subquestion: {description}
    Thoroughly analyze the sub-questions and provide a comprehensive, detailed response to each. 
    Use the web search tool to research relevant information and reflect it in your answers.
    """
    
async def run_llm_parallel(prompt_details):
    tasks = [
        llm_search_async(item['user_prompt'], item['model'])
        for item in prompt_details
    ]

    responses = await asyncio.gather(*tasks)
    return responses


# Define function for Orchestrator-worker workflow execution
async def run_orchestrator_workflow(user_query):
    orchestrator_prompt = get_orchestrator_prompt(user_query)
    orchestrator_response = llm_call(orchestrator_prompt, model="gpt-4o")
    
    subtask_list = json.loads(
        orchestrator_response.replace('```json','').replace('```', '')
    )
    # print sub question
    for i, subtask in enumerate(subtask_list, start=1):
        print(f"\n--- Sub question {i} ---")
        print("Question:", subtask['question'])
        print("Explanation", subtask['description'])
        
    worker_prompt_details = [
        {
            "user_prompt": get_worker_prompt(
                user_query, 
                subtask["question"],
                subtask["description"]
            ),
            "model": "gpt-4.1"
        }
        for subtask in subtask_list
    ]
    
    print("\n========== Sample Worker Prompt ==========")
    print(worker_prompt_details[0]['user_prompt'])
    
    worker_responses = await run_llm_parallel(worker_prompt_details)
    
    print("\n========== Workder Response Result ===========")
    for i, responses in enumerate(worker_responses, 1):
        print(f"\n--- Lower Question {i} Response ---")
        print(responses)
        
        
    aggregator_prompt=(
        "Tje following are responses received by breaking down the user's question into sub-questions.\n"
        "Synthesize all of this and provide a final answer.\n"
        "Include the responses to the sub-questions as comprehensivley and in as much detail as possible.\n"
        f"User Query: {user_query}\n\n"
        "subquestion and response:\n"
    )       
    
    for i, task in enumerate(subtask_list):
        aggregator_prompt += f"\n{i+1}. SubQuestion : {task['question']}\n"
        aggregator_prompt += f" Response: {worker_responses[i]}\n"
        
        final_response = llm_call(aggregator_prompt, model="gpt-4o")
    print("\n========== Final Report Result ==========")
    print(final_response)
        
        
# 3. Define main function and execute workflow
async def main():
    user_query = "how will AI services evolve? in 2026"
    final_output = await run_orchestrator_workflow(user_query)
    
if __name__ == "__main__":
    asyncio.run(main())