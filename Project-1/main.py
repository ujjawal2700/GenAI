import json
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    # API CALL TO GET WEATHER
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

available_tools = {
    "get_weather" : get_weather,
    "run_command" : run_command
}

SYSTEM_PROMPT = """ 

    You are a helpful AI Assistant who is specialised in resolving user's query.
    You work on start, plan, action, observe mode.
    
    for the given user query and available tools, plan the step by step execution, based on the planning.
    select the relevent tool from the available tools. and based on the tool selection you perform an action to call the tool.
    
    wait for the observation and based on the ovservation from the tool call resolve the user query.
    
    RULES:
    - Follow the output JSON format.
    - Always perform one step at a time and wait for next input.
    - Carefully analyse user's query.
    
    Available Tools:
    - "get_weather" : Takes the city name as the input and returns the current weather for the city.
    - "run_command" : Takes Linux command as a string an input and execute the command and return the output after executing it.
    
    Example:
    User Query: What is the weather of new york
    output: {"step": "plan", "content" : "The user is interested in weather data of New York."}
    output: {"step": "plan", "content" : "From the available tools i should call get_weather."}
    output: {"step": "action", "function" : "get_weather", "input" : "new york"}
    output: {"step": "observe", "output" : "12 degree Cel"}
    output: {"step": "output", "content" : "The weather of new york seems to be 12 degrees."}
    """

messages = [
    {"role" : "system", "content" : SYSTEM_PROMPT},
]
while True:

    query = input(">> ")
    messages.append({"role": "user", "content": query})
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            response_format={"type": "json_object"},
            messages=messages,
        )
        
        messages.append({"role" : "assistant", "content" : response.choices[0].message.content})
        parsed_response = json.loads(response.choices[0].message.content)
        
        if parsed_response.get("step") == "plan":
            print(f"🧠 : {parsed_response.get("content")}" )
            continue
        
        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")
            
            print(f"🛠️: Calling Tool: {tool_name} with input {tool_input}")
            
            if available_tools.get(tool_name) != False :
                output = available_tools[tool_name](tool_input)
                messages.append({"role" : "user", "content" : json.dumps({"step" : "observe", "output" : output})})
                continue 
            
            
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break