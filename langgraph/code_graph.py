from typing_extensions import TypedDict
from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel # more likely to zod in JS, for validating outputs.

load_dotenv()
client = OpenAI()

class ClassifyMessageResponse(BaseModel):
    is_coding_question: bool
class CodeAccuracyResponse(BaseModel):
    accuracy_percentage: int

class State(TypedDict):
    user_query: str
    llm_result: str | None
    accuracy_percentage: int | None
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
    is_coding_question = response.choices[0].message.parsed.is_coding_question
    state["is_coding_question"] = is_coding_question
    return state

def route_query(state: State) -> Literal["general_query", "coding_query"]:
    is_coding_question = state["is_coding_question"]
    if is_coding_question:
        return "coding_query"
    else:
        return "general_query"
    
def refactor_code(state: State) -> Literal[END, "coding_query"]:
    code_accuracy = state["accuracy_percentage"]
    if code_accuracy < 80:
        return "coding_query"
    else:
        return END

def general_query(state: State):
    query = state["user_query"]
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": query},
        ]
    )
    state["llm_result"] = response.choices[0].message.content
    return state

def coding_query(state: State):
    query = state["user_query"]
    SYSTEM_PROMPT="""
    You are an Coding Expert Agent. Your job is to solve the users coding related query.
    The query can be in any of the computer languages or can be a theory based.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
    )
    state["llm_result"] = response.choices[0].message.content
    return state
    pass

def code_validate_query(state: State):
    query = state["user_query"]
    llm_code = state["llm_result"]
    SYSTEM_PROMPT="""
    You are a helpful AI assistant. Your job is to check the response of the other model which will be given to you. It will be more likely to an coding related response or some theory
    based response. you will be given to user query and the other llm response. You have to analyse the response and check is the repsponse of the other llm is how much accurate and clear. you have to give the number between 1 to 100 where 1 is the lowest (means the other llm response is not at all accurate) and 100 is the highest (means the response is accurate.)
    User Query: {query}
    llm response: {llm_code}
    Return the response in specified JSON boolean only.
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=CodeAccuracyResponse,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    state["accuracy_percentage"] = response.choices[0].message.parsed.accuracy_percentage
    return state


#graph building
graph_builder = StateGraph(State)
#adding nodes
graph_builder.add_node("classify_message", classify_message)
graph_builder.add_node("route_query", route_query)
graph_builder.add_node("general_query", general_query)
graph_builder.add_node("coding_query", coding_query)
graph_builder.add_node("code_validate_query", code_validate_query)
#adding edges
graph_builder.add_edge(START, "classify_message")
graph_builder.add_conditional_edges("classify_message", route_query)
graph_builder.add_edge("general_query", END)
graph_builder.add_edge("coding_query", "code_validate_query")
graph_builder.add_conditional_edges("code_validate_query", refactor_code)



graph = graph_builder.compile()

def main():
    user = input("> ")
    _state: State = {
        "user_query": user,
        "accuracy_percentage": None,
        "is_coding_question": False,
        "llm_result": None,
    }
    response = graph.invoke(_state)
    print(response)
    
main()