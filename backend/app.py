from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import prompts

load_dotenv()
client = OpenAI(api_key=os.getenv("API_Key_Calv"))

app = Flask(__name__)

@app.route("/api/critique", methods=["POST"])
def critique():
    data = request.get_json()
    art = data.get("art", "a digital painting")
    style = data.get("style", "surrealism")

    prompt = prompts.generate_prompt(art, style)
    messages = [
        {"role": "system", "content": prompts.system_message},
        {"role": "user", "content": prompt}
    ]

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3,
        max_tokens=500,
    )

    return jsonify({"critique": completion.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)
    