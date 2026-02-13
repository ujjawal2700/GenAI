from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

# Chain-of-Thoughts prompting
SYSTEM_PROMPT = """
you are a helpful Ai assistant who is specialized in resolving user's query.
for the given user input, analyze the input and break down the problem step by step.

The steps are: you get the user input, you analyze, you think, you think again and think for several times and then return the output with explanation.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Follow the strict JSON output as per schema.
2. Always perform one step at a time and wait for the next input.
3. Carefully analyze the user's input and provide a detailed explanation of your thought process.

Output format:
{{"step" : "string", "content" : "string"}}

Example:
Input: What is 2 + 2?
Output:{{"step" : "analyse", "content" : "Alright! The user is interested in maths query and he is asking a basic airthmatic operation."}}
Output:{{"step" : "think", "content" : "To perform this addition, I must go from left to right and add all the operands."}}
Output:{{"step" : "output", "content" : "4"}}
Output:{{"step" : "validate", "content" : "Seems like 4 is the correct answer for 2 + 2"}}
Output:{{"step" : "result", "content" : "2 + 2 is 4 and this is calaulated by adding all the numbers together."}}



Example:
Input: What is 2 + 2 * 5 /3
Output:{{"step" : "analyse", "content" : "Alright! The user is interested in maths query and he is asking a basic airthmatic operation."}}
Output:{{"step" : "think", "content" : "To solve this qeuation i must use BODMAS rule and solve the equation step by step."}}
Output:{{"step" : "validate", "content" : "Correct! using BODMAS is the right approach here."}}
Output:{{"step" : "think", "content" : "first i need to solve division that is 5 / 3 which gives 1.6666666666666667."}}
Output:{{"step" : "validate", "content" : "Correct! using BODMAS the divison must be performed first.."}}
Output:{{"step" : "think", "content" : "Now, as i have already solved 5 / 3 now the equation looks like 2 + 2 * 1.6666666666666667."}}
Output:{{"step" : "validate", "content" : "Yes! the new equation is absolutely correct."}}
and so on till the final output is achieved.


"""


# response = client.chat.completions.create(
#     model = "gpt-4.1-mini",
#     response_format={"type" : "json_object"},
#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "what is average of 54356, 766, 8757 and 7531"},
#         {"role" : "assistant", "content" : json.dumps({"step" : "analyse", "Content" : "The user is asking to find the average of four numbers: 54356, 766, 8757, and 7531. The average is computed by adding all numbers and dividing the sum by the total count of numbers."})},
#         {"role" : "assistant", "content" : json.dumps({"step": "think", "Content": "To find the average, I need to sum all the numbers: 54356 + 766 + 8757 + 7531, then divide by 4, as there are 4 numbers in total."})},
#         {"role" : "assistant", "content" : json.dumps({"step": "think", "Content": "Calculating the sum: 54356 + 766 = 55122; 55122 + 8757 = 63879; 63879 + 7531 = 71410. Now, dividing 71410 by 4 to get the average."})},
#         {"role" : "assistant", "content" : json.dumps({"step": "output", "Content": "The average is 71410 divided by 4, which equals 17852.5."})},
#         {"role" : "assistant", "content" : json.dumps({"step": "validate", "Content": "I have correctly summed all the numbers to 71410 and divided by 4, resulting in 17852.5 which is the correct average."})},
#         {"role" : "assistant", "content" : json.dumps({"step": "result", "Content": "The average of 54356, 766, 8757, and 7531 is 17852.5, calculated by summing all four numbers to get 71410 and dividing by 4."})},
        
        
#     ]
# )

# print("\n\n🤖",response.choices[0].message.content, "\n\n")


messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

query = input(">> ")
messages.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=messages
    )
    # print("\n\n🤖", response.choices[0].message.content, "\n\n")
    messages.append({"role" : "assistant", "content" : response.choices[0].message.content})
    parsed_response = json.loads(response.choices[0].message.content)
    # print("\n🤖", parsed_response, )
    
    if parsed_response.get("step") != "result":
        print("\n🧠:", parsed_response.get("content"))
        continue
    
    print("\n🤖", parsed_response.get("content"), "\n\n")
    break