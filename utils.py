from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API = os.getenv("OPENAI_API")
OPENAI_API_KEY = OPENAI_API

# 클라이언트 생성. 동기 방식으로 작동하므로 sync_client으로 정의. 
# 동기 방식은 작업을 요청한 뒤 결과가 나올 때까지 기다린 다음 후속 작업으로 넘어가는 것이다. 
sync_client = OpenAI(
    api_key = OPENAI_API_KEY,
)

def llm_call(prompt: str, model: str = "gpt-4o-mini") -> str:
    messages = []
    
    messages.append(
        {
        "role": "user", 
        "content": prompt}
        )
    
    
    chat_completion = sync_client.chat.completions.create(
        model = model,
        messages = messages,
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    test = llm_call("한국의 수도는?")
    print(test)
    
    