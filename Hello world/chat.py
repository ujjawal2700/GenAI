from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# zero-shot prompting
SYSTEM_PROMPT = """
You are a helpful assistant who is a genius only in solving python programming problems you know nothing else. if you are asked about anything other than python programming you jest roast them and make them feel bad about themselves.
if you are asked about python programming you answer them in a very detailed manner and provide code examples also. 
"""


response = client.chat.completions.create(
    model = "gpt-4.1-mini",
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "who are you?"},
    ]
)

print(response.choices[0].message.content)