from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API = os.getenv("OPENAI_API")
OPENAI_API_KEY = OPENAI_API

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# 대화 내역을 저장할 리스트를 선언. 
message_history = []

# 무한 반복문(while True:)를 통해 계속 이어지는 대화문을 활성화.
while True:
    user_input = input("사용자: ")
    
    # 사용자의 질문을 리스트에 추가. 리스트의 각 요소는 role, content  키를 가진 딕셔너리 형태로 저장됨.
    message_history.append({"role": "user", "content": user_input})
    
    chat_completion = client.chat.completions.create(
        messages = message_history,
        model = "gpt-4o",
    )
    
    assistant_response = chat_completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": assistant_response})
    
    print(f"chatbot: {assistant_response}")