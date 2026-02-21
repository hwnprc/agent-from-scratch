import streamlit as st 
import asyncio
from utils import llm_call_async

async def run_llm_parallel(prompt_details):
    
    tasks = [
        llm_call_async(prompt["user_prompt"], prompt["model"])
        for prompt in prompt_details
        
    ]
    responses = []
    
    for task in asyncio.as_completed(tasks):
        result = await task
        responses.append(result)
        
    with st.expander("모델 응답 전체 보기"):
        for response in responses:
            st.markdown(f"모델 응답: {response}")
            
    return responses

async def run_parallel_agent(question, selected_models):
    parallel_prompt_details = [
        {"user_prompt": question, "model": model} for model in selected_models
    ]
    
    responses = await run_llm_parallel(parallel_prompt_details)
    
    aggregator_prompt = (
        "This is the response that many llm created based on the user's prompt.\n"
        "Your role is to aggregate these responses and give one final translation.\n"
        "Since some responses might be not accurate and biased, try to give credible and accurate response.\n"
        "Only print the final response.\n"
        "User Prompt:\n"
        f"{question}\n\n"
        "Model Response:"
    )
    for i in range(len(parallel_prompt_details)):
        aggregator_prompt += f"\n{i+1}. model response: {responses[i]}\n"
        
    with st.expander("Check Final Prompt", expanded=False):
        st.code(aggregator_prompt, language='markdown')
        
    final_respnose = await llm_call_async(aggregator_prompt, model="gpt-4o")
    st.subheader("Final Response")
    st.markdown(final_respnose)
    
def main():
    st.title("Parallel Processing Agent")
    question = st.text_area(
        "User Prompt",
        height = 100,
        value = """Try to translate this sentence into natural korean.
        "Do what you can, with what you have, where you are" - Theodore Roosevelt
        """)
    model_options = ["gpt-4o", "gpt-4o-mini", "o3"]
    selected_models = st.multiselect(
        "Select the model",
        model_options,
        default = model_options[:3]
    )
    
    if st.button("Run Agent"):
        if not question.strip():
            st.warning("Write down your question.")
        elif not selected_models:
            st.warning("Choose more than one model.")
        else:
            asyncio.run(run_parallel_agent(question.strip(), selected_models))
            
if __name__ == "__main__":
    main()