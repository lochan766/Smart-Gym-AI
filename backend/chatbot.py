import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def chatbot_response(msg):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a fitness assistant."},
                {"role": "user", "content": msg}
            ]
        )
        return res.choices[0].message.content

    except Exception as e:
        print(e)
        return "Ask me about workout or diet!"