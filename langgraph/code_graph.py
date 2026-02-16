from typing_extensions import TypedDict
from openai import OpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel

load_dotenv()
client = OpenAI()

class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool

class State(TypedDict):
    user_query: str
    llm_result: str | None
    accuracy_percentage: str | None
    is_coding_question: bool | None
    
    
def classify_message(state: State):
    query: str = state["user_query"]
    SYSTEM_PROPMT = """
    You are an helpful AI assistant. Your job is to determine whether the user's query is a coding question or not.
    Return the response in specified JSON boolean only.
    """

    #Structured Response
    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format=ClassifyMessageResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROPMT},
            {"role": "user", "content": query},
        ]
    )