
from datetime import datetime, timedelta
import json
import openai
import os
import random
import sys

#region Config
try:
    f = open('Config.txt','r')
    
    while(True):
        linea = f.readline()
        if not linea:
            break
        array_line = linea.replace(" ","").replace("\n","").split(':=')
        
        if array_line[0].upper() == "OPENAI_API_TYPE":
            os.environ["OPENAI_API_TYPE"] = array_line[1]
        if array_line[0].upper() == "OPENAI_API_VERSION":
            os.environ["OPENAI_API_VERSION"] = array_line[1]
        if array_line[0].upper() == "OPENAI_API_BASE":
            os.environ["OPENAI_API_BASE"] = array_line[1]
        if array_line[0].upper() == "OPENAI_API_KEY":
            os.environ["OPENAI_API_KEY"] = array_line[1]
        if array_line[0].upper() == "AZURE_OPENAI_ENDPOINT":
            os.environ["AZURE_OPENAI_ENDPOINT"] = array_line[1]
    f.close()
except:
    print("Ha ocurrido un error leyendo el archivo config: {}".format(sys.exc_info()[0]))

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

model_engine = "gpt-35-turbo"
#endregion

function_descriptions = [
    {
        "name": "get_sum",
        "description": "Sum two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "first_number": {
                    "type": "number",
                    "description": "The first number",
                },
                "second_number": {
                    "type": "number",
                    "description": "The second number",
                },
                "result_number": {
                    "type": "number",
                    "description": "The result of the prompt",
                }
            },
            "required": ["first_number", "second_number", "result_number"],
        },
    }
]

num1 = random.randint(0, 9)
num2 = random.randint(0, 9)
user_prompt = "Can you please sum {} + {}.".format(num1,num2)

completion = openai.chat.completions.create(
    model= model_engine,
    messages=[{"role": "user", "content": user_prompt}],
    # Add function calling
    functions=function_descriptions,
    function_call="auto",  # specify the function call
    temperature=1,
        max_tokens=50,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
)


# Note: the function does not exist yet

def get_sum(first_number, second_number, result_number):
    """Sum two numbers"""

    # Example output returned from an API or database
    sum_info = {
        "first_number": first_number,
        "second_number": second_number,
        "result_number": result_number,
        "Operation": "Sum"
    }

    return json.dumps(sum_info)


# It automatically fills the arguments with correct info based on the prompt
output = completion.choices[0].message
params = json.loads(output.function_call.arguments)

# Call the function with arguments
chosen_function = eval(output.function_call.name)
sum_result = chosen_function(**params)

print(sum_result)