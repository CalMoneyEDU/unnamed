import os
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv 
import prompts

# load the .env file
_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.environ.get("API_Key_Calv")
)

model = "gpt-4"
temperature = 0.3
max_tokens = 500
topic = "" # topic to generate text about
messages=[
            {
                "role": "system",
                "content": "you are a helpful assistant." # these need to be changed to the actual system message and prompt
            },
            {
                "role": "user",
                "content": "list out ten things that are made of gold." # this needs to be changed to the actual user message
            }
        ]

art = "a digital painting"
style = "surrealism"

system_message = prompts.system_message
prompt = prompts.generate_prompt(art, style)

def get_critique():
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content

print(get_critique())