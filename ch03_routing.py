from utils import llm_call

#defines a function that takes user's question as input and returns a string (the category type)
def llm_router_call(user_prompt: str) -> str:
    # using an f-string to insert the acutal user question into the prompt
    router_prompt = f""" 
        User question: {user_prompt}
        
        Choose the most appropriate type for the above question.
        - casual: General conversation, scheduling, information requests, etc.
        - quick: Calculations, short answers, simple commands, etc.
        - coding: Python, code writing, debugging errors, etc.
        
        Output only the type in a single word.
        """
    
    routing_result = llm_call(router_prompt).strip() #removes any leading whitespace from the response
    return routing_result #returns the classification result. among three

def run_general_agent(user_prompt: str) -> str:
    prompt = f"""
    너는 다재다능한 일상 도우미야. 
    여행 일정, 추천, 요약 등 일상적인 질문에 친절하고 유용하게 답변하지. 
    
    [사용자 질문]
    {user_prompt}
    """
    return llm_call(prompt, model="gpt-4o")

def run_quick_agent(user_prompt: str) -> str:
    prompt = f"""
    너는 빠르고 간단한 응답을 제공하는 빠른 에이전트야.
    사용자의 질문에 두괄식으로 간결하게 답변하지.
    
    [사용자 질문]
    {user_prompt}
    """
    return llm_call(prompt, model="gpt-4o-mini")

def run_coding_agent(user_prompt: str) -> str:
    prompt = f"""
    너는 뛰어난 코딩 비서야.
    파이썬, 자바스크립트, API 개발, 오류 디버깅 등에 능숙해.
    질문에 대해 최대한 정확하게 실행 가능한 코드를 제공하지.

    [사용자 질문]
    {user_prompt}
    """
    return llm_call(prompt, model="o3")

# ensures the following code only runs when the script is executed directly (not when imported)
if __name__ == "__main__":
    
    #Creates a dictionary mapping each question type to a specific AI model
    #ROUTING_MAP = {
    #    "casual" : "gpt-4o",
    #    "quick": "gpt-4o-mini",
    #    "coding": "o3"
    #}
    
    queries = [
        "Plan a Lisbon travel itinerary for me.",
        "What is 1 plus 2?",
        "Create an API web server with Python."
    ]
    
    ROUTING_MAP={
            "casual" : run_general_agent,
            "quick": run_quick_agent,
            "coding": run_coding_agent
        } 
    
    #print final responses based on each question
    for query in queries: #query takes on each value one at a time. 
        
        print("\n==사용자 질문==")
        print(query)
        
        category = llm_router_call(query)
        
        final_llm_call = ROUTING_MAP.get(category, run_general_agent)
        response = final_llm_call(query)
    
        
        """
        #looks up which model to use based on the category. if category not found, defaults to "gpt-4o"
        selected_model = ROUTING_MAP.get(category, "gpt-4o")
        print(f"[question] {query}") #print the current question and which model was selected
        print(f"[selected model] {selected_model}")
        
        response = llm_call(query, model=selected_model) 
        #creating a variable call 'response' and storing the result returned by the 'llm_call; function, 
        #which we call with the 'query' and 'selected_model' as arguments.
        print("[model response result]")
        print(response)
        result = llm_router_call(query)
        """        
        
        print("[model reponse result]")
        print(f"Question: {query} => Type: {category}")
        
        
    """
    Old Flow:
    User Question -> Router -> Get model name -> llm_call (query, model) -> Response
    
    New Flow:
    User Question -> Router -> Get agent function -> Agent function with custom prompt -> llm_call -> Reponse
    
    """