# Package Import 
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API = os.getenv("OPENAI_API")
OPENAI_API_KEY = OPENAI_API

# Generate Client
client = OpenAI(
    api_key=OPENAI_API_KEY
)

# API request and response
chat_completion = client.chat.completions.create(
    messages = [
        {
            "role": "user",
            "content": "Say this is a test.",
        }
    ],
    model = "gpt-4o",
)

# Print the response
print(chat_completion.choices[0].message.content) 
#API 응답에 여러 개의 답변이 포함될 수 있어 choices 라는 리스트를 사용하며, 보통은 응답이 하나이기 때문에 choices[0] 으로 첫 번째 응답을 가져온다. 
#응답에는 텍스트로 된 응답 본문 뿐만 아니라 응답 아이디, 모델 이름, 토큰 사용량 등 다양한 정보가 들어있는데, 여기서는 응답의 본문 'message.content'만 출력한다. 