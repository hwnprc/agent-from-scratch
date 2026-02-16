import streamlit as st 
import re
from utils import llm_call

def llm_router_call(user_prompt: str) -> str:
    router_prompt = f"""
    User Question: {user_prompt}
    
    위 질문에 대해 가장 적절한 유형을 하나 골라
    - 일상: 일반적인 대화, 일정 짜기, 정보 요청 등
    - 빠른: 계산, 단답형 질문, 간단한 명령 등
    - 코딩: 파이썬, 코드 작성, 오류 디버깅 등
    단답형으로 유형만 출력해.
    """
    routing_result = llm_call(router_prompt, model="gpt-4o-mini").strip()
    return routing_result

def run_general_agent(user_prompt: str):
    prompt = f"""
    너는 다재다능한 일상 도우미야. 
    여행 일정, 추천, 요약 등 일상적인 질문에 친절하고 유용하게 답변하지. 
    
    [사용자 질문]
    {user_prompt}
    """
    
    response = llm_call(prompt, model="gpt-4o")
    st.write("🐝 Daily Agent Response")
    st.write(response)
    
def run_quick_agent(user_prompt: str):
    prompt = f"""
    너는 빠르고 간단한 응답을 제공하는 빠른 에이전트야.
    사용자의 질문에 두괄식으로 간결하게 답변하지.
    
    [사용자 질문]
    {user_prompt}
    """
    response = llm_call(prompt, model="gpt-4o-mini")
    st.markdown("🫡 Quick Agent Response")
    st.success(response)
    
    
def run_coding_agent(user_prompt: str):
    prompt = f"""
    너는 뛰어난 코딩 비서야.
    파이썬, 자바스크립트, API 개발, 오류 디버깅 등에 능숙해.
    질문에 대해 최대한 정확하게 실행 가능한 코드를 제공하지.

    [사용자 질문]
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

if st.button("Agent Run") and user_input.strip():
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
    