import streamlit as st 
import re
from utils import llm_call

def llm_router_call(user_prompt: str) -> str:
    router_prompt = f"""
    User Question: {user_prompt}
    
    Choose the most appropriate type for the above question.
        - casual: General conversation, scheduling, information requests, etc.
        - quick: Calculations, short answers, simple commands, etc.
        - coding: Python, code writing, debugging errors, etc.
        
        Output only the type in a single word.
        """
    routing_result = llm_call(router_prompt, model="gpt-4o-mini").strip()
    return routing_result

def run_general_agent(user_prompt: str):
    prompt = f"""
    You are a versatile daily assistant.
You answer everyday questions such as travel itineraries, recommendations, summaries, etc. in a friendly and helpful manner.

[User Question]
    {user_prompt}
    """
    
    response = llm_call(prompt, model="gpt-4o")
    st.write("🐝 Daily Agent Response")
    st.write(response)
    
def run_quick_agent(user_prompt: str):
    prompt = f"""
    You are a quick agent that provides fast and simple responses.
You answer the user's questions concisely in a top-down manner (starting with the main point first).

[User Question]
    {user_prompt}
    """
    response = llm_call(prompt, model="gpt-4o-mini")
    st.markdown("🫡 Quick Agent Response")
    st.success(response)
    
    
def run_coding_agent(user_prompt: str):
    prompt = f"""
    You are an excellent coding assistant.
You are skilled in Python, JavaScript, API development, error debugging, etc.
You provide executable code as accurately as possible for the question.

[User Question]
    {user_prompt}
    """
    
    response = llm_call(prompt, model="o3")
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)
    last_code = code_blocks[-1].strip() if code_blocks else None
    st.markdown("🙌🏻 Coding Agent Response")
    tab1, tab2 = st.tabs(["👩🏻‍🍼 Total Response", "💻 Total Code"])
    with tab1:
        st.write(response)
    with tab2:
        if last_code:
            st.code(last_code, language="python")
        else:
            st.info("Code block is not detected.")

if __name__ == "__main__":
    st.set_page_config(page_title="Routing Agent", layout="centered")
    st.title("🤖 Routing Agent")
    st.markdown("Based on the user's prompt, we choose adequate agent and reply in an optimized version.")    
    
user_input = st.text_input("User Question")

if st.button("Run Agent") and user_input.strip():
    with st.spinner("Agent is analyzing.."):
        category = llm_router_call(user_input)
        st.markdown(f"🔍 Category Result: `{category}`")
        
        ROUTING_MAP={
            "casual" : run_general_agent,
            "quick": run_quick_agent,
            "coding": run_coding_agent
        } 
        
        final_llm_call = ROUTING_MAP.get(category, run_general_agent)
        final_llm_call(user_input)
    